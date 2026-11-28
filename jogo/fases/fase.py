"""Uma fase: tamanho, colisão, início, chegada e o desenho do cenário.

A fase não sabe de onde veio (Tiled, TOML, teste). Quem cria é o carregador_fases.py.
"""

import pygame

ESPESSURA_PAREDE = 100


class Fase:
    def __init__(
        self,
        largura: int,
        altura: int,
        inicio: tuple[int, int],
        chegada: pygame.Rect,
        plataformas: list[pygame.Rect],
        superficies: list[pygame.Rect] | None = None,
        desenho: pygame.Surface | None = None,
        nome: str = "",
    ):
        self.largura, self.altura = largura, altura
        self.inicio = inicio  # posição dos PÉS do personagem no começo
        self.chegada = chegada
        self.plataformas = plataformas  # retângulos sólidos (já juntados)
        # Superfícies = topos onde dá para pisar. Usadas para conferir o alcance.
        self.superficies = superficies if superficies is not None else plataformas
        self.desenho = desenho  # cenário inteiro já desenhado (vem do Tiled)
        self.nome = nome
        # Paredes invisíveis nas bordas: o personagem não sai do mundo pelos lados.
        self.paredes = [
            pygame.Rect(-ESPESSURA_PAREDE, -altura, ESPESSURA_PAREDE, altura * 3),
            pygame.Rect(largura, -altura, ESPESSURA_PAREDE, altura * 3),
        ]
        self.limite_queda = altura + 100  # passou disto, caiu para fora

    @classmethod
    def de_dados(cls, dados: dict) -> "Fase":
        """Fase simples a partir de um dicionário (usada nos testes)."""
        largura, altura = dados["tamanho"]
        return cls(
            largura,
            altura,
            tuple(dados["inicio"]),
            pygame.Rect(*dados["chegada"]),
            [pygame.Rect(*p) for p in dados["plataformas"]],
        )

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
        if self.desenho is not None:
            # Copia só o pedaço do cenário que a câmera está vendo.
            area = pygame.Rect(round(camera.x), round(camera.y), *tela.get_size())
            tela.blit(self.desenho, (0, 0), area)
            return
        # Sem desenho (fases de teste): retângulos simples.
        for p in self.plataformas:
            pygame.draw.rect(tela, cores["plataforma"], camera.na_tela(p))
        pygame.draw.rect(tela, cores["destaque"], camera.na_tela(self.chegada))
