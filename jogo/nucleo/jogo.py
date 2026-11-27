"""O loop principal: lê eventos, atualiza a cena atual e desenha, 60 vezes por segundo."""

import asyncio
import sys

import pygame

from jogo.cenas.cena_teste import CenaTeste
from jogo.nucleo import config


class Jogo:
    def __init__(self):
        pygame.init()
        self.cfg = config.carregar("jogo")
        janela = self.cfg["janela"]
        self.tela = pygame.display.set_mode((janela["largura"], janela["altura"]))
        pygame.display.set_caption(janela["titulo"])
        self.relogio = pygame.time.Clock()
        self.fps = janela["fps"]
        self.rodando = True
        self.cena = CenaTeste(self)

    async def rodar(self, max_quadros: int | None = None) -> None:
        quadros = 0
        while self.rodando:
            # dt = segundos desde o último quadro. Limitado para um travamento
            # não fazer a Angel "teletransportar" atravessando o chão.
            dt = min(self.relogio.tick(self.fps) / 1000, 1 / 30)

            eventos = pygame.event.get()
            for e in eventos:
                if e.type == pygame.QUIT:
                    self.rodando = False
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    # No navegador não existe "fechar o programa"; Esc só vale no PC.
                    if sys.platform != "emscripten":
                        self.rodando = False

            self.cena.atualizar(dt, eventos)
            self.cena.desenhar(self.tela)
            pygame.display.flip()

            quadros += 1
            if max_quadros is not None and quadros >= max_quadros:
                self.rodando = False

            # Devolve o controle ao navegador a cada quadro (exigência do pygbag).
            await asyncio.sleep(0)

        pygame.quit()
