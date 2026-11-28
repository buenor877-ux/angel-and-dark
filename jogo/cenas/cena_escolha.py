"""Tela de escolha de personagem: Angel ou Dark."""

import sys

import pygame

from jogo.cenas.cena import Cena
from jogo.personagens.angel import Angel
from jogo.personagens.dark import Dark

OPCOES = [Angel, Dark]

# No navegador não existe "fechar o programa", então a dica do Esc some.
AJUDA = "Setas/A D: escolher   Enter/Espaço: jogar"
if sys.platform != "emscripten":
    AJUDA += "   Esc: sair"

TECLAS_ESQUERDA = (pygame.K_LEFT, pygame.K_a)
TECLAS_DIREITA = (pygame.K_RIGHT, pygame.K_d)
TECLAS_CONFIRMAR = (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE)


class CenaEscolha(Cena):
    def __init__(self, jogo, selecionado: int = 0):
        super().__init__(jogo)
        self.selecionado = selecionado
        self.cores = {k: tuple(v) for k, v in jogo.cfg["cores"].items()}
        self.fonte_titulo = pygame.font.Font(None, 48)
        self.fonte = pygame.font.Font(None, 28)
        self.amostras = [classe.criar((0, 0)) for classe in OPCOES]  # só para nome e cor

    @property
    def personagem_escolhido(self):
        return OPCOES[self.selecionado]

    def atualizar(self, dt: float, eventos: list[pygame.event.Event]) -> None:
        for e in eventos:
            if e.type != pygame.KEYDOWN:
                continue
            if e.key in TECLAS_ESQUERDA:
                self.selecionado = (self.selecionado - 1) % len(OPCOES)
            elif e.key in TECLAS_DIREITA:
                self.selecionado = (self.selecionado + 1) % len(OPCOES)
            elif e.key in TECLAS_CONFIRMAR:
                self.jogo.iniciar_fase(self.personagem_escolhido)
                return
            elif e.key == pygame.K_ESCAPE:
                self.jogo.sair()
                return

    def desenhar(self, tela: pygame.Surface) -> None:
        tela.fill(self.cores["fundo"])
        largura, altura = tela.get_size()
        self._texto(tela, self.fonte_titulo, "Escolha seu personagem", (largura // 2, 90))

        for i, pers in enumerate(self.amostras):
            centro_x = largura // 2 + (i * 2 - 1) * 160  # um à esquerda, outro à direita
            quadro = pygame.Rect(0, 0, 64, 96)
            quadro.center = (centro_x, altura // 2)
            pygame.draw.rect(tela, pers.cor, quadro)
            if i == self.selecionado:
                pygame.draw.rect(tela, self.cores["destaque"], quadro.inflate(24, 24), width=4)
            self._texto(tela, self.fonte, pers.nome, (centro_x, quadro.bottom + 36))

        self._texto(
            tela,
            self.fonte,
            AJUDA,
            (largura // 2, altura - 50),
        )

    def _texto(self, tela, fonte, texto, centro) -> None:
        imagem = fonte.render(texto, True, self.cores["texto"])
        tela.blit(imagem, imagem.get_rect(center=centro))
