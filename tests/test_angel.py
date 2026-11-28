"""Testes do movimento da Angel, sem abrir janela.

Cada teste simula alguns quadros com comandos fixos e confere o resultado.
"""

import pygame
import pytest

from jogo.nucleo import config
from jogo.nucleo.controles import Comandos
from jogo.personagens.angel import Angel
from jogo.personagens.personagem import Estado

DT = 1 / 60
CHAO = pygame.Rect(0, 500, 960, 40)


@pytest.fixture
def cfg():
    return config.carregar("personagens")["angel"]


def simular(angel, comandos, plataformas, quadros):
    for _ in range(quadros):
        angel.atualizar(DT, comandos, plataformas)


def angel_no_chao(cfg):
    """Angel apoiada no chão, já assentada."""
    angel = Angel(cfg, (100, 500 - cfg["altura"] - 10))
    simular(angel, Comandos(), [CHAO], 30)
    return angel


def test_cai_e_para_no_chao(cfg):
    angel = angel_no_chao(cfg)
    assert angel.no_chao
    assert angel.rect.bottom == CHAO.top
    assert angel.estado == Estado.PARADO


def test_anda_para_a_direita_e_esquerda(cfg):
    angel = angel_no_chao(cfg)
    x0 = angel.rect.x
    simular(angel, Comandos(direita=True), [CHAO], 20)
    assert angel.rect.x > x0
    assert angel.estado == Estado.ANDANDO

    x1 = angel.rect.x
    simular(angel, Comandos(esquerda=True), [CHAO], 40)
    assert angel.rect.x < x1


def test_nao_passa_da_velocidade_maxima(cfg):
    angel = angel_no_chao(cfg)
    simular(angel, Comandos(direita=True), [CHAO], 120)
    assert angel.vel_x == pytest.approx(cfg["velocidade"])


def test_pula_e_volta_ao_chao(cfg):
    angel = angel_no_chao(cfg)
    y_chao = angel.rect.y
    angel.atualizar(DT, Comandos(pulo_apertado=True, pulo_segurado=True), [CHAO])
    assert angel.estado == Estado.PULANDO
    simular(angel, Comandos(pulo_segurado=True), [CHAO], 10)
    assert angel.rect.y < y_chao
    simular(angel, Comandos(), [CHAO], 120)
    assert angel.no_chao
    assert angel.rect.y == y_chao


def altura_do_pulo(cfg, quadros_segurando):
    angel = angel_no_chao(cfg)
    y_chao = angel.rect.y
    angel.atualizar(DT, Comandos(pulo_apertado=True, pulo_segurado=True), [CHAO])
    menor_y = angel.rect.y
    for i in range(120):
        angel.atualizar(DT, Comandos(pulo_segurado=i < quadros_segurando), [CHAO])
        menor_y = min(menor_y, angel.rect.y)
    return y_chao - menor_y


def test_segurar_o_pulo_pula_mais_alto(cfg):
    assert altura_do_pulo(cfg, 60) > altura_do_pulo(cfg, 3) * 1.5


def test_nao_pula_no_ar(cfg):
    angel = Angel(cfg, (100, 0))
    simular(angel, Comandos(), [], 30)  # caindo há meio segundo, sem chão
    angel.atualizar(DT, Comandos(pulo_apertado=True, pulo_segurado=True), [])
    assert angel.vel_y > 0  # continua caindo


def test_tempo_de_coiote(cfg):
    """Logo depois de sair da borda ainda dá para pular."""
    borda = pygame.Rect(0, 500, 100, 40)
    angel = Angel(cfg, (100 - cfg["largura"] - 2, 500 - cfg["altura"] - 2))
    simular(angel, Comandos(), [borda], 20)
    assert angel.no_chao
    # anda até sair da borda
    while angel.no_chao:
        angel.atualizar(DT, Comandos(direita=True), [borda])
    angel.atualizar(DT, Comandos(direita=True, pulo_apertado=True, pulo_segurado=True), [borda])
    assert angel.vel_y < 0


def test_bate_na_parede(cfg):
    angel = angel_no_chao(cfg)
    parede = pygame.Rect(angel.rect.right + 20, 300, 40, 200)
    simular(angel, Comandos(direita=True), [CHAO, parede], 60)
    assert angel.rect.right == parede.left


def test_bate_a_cabeca_no_teto(cfg):
    angel = angel_no_chao(cfg)
    teto = pygame.Rect(0, angel.rect.top - 30, 960, 20)
    angel.atualizar(DT, Comandos(pulo_apertado=True, pulo_segurado=True), [CHAO, teto])
    simular(angel, Comandos(pulo_segurado=True), [CHAO, teto], 10)
    assert angel.rect.top >= teto.bottom


def test_reiniciar_volta_ao_inicio(cfg):
    angel = Angel(cfg, (80, 380))
    simular(angel, Comandos(direita=True), [CHAO], 60)
    angel.reiniciar()
    assert (angel.rect.x, angel.rect.y) == (80, 380)
    assert angel.vel_x == angel.vel_y == 0
