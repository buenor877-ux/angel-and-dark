"""Cena de teste: o personagem escolhido numa fase de teste."""

import pygame

from jogo.cenas.cena import Cena
from jogo.fases.fase import Fase
from jogo.nucleo import config
from jogo.nucleo.controles import ler_comandos


class CenaTeste(Cena):
    def __init__(self, jogo, classe_personagem):
        super().__init__(jogo)
        self.cores = {k: tuple(v) for k, v in jogo.cfg["cores"].items()}
        self.fase = Fase(config.carregar("fase_teste"), jogo.cfg["janela"]["altura"])
        self.personagem = classe_personagem.criar(self.fase.inicio)
        self.quedas = 0
        self.fonte = pygame.font.Font(None, 24)

    def atualizar(self, dt: float, eventos: list[pygame.event.Event]) -> None:
        if any(e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE for e in eventos):
            self.jogo.ir_para_escolha(type(self.personagem))
            return

        comandos = ler_comandos(eventos)
        self.personagem.atualizar(dt, comandos, self.fase.plataformas)
        if self.fase.caiu_para_fora(self.personagem.rect):
            self.personagem.reiniciar()
            self.quedas += 1

    def desenhar(self, tela: pygame.Surface) -> None:
        tela.fill(self.cores["fundo"])
        self.fase.desenhar(tela, self.cores["plataforma"])
        self.personagem.desenhar(tela)

        linhas = [
            f"Fase de teste - {self.personagem.nome}",
            "Setas/A D: andar   Espaco/W: pular   Esc: trocar personagem",
            f"Estado: {self.personagem.estado.value}   Quedas: {self.quedas}",
        ]
        for i, texto in enumerate(linhas):
            imagem = self.fonte.render(texto, True, self.cores["texto"])
            tela.blit(imagem, (12, 10 + i * 22))
