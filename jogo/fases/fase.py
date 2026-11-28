"""Uma fase: tamanho, colisão, perigos, checkpoints, início, chegada e o desenho do cenário.

A fase não sabe de onde veio (Tiled, dicionário de teste). Quem cria é o carregador_fases.py.
"""

from dataclasses import dataclass, field

import pygame

ESPESSURA_PAREDE = 100


@dataclass
class LugarInimigo:
    """Onde um inimigo nasce: o tipo ("javali") e a área dele.

    A fase só guarda o lugar; quem cria o inimigo de verdade é a cena
    (assim a fase não precisa conhecer as classes de inimigo).
    A área é o território: o inimigo nasce no meio, com os pés no fundo dela,
    e não sai dela nem patrulhando nem investindo.
    """

    tipo: str
    area: pygame.Rect
    propriedades: dict = field(default_factory=dict)  # do Tiled (ex.: olhando = "direita")


def _lugar_inimigo(dados: list) -> LugarInimigo:
    """["planta", x, y, largura, altura] e, se quiser, as propriedades no fim."""
    propriedades = dados[5] if len(dados) > 5 else {}
    return LugarInimigo(dados[0], pygame.Rect(*dados[1:5]), propriedades)


class Checkpoint:
    """Bandeirinha que vira o novo ponto de volta quando o personagem passa por ela."""

    def __init__(self, rect: pygame.Rect, imagem: pygame.Surface | None = None):
        self.rect = rect
        self.ativo = False
        self.imagem = imagem
        # Apagada (cinza) até ser ativada.
        self.imagem_apagada = pygame.transform.grayscale(imagem) if imagem else None

    @property
    def pes(self) -> tuple[int, int]:
        """Onde ficam os pés do personagem ao voltar aqui."""
        return self.rect.centerx, self.rect.bottom


class Fase:
    def __init__(
        self,
        largura: int,
        altura: int,
        inicio: tuple[int, int],
        chegada: pygame.Rect,
        plataformas: list[pygame.Rect],
        superficies: list[pygame.Rect] | None = None,
        perigos: list[pygame.Rect] | None = None,
        checkpoints: list[Checkpoint] | None = None,
        inimigos: list[LugarInimigo] | None = None,
        desenho: pygame.Surface | None = None,
        desenho_frente: pygame.Surface | None = None,
        nome: str = "",
    ):
        self.largura, self.altura = largura, altura
        self.inicio = inicio  # posição dos PÉS do personagem no começo
        self.chegada = chegada
        self.plataformas = plataformas  # retângulos sólidos (já juntados)
        # Superfícies = topos onde dá para pisar. Usadas para conferir o alcance.
        self.superficies = superficies if superficies is not None else plataformas
        self.perigos = perigos or []  # encostou, leva dano
        self.checkpoints = sorted(checkpoints or [], key=lambda c: c.rect.x)
        self.inimigos = sorted(inimigos or [], key=lambda i: i.area.x)
        self.desenho = desenho  # cenário desenhado atrás do personagem
        self.desenho_frente = desenho_frente  # desenhado na frente (água, por exemplo)
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
            perigos=[pygame.Rect(*p) for p in dados.get("perigos", [])],
            checkpoints=[Checkpoint(pygame.Rect(*c)) for c in dados.get("checkpoints", [])],
            inimigos=[_lugar_inimigo(i) for i in dados.get("inimigos", [])],
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

    def perigo_tocado(self, rect: pygame.Rect) -> pygame.Rect | None:
        """O perigo em que o personagem encostou, ou None."""
        i = rect.collidelist(self.perigos)
        return self.perigos[i] if i != -1 else None

    def ativar_checkpoints(self, rect: pygame.Rect) -> bool:
        """Ativa os checkpoints que o personagem já passou. True se ativou algum novo."""
        novo = False
        for c in self.checkpoints:
            if not c.ativo and rect.centerx >= c.rect.centerx:  # passou, mesmo pulando por cima
                c.ativo = True
                novo = True
        return novo

    def ponto_de_volta(self) -> tuple[int, int]:
        """Pés do personagem ao perder uma vida: último checkpoint ativo, ou o início."""
        ativos = [c for c in self.checkpoints if c.ativo]
        return ativos[-1].pes if ativos else self.inicio

    # ---------- desenho ----------

    def _area(self, tela: pygame.Surface, camera) -> pygame.Rect:
        return pygame.Rect(round(camera.x), round(camera.y), *tela.get_size())

    def desenhar(self, tela: pygame.Surface, cores: dict, camera) -> None:
        if self.desenho is not None:
            # Copia só o pedaço do cenário que a câmera está vendo.
            tela.blit(self.desenho, (0, 0), self._area(tela, camera))
        else:
            # Sem desenho (fases de teste): retângulos simples.
            for p in self.plataformas:
                pygame.draw.rect(tela, cores["plataforma"], camera.na_tela(p))
            for p in self.perigos:
                pygame.draw.rect(tela, cores["perigo"], camera.na_tela(p))
            pygame.draw.rect(tela, cores["destaque"], camera.na_tela(self.chegada))

        for c in self.checkpoints:
            imagem = c.imagem if c.ativo else c.imagem_apagada
            if imagem is not None:
                tela.blit(imagem, camera.na_tela(c.rect))
            else:
                cor = cores["destaque"] if c.ativo else cores["plataforma"]
                pygame.draw.rect(tela, cor, camera.na_tela(c.rect))

    def desenhar_frente(self, tela: pygame.Surface, camera) -> None:
        """O que fica na frente do personagem (água)."""
        if self.desenho_frente is not None:
            tela.blit(self.desenho_frente, (0, 0), self._area(tela, camera))
