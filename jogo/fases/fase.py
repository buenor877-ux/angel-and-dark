"""Dados de uma fase: plataformas e ponto de início.

Na Parte 1 a fase vem de config/fase_teste.toml. Quando o Tiled entrar,
só a forma de carregar muda; o resto do jogo continua usando esta classe.
"""

import pygame


class Fase:
    def __init__(self, dados: dict, altura_tela: int):
        self.inicio = tuple(dados["inicio"])
        self.plataformas = [pygame.Rect(*p) for p in dados["plataformas"]]
        self.limite_queda = altura_tela + 100  # passou disto, caiu para fora

    def caiu_para_fora(self, rect: pygame.Rect) -> bool:
        return rect.top > self.limite_queda

    def desenhar(self, tela: pygame.Surface, cor: tuple) -> None:
        for p in self.plataformas:
            pygame.draw.rect(tela, cor, p)
