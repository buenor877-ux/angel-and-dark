"""Testes da fase de teste e das configurações."""

import pygame

from jogo.fases.fase import Fase
from jogo.nucleo import config


def test_configs_carregam():
    assert config.carregar("jogo")["janela"]["fps"] == 60
    assert "angel" in config.carregar("personagens")


def test_fase_teste_tem_chao_e_inicio_valido():
    fase = Fase(config.carregar("fase_teste"), altura_tela=540)
    assert len(fase.plataformas) >= 2
    x, y = fase.inicio
    assert 0 <= x < 960 and 0 <= y < 540


def test_detecta_queda_para_fora():
    fase = Fase(config.carregar("fase_teste"), altura_tela=540)
    assert not fase.caiu_para_fora(pygame.Rect(100, 400, 32, 48))
    assert fase.caiu_para_fora(pygame.Rect(100, 700, 32, 48))
