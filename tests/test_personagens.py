"""Angel e Dark: mesma base de movimento, identidades separadas."""

import pygame

from jogo.nucleo.controles import Comandos
from jogo.personagens.angel import Angel
from jogo.personagens.dark import Dark
from jogo.personagens.personagem import Personagem, carregar_config

DT = 1 / 60
CHAO = pygame.Rect(0, 500, 960, 40)


def test_os_dois_herdam_de_personagem():
    assert issubclass(Angel, Personagem)
    assert issubclass(Dark, Personagem)


def test_bloco_do_personagem_completa_o_movimento():
    cfg = carregar_config("dark")
    assert "forca_pulo" in cfg  # veio de [movimento]
    assert "cor" in cfg  # veio de [dark]


def test_cores_diferentes():
    assert Angel.criar((0, 0)).cor != Dark.criar((0, 0)).cor


def trajeto(classe):
    """Posições de um pulo andando para a direita."""
    p = classe.criar((100, 400))
    for _ in range(30):
        p.atualizar(DT, Comandos(), [CHAO])
    pontos = []
    p.atualizar(DT, Comandos(direita=True, pulo_apertado=True, pulo_segurado=True), [CHAO])
    for _ in range(90):
        p.atualizar(DT, Comandos(direita=True, pulo_segurado=True), [CHAO])
        pontos.append((p.rect.x, p.rect.y))
    return pontos


def test_movimento_igual_entre_angel_e_dark():
    """Decisão de 28/11: só os poderes diferenciam os dois."""
    assert trajeto(Angel) == trajeto(Dark)


def test_paredes_invisiveis_seguram_o_personagem_no_mundo():
    from jogo.fases import carregador_fases

    fase = carregador_fases.carregar("01_floresta", escala=2)
    p = Angel.criar((fase.inicio[0], fase.inicio[1] - 48))
    for _ in range(180):  # 3 segundos andando para a esquerda
        p.atualizar(DT, Comandos(esquerda=True), fase.solidos)
    assert p.rect.left == 0
