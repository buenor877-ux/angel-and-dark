"""Projétil: qualquer coisa que voa sozinha e machuca quem acerta.

Hoje é a semente da planta. Depois, sem mudar esta classe, vira a flecha do
arqueiro (com gravidade, em arco), a bola de fogo da salamandra e o que mais vier.
O que muda de um para outro são só os números, que vêm da config de quem atira.

Regras de todo projétil:
- anda em linha reta (ou em arco, se tiver gravidade);
- some ao bater num bloco sólido (parede, chão, teto);
- some ao acertar o personagem (quem decide o dano é a cena);
- some sozinho depois de percorrer o `alcance` (não fica voando para sempre).
"""

import pygame


class Projetil:
    def __init__(
        self,
        centro: tuple[float, float],
        velocidade: tuple[float, float],
        tamanho: tuple[int, int],
        cor: tuple[int, int, int],
        gravidade: float = 0.0,
        alcance: float = 1000.0,
    ):
        self.rect = pygame.Rect(0, 0, *tamanho)
        self.rect.center = (round(centro[0]), round(centro[1]))
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        self.vel_x, self.vel_y = velocidade
        self.gravidade = gravidade
        self.alcance = alcance
        self.cor = cor
        self.percorrido = 0.0
        self.ativo = True

    @classmethod
    def de_config(cls, cfg: dict, centro: tuple[float, float], direcao: int) -> "Projetil":
        """Cria a partir de um bloco da config (ex.: [planta.semente]).

        `direcao` é 1 (direita) ou -1 (esquerda). `velocidade_y` é opcional:
        negativo sai para cima, o que com gravidade faz um arco.
        """
        return cls(
            centro,
            (direcao * cfg["velocidade"], cfg.get("velocidade_y", 0.0)),
            (cfg["largura"], cfg["altura"]),
            tuple(cfg["cor"]),
            gravidade=cfg.get("gravidade", 0.0),
            alcance=cfg["alcance"],
        )

    def atualizar(self, dt: float, solidos: list[pygame.Rect]) -> None:
        if not self.ativo:
            return
        self.vel_y += self.gravidade * dt
        dx, dy = self.vel_x * dt, self.vel_y * dt
        self.x += dx
        self.y += dy
        self.rect.topleft = (round(self.x), round(self.y))
        self.percorrido += (dx * dx + dy * dy) ** 0.5
        if self.rect.collidelist(solidos) != -1 or self.percorrido >= self.alcance:
            self.ativo = False

    def acertou(self, rect: pygame.Rect) -> bool:
        """Encostou em `rect`? Se sim, o projétil some (acertou uma vez só)."""
        if self.ativo and self.rect.colliderect(rect):
            self.ativo = False
            return True
        return False

    def desenhar(self, tela: pygame.Surface, camera) -> None:
        if not self.ativo:
            return
        rect = camera.na_tela(self.rect)
        pygame.draw.ellipse(tela, self.cor, rect)
        # Um pontinho escuro: a semente tem "cara" e não some no fundo claro.
        pygame.draw.ellipse(tela, (40, 30, 20), rect.inflate(-rect.width // 2, -rect.height // 2))
