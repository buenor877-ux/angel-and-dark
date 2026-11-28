"""Planta da Floresta: fica parada e cospe sementes num ritmo fixo, sempre com aviso.

O ciclo é um metrônomo: espera → aviso (incha e fica vermelha) → cospe → espera...
Quem observa um ciclo aprende o ritmo e sabe exatamente quando pular.

Ela só "acorda" quando o jogador chega perto (não fica atirando fora da tela) e
cospe sempre para o mesmo lado: o padrão é a esquerda, de onde o jogador vem;
no Tiled dá para virar com a propriedade olhando = "direita".
"""

from enum import Enum

import pygame

from jogo.inimigos.inimigo import Inimigo
from jogo.projeteis import Projetil


class EstadoPlanta(Enum):
    ESPERA = "espera"  # parada, contando o tempo até o próximo tiro
    AVISO = "aviso"  # incha e fica vermelha: a semente vem aí


class Planta(Inimigo):
    chave = "planta"

    def reiniciar(self) -> None:
        super().reiniciar()
        self.estado = EstadoPlanta.ESPERA
        self.cronometro = self.cfg["tempo_espera"]

    def acordada(self, alvo: pygame.Rect) -> bool:
        """O jogador está perto o bastante para ela atirar?"""
        dx = abs(alvo.centerx - self.rect.centerx)
        dy = abs(alvo.centery - self.rect.centery)
        return dx <= self.cfg["distancia_ativacao"] and dy <= self.cfg["altura_ativacao"]

    def pensar(self, dt: float, solidos: list[pygame.Rect], alvo: pygame.Rect) -> None:
        self.vel_x = 0.0  # planta não anda
        if self.estado == EstadoPlanta.ESPERA:
            # O relógio só corre com o jogador por perto. Longe, ela "dorme"
            # e guarda onde parou: o ritmo continua o mesmo quando ele volta.
            if self.acordada(alvo):
                self.cronometro -= dt
                if self.cronometro <= 0:
                    self.estado = EstadoPlanta.AVISO
                    self.cronometro += self.cfg["tempo_aviso"]
        else:  # AVISO: uma vez avisado, o tiro sempre sai (aviso sem ataque confunde)
            self.cronometro -= dt
            if self.cronometro <= 0:
                self.cuspir()
                self.estado = EstadoPlanta.ESPERA
                self.cronometro += self.cfg["tempo_espera"]

    def boca(self) -> tuple[float, float]:
        """De onde a semente sai: na beirada do lado em que ela olha."""
        x = self.rect.right if self.olhando > 0 else self.rect.left
        return x, self.rect.top + self.cfg["altura_boca"]

    def cuspir(self) -> None:
        self.disparos.append(Projetil.de_config(self.cfg["semente"], self.boca(), self.olhando))

    # ---------- desenho ----------

    @property
    def progresso_aviso(self) -> float:
        """0 no começo do aviso, 1 na hora do tiro."""
        if self.estado != EstadoPlanta.AVISO:
            return 0.0
        return 1 - max(0.0, self.cronometro) / self.cfg["tempo_aviso"]

    def cor_atual(self) -> tuple:
        if self.estado == EstadoPlanta.AVISO:
            return tuple(self.cfg["cor_aviso"])
        return self.cor

    def forma_desenho(self, rect: pygame.Rect) -> pygame.Rect:
        """Durante o aviso, vai inchando até a hora do tiro (os pés ficam no lugar)."""
        inchaco = round(self.cfg["inchaco"] * self.progresso_aviso)
        maior = rect.inflate(inchaco * 2, inchaco * 2)
        maior.midbottom = rect.midbottom
        return maior

    def desenhar_detalhes(self, tela: pygame.Surface, rect: pygame.Rect) -> None:
        # Folhas na base (verde escuro) e a "boca" escura do lado em que ela cospe.
        folha = tuple(self.cfg["cor_folha"])
        pygame.draw.rect(tela, folha, (rect.left - 6, rect.bottom - 8, rect.width + 12, 8))
        altura_boca = round(self.cfg["altura_boca"] * rect.height / self.rect.height)
        boca_x = rect.right - 8 if self.olhando > 0 else rect.left
        pygame.draw.rect(tela, (30, 20, 20), (boca_x, rect.top + altura_boca - 5, 8, 10))
        super().desenhar_detalhes(tela, rect)  # o olho
