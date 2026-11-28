"""O que todo inimigo tem em comum: corpo, gravidade, território, levar pisão e ser derrotado.

Cada inimigo (javali, planta, vespa...) herda desta classe e só escreve o próprio
comportamento em `pensar()`. É a mesma ideia de Angel e Dark herdando de Personagem.
"""

import pygame

from jogo.nucleo import config


def carregar_config(chave: str) -> dict:
    """Junta o bloco [geral] com o bloco do inimigo; o do inimigo vence."""
    dados = config.carregar("inimigos")
    return {**dados["geral"], **dados[chave]}


class Inimigo:
    chave = ""  # nome do bloco em config/inimigos.toml

    def __init__(self, cfg: dict, area: pygame.Rect):
        self.cfg = cfg
        self.area = pygame.Rect(area)  # território: não sai daqui
        self.cor = tuple(cfg["cor"])
        self.rect = pygame.Rect(0, 0, cfg["largura"], cfg["altura"])
        self.reiniciar()

    @classmethod
    def criar(cls, area: pygame.Rect) -> "Inimigo":
        return cls(carregar_config(cls.chave), area)

    def reiniciar(self) -> None:
        """Volta para o meio do território, vivo e olhando para a esquerda."""
        self.rect.midbottom = self.area.midbottom
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.olhando = -1  # 1 = direita, -1 = esquerda (o jogador vem da esquerda)
        self.no_chao = False
        self.bateu = False  # bateu em parede ou no fim do território neste quadro
        self.tempo_derrotado = 0.0
        self.derrotado = False

    @property
    def vivo(self) -> bool:
        """Ainda participa da fase (machuca e pode ser pisado)."""
        return not self.derrotado

    @property
    def piscando_dano(self) -> bool:
        """Logo depois do pisão: o corpo inteiro fica branco antes de amassar."""
        if not self.derrotado:
            return False
        return self.cfg["tempo_derrotado"] - self.tempo_derrotado < self.cfg["tempo_piscar_dano"]

    @property
    def sumiu(self) -> bool:
        """Já acabou a animação de amassado: não precisa mais desenhar."""
        return self.derrotado and self.tempo_derrotado <= 0

    # ---------- atualização ----------

    def atualizar(self, dt: float, solidos: list[pygame.Rect], alvo: pygame.Rect) -> None:
        if self.derrotado:
            self.tempo_derrotado = max(0.0, self.tempo_derrotado - dt)
            return
        self.pensar(dt, solidos, alvo)
        self._mover(dt, solidos)

    def pensar(self, dt: float, solidos: list[pygame.Rect], alvo: pygame.Rect) -> None:
        """Decide `vel_x` e `olhando`. Cada inimigo escreve o seu."""

    def _mover(self, dt: float, solidos: list[pygame.Rect]) -> None:
        """Anda e cai como o personagem, mas guarda se bateu (`bateu`)."""
        self.bateu = False
        self.x += self.vel_x * dt
        self.rect.x = round(self.x)
        for p in solidos:
            if self.rect.colliderect(p):
                if self.vel_x > 0:
                    self.rect.right = p.left
                elif self.vel_x < 0:
                    self.rect.left = p.right
                self.bateu = True
        # O território também funciona como parede.
        if self.rect.left < self.area.left:
            self.rect.left = self.area.left
            self.bateu = True
        elif self.rect.right > self.area.right:
            self.rect.right = self.area.right
            self.bateu = True
        self.x = float(self.rect.x)

        self.vel_y = min(self.vel_y + self.cfg["gravidade"] * dt, self.cfg["velocidade_queda_max"])
        self.y += self.vel_y * dt
        self.rect.y = round(self.y)
        self.no_chao = False
        for p in solidos:
            if self.rect.colliderect(p) and self.vel_y > 0:
                self.rect.bottom = p.top
                self.no_chao = True
                self.vel_y = 0.0
        if not self.no_chao and self.rect.move(0, 1).collidelist(solidos) != -1:
            self.no_chao = True
            self.vel_y = 0.0
        self.y = float(self.rect.y)

    def tem_chao_a_frente(self, solidos: list[pygame.Rect]) -> bool:
        """Olha um pixel à frente do pé: se não tem chão ali, é borda (buraco ou água)."""
        x = self.rect.right if self.olhando > 0 else self.rect.left - 1
        return pygame.Rect(x, self.rect.bottom, 1, 2).collidelist(solidos) != -1

    def chega_na_borda(self, solidos: list[pygame.Rect]) -> bool:
        """Borda do chão, parede ou fim do território logo à frente."""
        if not self.tem_chao_a_frente(solidos):
            return True
        frente = self.rect.move(self.olhando * 2, -1)
        if frente.collidelist(solidos) != -1:
            return True
        return frente.left < self.area.left or frente.right > self.area.right

    # ---------- contato com o jogador ----------

    def foi_pisado(self, pes_antes: float, vel_y: float, rect: pygame.Rect) -> bool:
        """O jogador caiu em cima? Vindo de cima e descendo; de lado não vale."""
        if not self.vivo or not rect.colliderect(self.rect) or vel_y <= 0:
            return False
        return pes_antes <= self.rect.top + self.cfg["tolerancia_pisao"]

    def derrotar(self) -> None:
        self.derrotado = True
        self.tempo_derrotado = self.cfg["tempo_derrotado"]
        self.vel_x = 0.0

    def machuca(self, rect: pygame.Rect) -> bool:
        return self.vivo and rect.colliderect(self.rect)

    # ---------- desenho ----------

    def cor_atual(self) -> tuple:
        return self.cor

    def deslocamento_desenho(self) -> int:
        """Tremida do desenho (o corpo não se mexe)."""
        return 0

    def desenhar(self, tela: pygame.Surface, camera) -> None:
        if self.sumiu:
            return
        rect = camera.na_tela(self.rect)
        if self.piscando_dano:  # branco = levou dano (vermelho é só para "vou atacar")
            # Pisca branco/marrom 20 vezes por segundo: assim não se confunde com a Angel,
            # que também é branca por enquanto.
            branco = int(self.tempo_derrotado * 40) % 2 == 0
            pygame.draw.rect(tela, tuple(self.cfg["cor_dano"]) if branco else self.cor, rect)
            return
        if self.derrotado:  # amassado: um terço da altura, grudado no chão
            rect = pygame.Rect(rect.x, rect.bottom - rect.height // 3, rect.width, rect.height // 3)
            pygame.draw.rect(tela, self.cor, rect)
            return
        rect = rect.move(self.deslocamento_desenho(), 0)
        pygame.draw.rect(tela, self.cor_atual(), rect)
        # "Presa" clara do lado em que olha: mostra para onde ele vai.
        lado = rect.right - 8 if self.olhando > 0 else rect.left
        pygame.draw.rect(tela, (240, 230, 210), (lado, rect.bottom - 12, 8, 6))
        olho = rect.right - 14 if self.olhando > 0 else rect.left + 10
        pygame.draw.rect(tela, (20, 20, 20), (olho, rect.top + 6, 4, 4))
