"""Cena de teste: o personagem escolhido numa fase maior que a tela, com câmera."""

import pygame

from jogo.cenas.cena import Cena
from jogo.fases.camera import Camera
from jogo.fases.fase import Fase
from jogo.nucleo import config
from jogo.nucleo.controles import ler_comandos

TEMPO_TELA_CONCLUIDA = 2.0  # segundos mostrando "Fase concluída!" antes de voltar


class CenaTeste(Cena):
    def __init__(self, jogo, classe_personagem):
        super().__init__(jogo)
        self.cores = {k: tuple(v) for k, v in jogo.cfg["cores"].items()}
        janela = jogo.cfg["janela"]
        self.fase = Fase(config.carregar("fase_teste"))
        self.personagem = classe_personagem.criar(self.fase.inicio)
        self.camera = Camera(
            jogo.cfg["camera"], (janela["largura"], janela["altura"]), self.fase.tamanho
        )
        self.camera.centralizar(self.personagem.rect)
        self.quedas = 0
        self.concluida = False
        self.tempo_concluida = 0.0
        self.fonte = pygame.font.Font(None, 24)
        self.fonte_grande = pygame.font.Font(None, 64)

    def atualizar(self, dt: float, eventos: list[pygame.event.Event]) -> None:
        if any(e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE for e in eventos):
            self.jogo.ir_para_escolha(type(self.personagem))
            return

        if self.concluida:
            self.tempo_concluida += dt
            if self.tempo_concluida >= TEMPO_TELA_CONCLUIDA:
                self.jogo.ir_para_escolha(type(self.personagem))
            return

        p = self.personagem
        p.atualizar(dt, ler_comandos(eventos), self.fase.solidos)
        if self.fase.caiu_para_fora(p.rect):
            p.reiniciar()
            self.quedas += 1
            self.camera.centralizar(p.rect, p.olhando)
        elif self.fase.chegou(p.rect):
            self.concluida = True
        self.camera.atualizar(dt, p.rect, p.olhando, p.no_chao)

    def desenhar(self, tela: pygame.Surface) -> None:
        tela.fill(self.cores["fundo"])
        self.fase.desenhar(tela, self.cores, self.camera)
        self.personagem.desenhar(tela, self.camera)

        # O texto fica fixo na tela: não usa a câmera.
        linhas = [
            f"Fase de teste - {self.personagem.nome}",
            "Setas/A D: andar   Espaço/W: pular   Esc: trocar personagem",
            f"Estado: {self.personagem.estado.value}   Quedas: {self.quedas}",
        ]
        for i, texto in enumerate(linhas):
            imagem = self.fonte.render(texto, True, self.cores["texto"])
            tela.blit(imagem, (12, 10 + i * 22))

        if self.concluida:
            imagem = self.fonte_grande.render("Fase concluída!", True, self.cores["destaque"])
            tela.blit(imagem, imagem.get_rect(center=tela.get_rect().center))
