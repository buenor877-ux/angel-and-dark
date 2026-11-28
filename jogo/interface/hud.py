"""HUD: o que fica fixo na tela durante a fase (corações, vidas, nome da fase).

HUD vem de "heads-up display", o painel que o jogador vê por cima do jogo.
"""

from pathlib import Path

import pygame

RAIZ = Path(__file__).resolve().parents[2]


class Hud:
    def __init__(self, cfg: dict, cores: dict):
        """cfg vem de config/jogo.toml, bloco [hud]."""
        self.cores = cores
        folha = pygame.image.load(str(RAIZ / cfg["imagem"])).convert_alpha()
        t, esc = cfg["tamanho_bloco"], cfg["escala"]
        colunas = folha.get_width() // t

        def icone(indice: int) -> pygame.Surface:
            x, y = (indice % colunas) * t, (indice // colunas) * t
            return pygame.transform.scale(folha.subsurface((x, y, t, t)), (t * esc, t * esc))

        self.coracao_cheio = icone(cfg["coracao_cheio"])
        self.coracao_vazio = icone(cfg["coracao_vazio"])
        self.fonte = pygame.font.Font(None, 30)
        self.fonte_pequena = pygame.font.Font(None, 22)

    def desenhar(self, tela: pygame.Surface, vida, titulo: str, ajuda: str) -> None:
        x, y = 12, 10
        lado = self.coracao_cheio.get_width()
        for i in range(vida.max_coracoes):
            icone = self.coracao_cheio if i < vida.coracoes else self.coracao_vazio
            tela.blit(icone, (x + i * (lado + 4), y))

        texto_vidas = self.fonte.render(
            f"Vidas: {vida.vidas}", True, self.cores["texto_fase"], self.cores["caixa"]
        )
        tela.blit(texto_vidas, (x + vida.max_coracoes * (lado + 4) + 12, y + 6))

        for i, linha in enumerate((titulo, ajuda)):
            img = self.fonte_pequena.render(
                linha, True, self.cores["texto_fase"], self.cores["caixa"]
            )
            tela.blit(img, (x, y + lado + 8 + i * 20))
