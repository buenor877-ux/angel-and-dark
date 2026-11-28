"""Carrega fases feitas no Tiled (assets/mapas/<nome>.tmx).

É o único lugar do jogo que conhece o Tiled e o pytmx. Se um dia trocar de editor
(LDtk, por exemplo), só este arquivo muda: o resto do jogo continua recebendo uma Fase.

Combinado com o mapa:
- camada de blocos com a propriedade `solido = true` → o personagem bate nela;
- camada de blocos com `perigo = true` → encostou, leva dano. A propriedade
  `altura_dano` (0 a 1) diz quanto do bloco, de baixo para cima, machuca;
- camada de blocos com `frente = true` → desenhada na frente do personagem (água);
- outras camadas de blocos → só desenho atrás do personagem (decoração);
- camada de objetos "objetos": ponto "inicio" (pés), retângulo "chegada" e
  objetos-bloco "checkpoint" (podem ser vários) e retângulos de inimigo, com o
  nome do tipo ("javali", "planta" ou "vespa"). O retângulo do inimigo é o
  território dele: quem anda no chão fica com os pés no fundo do retângulo e vai
  até as pontas; a vespa voa dentro dele. Propriedades do objeto (ex.: olhando =
  "direita") chegam ao inimigo.
"""

from pathlib import Path

import pygame
import pytmx

from jogo.fases.fase import Checkpoint, Fase, LugarInimigo

TIPOS_INIMIGO = {"javali", "planta", "vespa"}  # nomes de objeto que viram inimigo

RAIZ = Path(__file__).resolve().parents[2]
PASTA_MAPAS = RAIZ / "assets" / "mapas"

# Cor que significa "vazio" nas camadas do cenário. Não aparece na arte da Kenney
# (conferido: nenhum pixel rosa e nenhum pixel semitransparente).
COR_CHAVE = (255, 0, 255)


def _camada_vazia(tamanho: tuple[int, int]) -> pygame.Surface:
    """Imagem do tamanho do mundo, toda "vazia", pronta para receber blocos.

    Por que não usar transparência por pixel (SRCALPHA): a cada quadro o navegador
    misturava todos os pixels da tela, até os vazios, e cada camada custava ~16 ms
    (o limite para 60 FPS é 16,7 ms). Pixel art não tem meio-transparente, então
    uma cor-chave com RLE (que pula os trechos vazios de uma vez) dá o mesmo visual.
    """
    camada = pygame.Surface(tamanho)
    camada.fill(COR_CHAVE)
    camada.set_colorkey(COR_CHAVE, pygame.RLEACCEL)
    return camada


def carregar(nome: str, escala: int) -> Fase:
    mapa = pytmx.load_pygame(str(PASTA_MAPAS / f"{nome}.tmx"))
    tam = mapa.tilewidth * escala  # tamanho do bloco no jogo, em pixels
    tamanho_mundo = (mapa.width * tam, mapa.height * tam)

    solidos = [[False] * mapa.width for _ in range(mapa.height)]
    perigos = []
    desenho = _camada_vazia(tamanho_mundo)
    desenho_frente = None

    for camada in mapa.visible_layers:
        if not isinstance(camada, pytmx.TiledTileLayer):
            continue
        props = camada.properties
        e_solida = bool(props.get("solido", False))
        e_perigo = bool(props.get("perigo", False))
        altura_dano = float(props.get("altura_dano", 1.0))
        if props.get("frente", False):
            desenho_frente = desenho_frente or _camada_vazia(tamanho_mundo)
            destino = desenho_frente
        else:
            destino = desenho

        for x, y, gid in camada.iter_data():
            if not gid:
                continue
            imagem = mapa.get_tile_image_by_gid(gid)
            if imagem is not None:
                destino.blit(pygame.transform.scale(imagem, (tam, tam)), (x * tam, y * tam))
            if e_solida:
                solidos[y][x] = True
            if e_perigo:
                perigos.append(_area_de_dano(x, y, tam, altura_dano))

    inicio = chegada = None
    checkpoints = []
    inimigos = []
    for o in mapa.get_layer_by_name("objetos"):
        if o.name == "inicio":
            inicio = (round(o.x * escala), round(o.y * escala))
        elif o.name == "chegada":
            chegada = _escalar(o, escala)
        elif o.name == "checkpoint":
            img = o.image and pygame.transform.scale(o.image, (tam, tam))
            checkpoints.append(Checkpoint(_escalar(o, escala), img))
        elif o.name in TIPOS_INIMIGO:
            inimigos.append(LugarInimigo(o.name, _escalar(o, escala), dict(o.properties)))
    if inicio is None or chegada is None:
        raise ValueError(f"{nome}.tmx precisa dos objetos 'inicio' e 'chegada'")

    return Fase(
        largura=tamanho_mundo[0],
        altura=tamanho_mundo[1],
        inicio=inicio,
        chegada=chegada,
        plataformas=juntar_blocos(solidos, tam),
        superficies=achar_superficies(solidos, tam),
        perigos=perigos,
        checkpoints=checkpoints,
        inimigos=inimigos,
        desenho=desenho,
        desenho_frente=desenho_frente,
        nome=mapa.properties.get("nome", nome),
    )


def _escalar(objeto, escala: int) -> pygame.Rect:
    return pygame.Rect(
        round(objeto.x * escala),
        round(objeto.y * escala),
        round(objeto.width * escala),
        round(objeto.height * escala),
    )


def _area_de_dano(x: int, y: int, tam: int, altura_dano: float) -> pygame.Rect:
    """Só a parte de baixo do bloco machuca (o espinho não ocupa o bloco todo).

    Também encolhe um pouco dos lados: raspar na pontinha não deve doer.
    """
    altura = max(1, round(tam * altura_dano))
    margem = round(tam * 0.15)
    return pygame.Rect(x * tam + margem, (y + 1) * tam - altura, tam - 2 * margem, altura)


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
