"""Fundo com profundidade (parallax).

O fundo anda mais devagar que a fase: `fator = 0.3` quer dizer que, quando a câmera
anda 100 px, o fundo anda 30 px. Isso dá a sensação de que ele está longe.
"""

from pathlib import Path

import pygame

RAIZ = Path(__file__).resolve().parents[2]


class Fundo:
    def __init__(self, cfg: dict, tamanho_tela: tuple[int, int], cam_y_max: float):
        """cfg vem de config/fases.toml, bloco [<fase>.fundo]."""
        self.cfg = cfg
        self.largura_tela, self.altura_tela = tamanho_tela
        self.cam_y_max = cam_y_max  # altura da câmera no ponto mais baixo da fase

        folha = pygame.image.load(str(RAIZ / cfg["imagem"])).convert_alpha()
        t, esc = cfg["tamanho_bloco"], cfg["escala"]

        def bloco(indice: int) -> pygame.Surface:
            colunas = folha.get_width() // t
            x, y = (indice % colunas) * t, (indice // colunas) * t
            return pygame.transform.scale(folha.subsurface((x, y, t, t)), (t * esc, t * esc))

        # A faixa (morros e árvores) vira uma imagem só, repetida na horizontal.
        pedacos = [bloco(i) for i in cfg["faixa"]]
        lado = t * esc
        # Sem transparência: os blocos de fundo da Kenney são 100% opacos, e
        # misturar transparência à toa custava ~3 ms por quadro no navegador.
        self.faixa = pygame.Surface((lado * len(pedacos), lado))
        for i, p in enumerate(pedacos):
            self.faixa.blit(p, (i * lado, 0))
        # Céu e chão do fundo: cores tiradas dos próprios blocos da Kenney.
        self.cor_ceu = bloco(cfg["ceu"]).get_at((0, 0))
        self.cor_base = bloco(cfg["base"]).get_at((0, 0))

    def desenhar(self, tela: pygame.Surface, camera) -> None:
        # Vertical: quando a câmera sobe, o fundo desce devagar (fator_y pequeno).
        base_faixa = (
            self.altura_tela * self.cfg["altura_horizonte"]
            - (camera.y - self.cam_y_max) * self.cfg["fator_y"]
        )
        topo_faixa = round(base_faixa - self.faixa.get_height())

        tela.fill(self.cor_ceu)
        pygame.draw.rect(
            tela,
            self.cor_base,
            (0, topo_faixa + self.faixa.get_height(), self.largura_tela, self.altura_tela),
        )

        # Horizontal: repete a faixa, deslocada pela câmera vezes o fator.
        largura = self.faixa.get_width()
        x = -round(camera.x * self.cfg["fator_x"]) % largura - largura
        while x < self.largura_tela:
            tela.blit(self.faixa, (x, topo_faixa))
            x += largura
