"""Inimigos das fases. Cada tipo do Tiled (nome do objeto) aponta para a sua classe."""

from jogo.inimigos.inimigo import Inimigo
from jogo.inimigos.javali import Javali
from jogo.inimigos.planta import Planta
from jogo.inimigos.vespa import Vespa

TIPOS: dict[str, type[Inimigo]] = {"javali": Javali, "planta": Planta, "vespa": Vespa}


def criar(tipo: str, area, propriedades: dict | None = None) -> Inimigo:
    return TIPOS[tipo].criar(area, propriedades)
