"""Cena de uma fase: o personagem escolhido numa fase feita no Tiled, com câmera e fundo."""

import pygame

from jogo.cenas.cena import Cena
from jogo.fases import carregador_fases
from jogo.fases.camera import Camera
from jogo.fases.fundo import Fundo
from jogo.nucleo import config
from jogo.nucleo.controles import ler_comandos

TEMPO_TELA_CONCLUIDA = 2.0  # segundos mostrando "Fase concluída!" antes de voltar


class CenaFase(Cena):
    def __init__(self, jogo, classe_personagem, nome_fase: str, fase=None):
        """`fase` pronta é opcional (os testes usam fases simples, sem Tiled)."""
        super().__init__(jogo)
        self.cores = {k: tuple(v) for k, v in jogo.cfg["cores"].items()}
        janela = jogo.cfg["janela"]
        tela = (janela["largura"], janela["altura"])

        self.fase = fase or carregador_fases.carregar(nome_fase, jogo.cfg["mapa"]["escala"])
        self.personagem = classe_personagem.criar((0, 0))
        pes_x, pes_y = self.fase.inicio
        self.personagem.inicio = (pes_x, pes_y - self.personagem.rect.height)
        self.personagem.reiniciar()

        self.camera = Camera(jogo.cfg["camera"], tela, self.fase.tamanho)
        self.camera.centralizar(self.personagem.rect)

        cfg_fase = config.carregar("fases").get(nome_fase, {})
        cam_y_max = self.fase.altura - tela[1]
        self.fundo = Fundo(cfg_fase["fundo"], tela, cam_y_max) if "fundo" in cfg_fase else None
        self.titulo = cfg_fase.get("nome", self.fase.nome or nome_fase)

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
        if self.fundo:
            self.fundo.desenhar(tela, self.camera)
        else:
            tela.fill(self.cores["fundo"])
        self.fase.desenhar(tela, self.cores, self.camera)
        self.personagem.desenhar(tela, self.camera)

        # O texto fica fixo na tela: não usa a câmera.
        linhas = [
            f"{self.titulo} - {self.personagem.nome}",
            "Setas/A D: andar   Espaço/W: pular   Esc: trocar personagem",
            f"Estado: {self.personagem.estado.value}   Quedas: {self.quedas}",
        ]
        for i, texto in enumerate(linhas):
            imagem = self.fonte.render(texto, True, self.cores["texto_fase"], self.cores["caixa"])
            tela.blit(imagem, (12, 10 + i * 22))

        if self.concluida:
            imagem = self.fonte_grande.render(
                "Fase concluída!", True, self.cores["destaque"], self.cores["caixa"]
            )
            tela.blit(imagem, imagem.get_rect(center=tela.get_rect().center))
