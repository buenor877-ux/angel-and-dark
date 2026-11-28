"""Vespa da Floresta: voa em zigue-zague dentro do território, sempre no mesmo desenho.

Ela anda na horizontal e na vertical ao mesmo tempo, com velocidade constante, e
rebate nas bordas do território, como uma bolinha numa caixa. O resultado é um
zigue-zague que se repete: quem observa um pouco sabe por onde ela vai passar.

Não sente gravidade nem bate em blocos: por isso o território dela, no Tiled,
precisa ficar no ar livre (há um teste que confere isso no mapa).
"""

import pygame

from jogo.inimigos.inimigo import Inimigo


class Vespa(Inimigo):
    chave = "vespa"

    def reiniciar(self) -> None:
        super().reiniciar()
        self.rect.center = self.area.center  # nasce no meio do território, no ar
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        self.vel_x = self.olhando * self.cfg["velocidade_x"]
        self.vel_y = -self.cfg["velocidade_y"]  # começa subindo
        self.tempo = 0.0  # para bater as asas

    def atualizar(self, dt: float, solidos: list[pygame.Rect], alvo: pygame.Rect) -> None:
        if self.derrotado:  # pisada: cai reto, sem asas, até sumir
            self.y += self.cfg["velocidade_queda_derrotada"] * dt
            self.rect.y = round(self.y)
        super().atualizar(dt, solidos, alvo)

    def _mover(self, dt: float, solidos: list[pygame.Rect]) -> None:
        """Voa e rebate nas bordas do território (no lugar da gravidade da classe base)."""
        self.tempo += dt
        self.bateu = False
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        self.rect.topleft = (round(self.x), round(self.y))

        a = self.area
        if self.rect.left <= a.left or self.rect.right >= a.right:
            self.rect.clamp_ip(a)
            # Vira para o lado de dentro do território.
            self.olhando = 1 if self.rect.left <= a.left else -1
            self.vel_x = self.olhando * self.cfg["velocidade_x"]
            self.bateu = True
        if self.rect.top <= a.top or self.rect.bottom >= a.bottom:
            self.rect.clamp_ip(a)
            sinal = 1 if self.rect.top <= a.top else -1
            self.vel_y = sinal * self.cfg["velocidade_y"]
        self.x, self.y = float(self.rect.x), float(self.rect.y)

    # ---------- desenho ----------

    def desenhar_detalhes(self, tela: pygame.Surface, rect: pygame.Rect) -> None:
        listra = tuple(self.cfg["cor_listra"])
        for i in (1, 2):  # duas listras pretas, de cima a baixo
            x = rect.left + rect.width * i // 3 - 2
            pygame.draw.rect(tela, listra, (x, rect.top, 4, rect.height))
        # Ferrão atrás (do lado oposto ao que ela olha).
        ferrao = rect.left - 5 if self.olhando > 0 else rect.right
        pygame.draw.rect(tela, listra, (ferrao, rect.centery - 2, 5, 4))
        # Asas batendo: sobem e descem ~12 vezes por segundo.
        if not self.derrotado:
            alta = int(self.tempo * 24) % 2 == 0
            asa = pygame.Rect(0, 0, rect.width * 2 // 3, 8 if alta else 5)
            asa.midbottom = (rect.centerx, rect.top + (0 if alta else 3))
            pygame.draw.ellipse(tela, tuple(self.cfg["cor_asa"]), asa)
        super().desenhar_detalhes(tela, rect)  # o olho
