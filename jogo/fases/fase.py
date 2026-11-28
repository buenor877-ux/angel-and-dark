"""Dados de uma fase: tamanho, plataformas, início e chegada.

Por enquanto a fase vem de config/fase_teste.toml. Quando o Tiled entrar,
só a forma de carregar muda; o resto do jogo continua usando esta classe.
"""

import pygame

ESPESSURA_PAREDE = 100


class Fase:
    def __init__(self, dados: dict):
        self.largura, self.altura = dados["tamanho"]
        self.inicio = tuple(dados["inicio"])
        self.chegada = pygame.Rect(*dados["chegada"])
        self.plataformas = [pygame.Rect(*p) for p in dados["plataformas"]]
        # Paredes invisíveis nas bordas: o personagem não sai do mundo pelos lados.
        self.paredes = [
            pygame.Rect(-ESPESSURA_PAREDE, -self.altura, ESPESSURA_PAREDE, self.altura * 3),
            pygame.Rect(self.largura, -self.altura, ESPESSURA_PAREDE, self.altura * 3),
        ]
        self.limite_queda = self.altura + 100  # passou disto, caiu para fora

    @property
    def tamanho(self) -> tuple[int, int]:
        return self.largura, self.altura

    @property
    def solidos(self) -> list[pygame.Rect]:
        """Tudo em que o personagem bate."""
        return self.plataformas + self.paredes

    def caiu_para_fora(self, rect: pygame.Rect) -> bool:
        return rect.top > self.limite_queda

    def chegou(self, rect: pygame.Rect) -> bool:
        return rect.colliderect(self.chegada)

    def desenhar(self, tela: pygame.Surface, cores: dict, camera) -> None:
        area_visivel = pygame.Rect(round(camera.x), round(camera.y), *tela.get_size())
        for p in self.plataformas:
            if p.colliderect(area_visivel):  # só desenha o que aparece na tela
                pygame.draw.rect(tela, cores["plataforma"], camera.na_tela(p))
        self._desenhar_bandeira(tela, cores["destaque"], camera)

    def _desenhar_bandeira(self, tela: pygame.Surface, cor: tuple, camera) -> None:
        mastro = camera.na_tela(pygame.Rect(self.chegada.x, self.chegada.y, 4, self.chegada.h))
        pygame.draw.rect(tela, cor, mastro)
        x, y = mastro.right, mastro.top
        pygame.draw.polygon(tela, cor, [(x, y), (x + 30, y + 12), (x, y + 24)])
