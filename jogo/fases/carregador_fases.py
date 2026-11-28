"""Carrega fases feitas no Tiled (assets/mapas/<nome>.tmx).

É o único lugar do jogo que conhece o Tiled e o pytmx. Se um dia trocar de editor
(LDtk, por exemplo), só este arquivo muda: o resto do jogo continua recebendo uma Fase.

Combinado com o mapa:
- camada de blocos com a propriedade `solido = true` → o personagem bate nela;
- outras camadas de blocos → só desenho (decoração);
- camada de objetos "objetos" com um ponto "inicio" (pés) e um retângulo "chegada".
"""

from pathlib import Path

import pygame
import pytmx

from jogo.fases.fase import Fase

RAIZ = Path(__file__).resolve().parents[2]
PASTA_MAPAS = RAIZ / "assets" / "mapas"


def carregar(nome: str, escala: int) -> Fase:
    mapa = pytmx.load_pygame(str(PASTA_MAPAS / f"{nome}.tmx"))
    tam = mapa.tilewidth * escala  # tamanho do bloco no jogo, em pixels

    solidos = [[False] * mapa.width for _ in range(mapa.height)]
    desenho = pygame.Surface((mapa.width * tam, mapa.height * tam), pygame.SRCALPHA)

    for camada in mapa.visible_layers:
        if isinstance(camada, pytmx.TiledTileLayer):
            e_solida = bool(camada.properties.get("solido", False))
            for x, y, gid in camada.iter_data():
                if not gid:
                    continue
                imagem = mapa.get_tile_image_by_gid(gid)
                if imagem is not None:
                    desenho.blit(pygame.transform.scale(imagem, (tam, tam)), (x * tam, y * tam))
                if e_solida:
                    solidos[y][x] = True

    objetos = {o.name: o for o in mapa.get_layer_by_name("objetos")}
    ini, fim = objetos["inicio"], objetos["chegada"]

    return Fase(
        largura=mapa.width * tam,
        altura=mapa.height * tam,
        inicio=(round(ini.x * escala), round(ini.y * escala)),
        chegada=pygame.Rect(
            round(fim.x * escala),
            round(fim.y * escala),
            round(fim.width * escala),
            round(fim.height * escala),
        ),
        plataformas=juntar_blocos(solidos, tam),
        superficies=achar_superficies(solidos, tam),
        desenho=desenho,
        nome=mapa.properties.get("nome", nome),
    )


def juntar_blocos(solidos: list[list[bool]], tam: int) -> list[pygame.Rect]:
    """Junta blocos vizinhos em retângulos maiores.

    Testar colisão com 287 blocos a cada quadro é desperdício: juntando as sequências
    na horizontal e depois as faixas iguais na vertical, sobram poucos retângulos.
    """
    faixas: dict[tuple[int, int], pygame.Rect] = {}  # (início, fim) da faixa → retângulo aberto
    resultado = []
    for y, linha in enumerate(solidos):
        atuais = set()
        x = 0
        while x < len(linha):
            if not linha[x]:
                x += 1
                continue
            inicio = x
            while x < len(linha) and linha[x]:
                x += 1
            chave = (inicio, x)
            atuais.add(chave)
            if chave in faixas:
                faixas[chave].height += tam  # mesma faixa da linha de cima: cresce para baixo
            else:
                faixas[chave] = pygame.Rect(inicio * tam, y * tam, (x - inicio) * tam, tam)
        for chave in list(faixas):
            if chave not in atuais:  # a faixa acabou
                resultado.append(faixas.pop(chave))
    resultado.extend(faixas.values())
    return resultado


def achar_superficies(solidos: list[list[bool]], tam: int) -> list[pygame.Rect]:
    """Topos onde dá para pisar: bloco sólido com espaço vazio logo acima."""
    superficies = []
    for y, linha in enumerate(solidos):
        x = 0
        while x < len(linha):
            livre_acima = y == 0 or not solidos[y - 1][x]
            if not (linha[x] and livre_acima):
                x += 1
                continue
            inicio = x
            while x < len(linha) and linha[x] and (y == 0 or not solidos[y - 1][x]):
                x += 1
            superficies.append(pygame.Rect(inicio * tam, y * tam, (x - inicio) * tam, tam))
    return superficies
