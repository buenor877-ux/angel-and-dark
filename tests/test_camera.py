"""Testes da câmera: suave, olha à frente, não acompanha cada pulo, não sai do mundo."""

import pygame

from jogo.fases.camera import Camera
from jogo.nucleo import config

DT = 1 / 60
TELA = (960, 540)
MUNDO = (2880, 1080)


def camera():
    return Camera(config.carregar("jogo")["camera"], TELA, MUNDO)


def pers(x, y_pes):
    """Retângulo do personagem com os pés em `y_pes`."""
    return pygame.Rect(x, y_pes - 48, 32, 48)


def rodar(cam, rect, olhando=1, no_chao=True, quadros=120):
    for _ in range(quadros):
        cam.atualizar(DT, rect, olhando, no_chao)


def test_nao_mostra_fora_do_mundo():
    cam = camera()
    cam.centralizar(pers(10, 1040))  # bem no canto esquerdo de baixo
    assert cam.x == 0
    assert cam.y == MUNDO[1] - TELA[1]
    cam.centralizar(pers(2870, 1040))  # canto direito
    assert cam.x == MUNDO[0] - TELA[0]


def test_segue_suave_e_nao_pula_de_uma_vez():
    cam = camera()
    cam.centralizar(pers(500, 1040))
    x0 = cam.x
    alvo = pers(1500, 1040)
    cam.atualizar(DT, alvo, 1, True)
    assert x0 < cam.x < x0 + 200  # andou um pouco, não tudo
    rodar(cam, alvo)
    assert abs(cam.na_tela(alvo).centerx - (TELA[0] / 2 - 120)) < 2  # chegou


def test_olha_para_o_lado_em_que_anda():
    cam = camera()
    r = pers(1400, 1040)
    rodar(cam, r, olhando=1)
    na_tela_direita = cam.na_tela(r).centerx
    rodar(cam, r, olhando=-1)
    na_tela_esquerda = cam.na_tela(r).centerx
    assert na_tela_direita < TELA[0] / 2 < na_tela_esquerda  # sobra espaço à frente


def test_nao_acompanha_o_pulo():
    cam = camera()
    cam.centralizar(pers(1400, 680))  # pisando no alto, longe das bordas do mundo
    y0 = cam.y
    for altura in range(0, 100, 10):  # sobe 100 px no ar...
        cam.atualizar(DT, pers(1400, 680 - altura), 1, no_chao=False)
    for altura in range(100, 0, -10):  # ...e desce
        cam.atualizar(DT, pers(1400, 680 - altura), 1, no_chao=False)
    assert abs(cam.y - y0) < 1


def test_sobe_ao_pisar_mais_alto():
    cam = camera()
    cam.centralizar(pers(1400, 860))
    y0 = cam.y
    rodar(cam, pers(1400, 680), no_chao=True)
    assert cam.y < y0 - 150


def test_desce_ao_cair_perto_da_borda_de_baixo():
    cam = camera()
    cam.centralizar(pers(1400, 680))
    y0 = cam.y
    rodar(cam, pers(1400, 1000), no_chao=False, quadros=60)  # caindo, sem pisar
    assert cam.y > y0 + 100
