"""Inimigos das fases. Cada tipo do Tiled (nome do objeto) aponta para a sua classe."""

from jogo.inimigos.inimigo import Inimigo
from jogo.inimigos.javali import Javali

TIPOS: dict[str, type[Inimigo]] = {"javali": Javali}


def criar(tipo: str, area) -> Inimigo:
    return TIPOS[tipo].criar(area)
