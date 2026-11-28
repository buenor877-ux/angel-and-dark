# /// script
# dependencies = [
#     "pygame-ce",
#     "pytmx",
# ]
# ///
"""Ponto de entrada do jogo. O pygbag exige que este arquivo se chame main.py.

O bloco acima (PEP 723) e os imports abaixo existem por causa do navegador: o pygbag
lê SÓ este arquivo para descobrir quais bibliotecas baixar. Sem eles, o jogo quebra
no navegador com "module 'pygame' has no attribute 'event'".
"""

import asyncio

import pygame  # noqa: F401  (precisa aparecer aqui para o pygbag preparar o pygame)
import pytmx  # noqa: F401  (idem: o carregador de fases usa)

from jogo.nucleo.jogo import Jogo


async def main():
    await Jogo().rodar()


asyncio.run(main())
