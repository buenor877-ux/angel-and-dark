"""Javali da Floresta: patrulha, vê o jogador, avisa tremendo e investe em linha reta.

Padrão "legível" (docs/04): todo ataque tem um aviso antes. Quem presta atenção
vê o javali parar e tremer, e tem tempo de pular por cima ou de pisar nele.
"""

from enum import Enum

import pygame

from jogo.inimigos.inimigo import Inimigo


class EstadoJavali(Enum):
    PATRULHA = "patrulha"  # anda devagar e vira na borda, na parede ou no fim do território
    AVISO = "aviso"  # viu o jogador: para e treme
    INVESTIDA = "investida"  # corre em linha reta até a borda ou a parede
    DESCANSO = "descanso"  # cansado, parado um pouco


class Javali(Inimigo):
    chave = "javali"

    def reiniciar(self) -> None:
        super().reiniciar()
        self.estado = EstadoJavali.PATRULHA
        self.cronometro = 0.0

    def ve(self, alvo: pygame.Rect) -> bool:
        """O jogador está na frente dele, perto e mais ou menos na mesma altura?"""
        frente = (alvo.centerx - self.rect.centerx) * self.olhando
        mesma_altura = alvo.bottom > self.rect.top - self.cfg["altura_visao"]
        mesma_altura = mesma_altura and alvo.top < self.rect.bottom
        return 0 < frente <= self.cfg["distancia_visao"] and mesma_altura

    def pensar(self, dt: float, solidos: list[pygame.Rect], alvo: pygame.Rect) -> None:
        e = self.estado
        if e == EstadoJavali.PATRULHA:
            if self.ve(alvo):
                self._mudar(EstadoJavali.AVISO, self.cfg["tempo_aviso"])
            else:
                if self.chega_na_borda(solidos):
                    self.olhando *= -1
                self.vel_x = self.olhando * self.cfg["velocidade_patrulha"]
                return
        elif e == EstadoJavali.INVESTIDA:
            if self.chega_na_borda(solidos):
                self._mudar(EstadoJavali.DESCANSO, self.cfg["tempo_descanso"])
            else:
                self.vel_x = self.olhando * self.cfg["velocidade_investida"]
                return
        else:  # AVISO ou DESCANSO: parado, esperando o cronômetro
            self.cronometro -= dt
            if self.cronometro <= 0:
                if e == EstadoJavali.AVISO:
                    self._mudar(EstadoJavali.INVESTIDA, 0.0)
                else:
                    self._mudar(EstadoJavali.PATRULHA, 0.0)
        self.vel_x = 0.0

    def _mudar(self, estado: EstadoJavali, tempo: float) -> None:
        self.estado = estado
        self.cronometro = tempo
        self.vel_x = 0.0

    # ---------- desenho ----------

    def cor_atual(self) -> tuple:
        if self.estado in (EstadoJavali.AVISO, EstadoJavali.INVESTIDA):
            return tuple(self.cfg["cor_aviso"])
        return self.cor

    def desenhar_detalhes(self, tela: pygame.Surface, rect: pygame.Rect) -> None:
        # "Presa" clara do lado em que olha: mostra para onde ele vai.
        lado = rect.right - 8 if self.olhando > 0 else rect.left
        pygame.draw.rect(tela, (240, 230, 210), (lado, rect.bottom - 12, 8, 6))
        super().desenhar_detalhes(tela, rect)  # o olho

    def deslocamento_desenho(self) -> int:
        if self.estado != EstadoJavali.AVISO:
            return 0
        # Treme de um lado para o outro ~20 vezes por segundo.
        return self.cfg["tremor"] if int(self.cronometro * 40) % 2 else -self.cfg["tremor"]
