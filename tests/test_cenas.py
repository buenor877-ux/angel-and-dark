"""Troca de telas: escolha de personagem e volta com Esc."""

import pygame

from jogo.cenas.cena_escolha import CenaEscolha
from jogo.cenas.cena_fase import CenaFase
from jogo.nucleo import config
from jogo.personagens.angel import Angel
from jogo.personagens.dark import Dark


class JogoFalso:
    """Faz o papel do Jogo e anota o que as cenas pediram."""

    def __init__(self):
        self.cfg = config.carregar("jogo")
        self.pedidos = []

    def iniciar_fase(self, classe):
        self.pedidos.append(("fase", classe))

    def ir_para_escolha(self, ultimo=None):
        self.pedidos.append(("escolha", ultimo))

    def sair(self):
        self.pedidos.append(("sair", None))


def tecla(key):
    return pygame.event.Event(pygame.KEYDOWN, key=key)


def test_escolha_comeca_na_angel_e_troca_com_as_setas():
    cena = CenaEscolha(JogoFalso())
    assert cena.personagem_escolhido is Angel
    cena.atualizar(0, [tecla(pygame.K_RIGHT)])
    assert cena.personagem_escolhido is Dark
    cena.atualizar(0, [tecla(pygame.K_RIGHT)])  # dá a volta
    assert cena.personagem_escolhido is Angel
    cena.atualizar(0, [tecla(pygame.K_a)])
    assert cena.personagem_escolhido is Dark


def test_enter_inicia_a_fase_com_o_escolhido():
    jogo = JogoFalso()
    cena = CenaEscolha(jogo)
    cena.atualizar(0, [tecla(pygame.K_d), tecla(pygame.K_RETURN)])
    assert jogo.pedidos == [("fase", Dark)]


def test_esc_na_escolha_pede_para_sair():
    jogo = JogoFalso()
    CenaEscolha(jogo).atualizar(0, [tecla(pygame.K_ESCAPE)])
    assert jogo.pedidos == [("sair", None)]


def test_esc_na_fase_volta_para_a_escolha():
    jogo = JogoFalso()
    cena = CenaFase(jogo, Dark, "01_floresta")
    assert cena.personagem.nome == "Dark"
    cena.atualizar(1 / 60, [tecla(pygame.K_ESCAPE)])
    assert jogo.pedidos == [("escolha", Dark)]


def test_chegar_na_bandeira_conclui_e_volta_depois_de_2_segundos():
    jogo = JogoFalso()
    cena = CenaFase(jogo, Angel, "01_floresta")
    cena.personagem.rect = cena.fase.chegada.copy()
    cena.personagem.x, cena.personagem.y = float(cena.fase.chegada.x), float(cena.fase.chegada.y)
    cena.atualizar(1 / 60, [])
    assert cena.concluida
    assert jogo.pedidos == []
    for _ in range(130):  # pouco mais de 2 segundos
        cena.atualizar(1 / 60, [])
    assert jogo.pedidos[0] == ("escolha", Angel)


def test_fase_desenha_sem_erro():
    tela = pygame.Surface((960, 540))
    cena = CenaFase(JogoFalso(), Dark, "01_floresta")
    cena.desenhar(tela)
    cena.concluida = True
    cena.desenhar(tela)


def test_personagem_comeca_de_pe_no_inicio_da_fase():
    cena = CenaFase(JogoFalso(), Angel, "01_floresta")
    for _ in range(30):
        cena.atualizar(1 / 60, [])
    assert cena.personagem.no_chao
    assert abs(cena.personagem.rect.bottom - cena.fase.inicio[1]) <= 4  # pousou logo abaixo
    assert cena.quedas == 0


def test_escolha_desenha_sem_erro():
    tela = pygame.Surface((960, 540))
    CenaEscolha(JogoFalso()).desenhar(tela)
