"""O loop principal e o "gerente" das cenas.

A cada quadro: lê eventos, atualiza a cena atual e desenha, 60 vezes por segundo.
As cenas não se conhecem: pedem ao Jogo para trocar de tela.
"""

import asyncio
import sys

import pygame

from jogo.cenas.cena_escolha import OPCOES, CenaEscolha
from jogo.cenas.cena_fase import CenaFase
from jogo.nucleo import config

NO_NAVEGADOR = sys.platform == "emscripten"


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
        self.cena = CenaEscolha(self)

    # ---------- troca de cenas ----------

    def iniciar_fase(self, classe_personagem) -> None:
        self.cena = CenaFase(self, classe_personagem, self.cfg["mapa"]["fase_inicial"])

    def ir_para_escolha(self, ultimo_personagem=None) -> None:
        """Volta à escolha, já marcando o último personagem usado."""
        indice = OPCOES.index(ultimo_personagem) if ultimo_personagem in OPCOES else 0
        self.cena = CenaEscolha(self, selecionado=indice)

    def sair(self) -> None:
        # No navegador não existe "fechar o programa".
        if not NO_NAVEGADOR:
            self.rodando = False

    # ---------- loop ----------

    async def rodar(self, max_quadros: int | None = None) -> None:
        quadros = 0
        while self.rodando:
            # dt = segundos desde o último quadro. Limitado para um travamento
            # não fazer o personagem atravessar o chão.
            dt = min(self.relogio.tick(self.fps) / 1000, 1 / 30)

            eventos = pygame.event.get()
            if any(e.type == pygame.QUIT for e in eventos):
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
