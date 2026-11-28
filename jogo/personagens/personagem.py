"""O que Angel e Dark têm em comum: andar, pular, cair e bater nas plataformas.

Angel e Dark herdam desta classe. Os poderes de cada um ficam nas classes filhas.
"""

from enum import Enum

import pygame

from jogo.nucleo import config
from jogo.nucleo.controles import Comandos
from jogo.personagens.vida import Vida


def carregar_config(chave: str) -> dict:
    """Junta o bloco [movimento] com o bloco do personagem; o do personagem vence."""
    dados = config.carregar("personagens")
    return {**dados["movimento"], **dados[chave]}


class Estado(Enum):
    """Máquina de estados: o que o personagem está fazendo agora."""

    PARADO = "parado"
    ANDANDO = "andando"
    PULANDO = "pulando"
    CAINDO = "caindo"


def _aproximar(valor: float, alvo: float, passo: float) -> float:
    """Move `valor` em direção a `alvo` sem passar dele."""
    if valor < alvo:
        return min(valor + passo, alvo)
    return max(valor - passo, alvo)


class Personagem:
    nome = "Personagem"
    chave = ""  # nome do bloco em config/personagens.toml

    def __init__(self, cfg: dict, posicao: tuple[float, float]):
        self.cfg = cfg
        self.cor = tuple(cfg["cor"])
        self.rect = pygame.Rect(0, 0, cfg["largura"], cfg["altura"])
        self.inicio = posicao
        self.vida = Vida(config.carregar("personagens")["vida"])
        self.reiniciar()

    @classmethod
    def criar(cls, posicao: tuple[float, float]) -> "Personagem":
        """Cria o personagem já com a config dele."""
        return cls(carregar_config(cls.chave), posicao)

    def reiniciar(self) -> None:
        """Volta ao ponto inicial, parado."""
        # Posição guardada em float: o Rect só aceita inteiros e perderia precisão.
        self.x, self.y = float(self.inicio[0]), float(self.inicio[1])
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.no_chao = False
        self.olhando = 1  # 1 = direita, -1 = esquerda (a câmera usa para olhar à frente)
        self.tempo_desde_chao = 999.0  # para o tempo de coiote
        self.tempo_desde_pulo = 999.0  # para o buffer de pulo
        self.estado = Estado.CAINDO
        self._sincronizar_rect()

    # ---------- atualização (chamada todo quadro) ----------

    def atualizar(self, dt: float, comandos: Comandos, plataformas: list[pygame.Rect]) -> None:
        self.vida.atualizar(dt)
        if not self.vida.sem_controle:  # durante o empurrão, o controle não responde
            self._andar(dt, comandos)
            self._pular(dt, comandos)
        self._aplicar_gravidade(dt)
        self._mover_e_colidir(dt, plataformas)
        self._atualizar_estado()

    def levar_dano(self, origem_x: float) -> bool:
        """Perde 1 coração e é empurrado para longe de `origem_x`. False = estava invulnerável."""
        if not self.vida.levar_dano():
            return False
        lado = 1 if self.rect.centerx >= origem_x else -1
        self.vel_x = lado * self.vida.cfg["empurrao_x"]
        self.vel_y = -self.vida.cfg["empurrao_y"]
        self.no_chao = False
        return True

    def _andar(self, dt: float, comandos: Comandos) -> None:
        direcao = int(comandos.direita) - int(comandos.esquerda)
        if direcao:
            self.olhando = direcao
        alvo = direcao * self.cfg["velocidade"]
        taxa = self.cfg["aceleracao"] if direcao else self.cfg["desaceleracao"]
        self.vel_x = _aproximar(self.vel_x, alvo, taxa * dt)

    def _pular(self, dt: float, comandos: Comandos) -> None:
        self.tempo_desde_chao = 0.0 if self.no_chao else self.tempo_desde_chao + dt
        self.tempo_desde_pulo = 0.0 if comandos.pulo_apertado else self.tempo_desde_pulo + dt

        pode_pular = self.tempo_desde_chao <= self.cfg["tempo_coiote"]
        quer_pular = self.tempo_desde_pulo <= self.cfg["tempo_buffer_pulo"]
        if pode_pular and quer_pular:
            self.vel_y = -self.cfg["forca_pulo"]
            self.no_chao = False
            self.tempo_desde_chao = 999.0  # impede pulo duplo pelo coiote
            self.tempo_desde_pulo = 999.0

        # Pulo variável: soltar o botão enquanto sobe limita a velocidade de subida.
        limite_subida = -self.cfg["forca_pulo"] * self.cfg["corte_pulo"]
        if not comandos.pulo_segurado and self.vel_y < limite_subida:
            self.vel_y = limite_subida

    def _aplicar_gravidade(self, dt: float) -> None:
        self.vel_y = min(self.vel_y + self.cfg["gravidade"] * dt, self.cfg["velocidade_queda_max"])

    def _mover_e_colidir(self, dt: float, plataformas: list[pygame.Rect]) -> None:
        # Move um eixo de cada vez: assim sabemos de que lado bateu.
        self.x += self.vel_x * dt
        self._sincronizar_rect()
        for p in plataformas:
            if self.rect.colliderect(p):
                if self.vel_x > 0:
                    self.rect.right = p.left
                elif self.vel_x < 0:
                    self.rect.left = p.right
                self.x = float(self.rect.x)
                self.vel_x = 0.0

        self.y += self.vel_y * dt
        self._sincronizar_rect()
        self.no_chao = False
        for p in plataformas:
            if self.rect.colliderect(p):
                if self.vel_y > 0:
                    self.rect.bottom = p.top
                    self.no_chao = True
                elif self.vel_y < 0:
                    self.rect.top = p.bottom
                self.y = float(self.rect.y)
                self.vel_y = 0.0

        # Sensor de pé: encostada no chão (sem sobrepor) também conta como no chão.
        # Sem isto, a gravidade de meio pixel por quadro faz o estado piscar.
        if not self.no_chao and self.vel_y >= 0:
            if self.rect.move(0, 1).collidelist(plataformas) != -1:
                self.no_chao = True
                self.vel_y = 0.0
                self.y = float(self.rect.y)

    def _atualizar_estado(self) -> None:
        if not self.no_chao:
            self.estado = Estado.PULANDO if self.vel_y < 0 else Estado.CAINDO
        elif abs(self.vel_x) > 1:
            self.estado = Estado.ANDANDO
        else:
            self.estado = Estado.PARADO

    def _sincronizar_rect(self) -> None:
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

    # ---------- desenho ----------

    def desenhar(self, tela: pygame.Surface, camera=None) -> None:
        if not self.vida.visivel:  # piscando depois de levar dano
            return
        rect = camera.na_tela(self.rect) if camera else self.rect
        pygame.draw.rect(tela, self.cor, rect)
