"""Ponto de entrada do jogo. O pygbag exige que este arquivo se chame main.py."""

import asyncio

from jogo.nucleo.jogo import Jogo


async def main():
    await Jogo().rodar()


asyncio.run(main())
