"""Modelo de toda cena (tela) do jogo: menu, fase, pausa, game over...

Cada cena sabe se atualizar e se desenhar. O Jogo só chama a cena atual.
"""

import pygame


class Cena:
    def __init__(self, jogo):
        self.jogo = jogo

    def atualizar(self, dt: float, eventos: list[pygame.event.Event]) -> None:
        pass

    def desenhar(self, tela: pygame.Surface) -> None:
        pass
