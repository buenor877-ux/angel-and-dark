"""Testes do projétil genérico: anda, faz arco com gravidade e some quando deve."""

import pygame
import pytest

from jogo.projeteis import Projetil

DT = 1 / 60
PAREDE = pygame.Rect(400, 0, 40, 1000)
CHAO = pygame.Rect(0, 1000, 2000, 80)


def semente(**extra):
    cfg = {"largura": 12, "altura": 12, "cor": [230, 200, 80], "velocidade": 240, "alcance": 1000}
    cfg.update(extra)
    return Projetil.de_config(cfg, (100, 500), -1)


def rodar(pr, quadros, solidos=()):
    for _ in range(quadros):
        pr.atualizar(DT, list(solidos))


def test_sai_no_lugar_certo_e_anda_reto_para_o_lado_pedido():
    pr = semente()
    assert pr.rect.center == (100, 500)
    rodar(pr, 30)  # meio segundo
    assert pr.rect.centerx == pytest.approx(100 - 120, abs=1)
    assert pr.rect.centery == 500  # sem gravidade: reto
    assert pr.ativo


def test_com_gravidade_faz_arco():
    pr = semente(velocidade_y=-300, gravidade=1200)
    alturas = []
    for _ in range(40):
        rodar(pr, 1)
        alturas.append(pr.rect.centery)
    assert min(alturas) < 500  # subiu
    assert alturas[-1] > min(alturas)  # e depois desceu


def test_some_ao_bater_na_parede():
    pr = Projetil((300, 500), (300, 0), (12, 12), (255, 255, 0))
    rodar(pr, 60, [PAREDE])
    assert not pr.ativo
    assert pr.rect.right <= PAREDE.left + 6  # parou na parede, não atravessou


def test_some_ao_cair_no_chao():
    pr = Projetil((300, 900), (100, 0), (12, 12), (255, 255, 0), gravidade=1800)
    rodar(pr, 60, [CHAO])
    assert not pr.ativo


def test_some_depois_do_alcance():
    pr = semente(alcance=200)
    rodar(pr, int(200 / 240 * 60) - 2)
    assert pr.ativo
    rodar(pr, 4)
    assert not pr.ativo


def test_acerta_uma_vez_so_e_some():
    pr = semente()
    alvo = pygame.Rect(90, 480, 32, 48)
    assert pr.acertou(alvo)
    assert not pr.ativo
    assert not pr.acertou(alvo)  # já sumiu: não machuca de novo


def test_nao_acerta_quem_esta_longe():
    pr = semente()
    assert not pr.acertou(pygame.Rect(600, 480, 32, 48))
    assert pr.ativo


def test_desenha_sem_erro_e_some_do_desenho():
    class Camera:
        def na_tela(self, r):
            return r

    tela = pygame.Surface((960, 540))
    pr = semente()
    pr.desenhar(tela, Camera())
    pr.ativo = False
    pr.desenhar(tela, Camera())
