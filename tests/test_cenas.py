"""Troca de telas: escolha de personagem e volta com Esc."""

import pygame

from jogo.cenas.cena_escolha import CenaEscolha
from jogo.cenas.cena_teste import CenaTeste
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
    cena = CenaTeste(jogo, Dark)
    assert cena.personagem.nome == "Dark"
    cena.atualizar(1 / 60, [tecla(pygame.K_ESCAPE)])
    assert jogo.pedidos == [("escolha", Dark)]


def test_escolha_desenha_sem_erro():
    tela = pygame.Surface((960, 540))
    CenaEscolha(JogoFalso()).desenhar(tela)
