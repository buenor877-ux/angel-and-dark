"""Cena da Parte 1: a Angel numa fase de teste."""

import pygame

from jogo.cenas.cena import Cena
from jogo.fases.fase import Fase
from jogo.nucleo import config
from jogo.nucleo.controles import ler_comandos
from jogo.personagens.angel import Angel


class CenaTeste(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.cores = {k: tuple(v) for k, v in jogo.cfg["cores"].items()}
        self.fase = Fase(config.carregar("fase_teste"), jogo.cfg["janela"]["altura"])
        self.angel = Angel(config.carregar("personagens")["angel"], self.fase.inicio)
        self.quedas = 0
        self.fonte = pygame.font.Font(None, 24)

    def atualizar(self, dt: float, eventos: list[pygame.event.Event]) -> None:
        comandos = ler_comandos(eventos)
        self.angel.atualizar(dt, comandos, self.fase.plataformas)
        if self.fase.caiu_para_fora(self.angel.rect):
            self.angel.reiniciar()
            self.quedas += 1

    def desenhar(self, tela: pygame.Surface) -> None:
        tela.fill(self.cores["fundo"])
        self.fase.desenhar(tela, self.cores["plataforma"])
        self.angel.desenhar(tela)

        linhas = [
            "Parte 1 - fase de teste",
            "Setas/A D: andar   Espaco/W: pular   Esc: sair",
            f"Estado: {self.angel.estado.value}   Quedas: {self.quedas}",
        ]
        for i, texto in enumerate(linhas):
            imagem = self.fonte.render(texto, True, self.cores["texto"])
            tela.blit(imagem, (12, 10 + i * 22))
