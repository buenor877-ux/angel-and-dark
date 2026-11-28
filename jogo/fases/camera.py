"""Câmera que segue o personagem numa fase maior que a tela.

Comportamento escolhido na Parte 3:
- Horizontal: segue suave, com um pequeno atraso, mostrando mais espaço à frente.
- Vertical: NÃO acompanha cada pulo. Só muda de altura quando o personagem pisa
  num lugar mais alto ou mais baixo, ou quando ele chega perto da borda da tela.
"""

import math

import pygame


def _suavizar(atual: float, alvo: float, velocidade: float, dt: float) -> float:
    """Aproxima `atual` de `alvo` de forma suave e igual em qualquer FPS."""
    fator = 1 - math.exp(-velocidade * dt)
    return atual + (alvo - atual) * fator


class Camera:
    def __init__(self, cfg: dict, tamanho_tela: tuple[int, int], tamanho_mundo: tuple[int, int]):
        self.cfg = cfg
        self.largura, self.altura = tamanho_tela
        self.largura_mundo, self.altura_mundo = tamanho_mundo
        self.x = 0.0
        self.y = 0.0
        self.altura_chao = 0.0  # altura (pés) usada como referência vertical

    # ---------- onde a câmera quer estar ----------

    def _alvo_x(self, rect: pygame.Rect, olhando: int) -> float:
        return rect.centerx + olhando * self.cfg["olhar_frente"] - self.largura / 2

    def _alvo_y(self) -> float:
        return self.altura_chao - self.altura * self.cfg["altura_personagem"]

    def _limitar(self) -> None:
        """Não deixa a câmera mostrar o lado de fora do mundo."""
        self.x = max(0.0, min(self.x, self.largura_mundo - self.largura))
        self.y = max(0.0, min(self.y, self.altura_mundo - self.altura))

    # ---------- atualização ----------

    def centralizar(self, rect: pygame.Rect, olhando: int = 1) -> None:
        """Pula direto para o personagem, sem suavizar (início da fase, depois de cair)."""
        self.altura_chao = float(rect.bottom)
        self.x = self._alvo_x(rect, olhando)
        self.y = self._alvo_y()
        self._limitar()

    def atualizar(self, dt: float, rect: pygame.Rect, olhando: int, no_chao: bool) -> None:
        # Vertical: a referência só muda ao pisar, ou se o personagem for sair da tela.
        if no_chao:
            self.altura_chao = float(rect.bottom)
        topo_seguro = self.y + self.altura * self.cfg["margem_topo"]
        base_segura = self.y + self.altura * self.cfg["margem_base"]
        if rect.bottom > base_segura or rect.top < topo_seguro:
            self.altura_chao = float(rect.bottom)

        self.x = _suavizar(self.x, self._alvo_x(rect, olhando), self.cfg["suavidade_x"], dt)
        self.y = _suavizar(self.y, self._alvo_y(), self.cfg["suavidade_y"], dt)
        self._limitar()

    # ---------- desenho ----------

    def na_tela(self, rect: pygame.Rect) -> pygame.Rect:
        """Converte uma posição do mundo para a posição na tela."""
        return rect.move(-round(self.x), -round(self.y))
