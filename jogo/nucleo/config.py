"""Leitura dos arquivos de configuração (pasta config/).

É o único lugar do jogo que sabe que as configurações são arquivos TOML.
Se um dia trocar de formato, só este arquivo muda.
"""

import tomllib
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PASTA_CONFIG = RAIZ / "config"


def carregar(nome: str) -> dict:
    """Lê config/<nome>.toml e devolve um dicionário."""
    caminho = PASTA_CONFIG / f"{nome}.toml"
    with caminho.open("rb") as arquivo:
        return tomllib.load(arquivo)
