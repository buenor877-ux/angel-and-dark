"""Testes das fases: o mapa do Tiled, a junção de blocos e o alcance (dá para chegar em tudo?)."""

import pygame
import pytest

from jogo.fases import carregador_fases
from jogo.fases.fase import Fase
from jogo.nucleo import config
from jogo.personagens.personagem import carregar_config

MARGEM = 0.85  # regra de design: usar no máximo 85% do pulo
ESCALA = 2


@pytest.fixture(scope="module")
def floresta():
    return carregador_fases.carregar("01_floresta", ESCALA)


def test_configs_carregam():
    assert config.carregar("jogo")["janela"]["fps"] == 60
    assert {"movimento", "angel", "dark"} <= config.carregar("personagens").keys()
    assert "fundo" in config.carregar("fases")["01_floresta"]


# ---------- o mapa da Floresta ----------


def test_floresta_tem_tamanho_e_desenho(floresta):
    assert floresta.tamanho == (160 * 18 * ESCALA, 30 * 18 * ESCALA)  # 6 telas
    assert floresta.desenho.get_size() == floresta.tamanho
    assert floresta.nome == "Floresta 1"


def test_inicio_e_chegada_dentro_do_mundo(floresta):
    mundo = pygame.Rect(0, 0, *floresta.tamanho)
    assert mundo.collidepoint(floresta.inicio)
    assert mundo.contains(floresta.chegada)


def test_inicio_fica_logo_acima_de_um_chao(floresta):
    x, y = floresta.inicio
    abaixo = pygame.Rect(x, y, 1, 40)
    assert abaixo.collidelist(floresta.plataformas) != -1


def test_blocos_viram_poucos_retangulos(floresta):
    """287 blocos de chão no mapa: juntados, a colisão fica bem mais leve."""
    assert len(floresta.plataformas) < 30


def test_detecta_queda_e_chegada(floresta):
    assert floresta.caiu_para_fora(pygame.Rect(100, floresta.altura + 200, 32, 48))
    assert not floresta.caiu_para_fora(pygame.Rect(100, 100, 32, 48))
    assert floresta.chegou(floresta.chegada.copy())


# ---------- juntar blocos ----------


def test_juntar_blocos_faz_retangulos_maiores():
    X, _ = True, False
    grade = [
        [_, X, X, _],
        [_, X, X, _],
        [X, X, X, X],
    ]
    rects = carregador_fases.juntar_blocos(grade, 10)
    area = sum(r.w * r.h for r in rects)
    assert area == 8 * 100  # 8 blocos de 10×10, nada sobrando nem faltando
    assert pygame.Rect(10, 0, 20, 20) in rects  # os 4 de cima viraram um só
    assert len(rects) == 2


def test_superficies_sao_so_os_topos():
    X, _ = True, False
    grade = [
        [_, X, _],
        [X, X, X],
    ]
    sup = carregador_fases.achar_superficies(grade, 10)
    assert pygame.Rect(10, 0, 10, 10) in sup  # topo do bloco do meio
    assert pygame.Rect(0, 10, 10, 10) in sup  # topos dos lados, na linha de baixo
    assert pygame.Rect(20, 10, 10, 10) in sup
    assert len(sup) == 3  # o bloco embaixo do topo não é superfície


# ---------- alcance: dá para chegar em todo lugar? ----------


def alcance_do_pulo():
    """Altura e distância máximas de um pulo, pelo personagem que alcança menos."""
    alcances = []
    for chave in ("angel", "dark"):
        cfg = carregar_config(chave)
        v, g = cfg["forca_pulo"], cfg["gravidade"]
        altura = v**2 / (2 * g)
        distancia = (2 * v / g) * cfg["velocidade"]  # tempo no ar × velocidade
        alcances.append((altura * MARGEM, distancia * MARGEM))
    return min(a for a, _ in alcances), min(d for _, d in alcances)


def vao_horizontal(a: pygame.Rect, b: pygame.Rect) -> int:
    return max(0, max(a.left, b.left) - min(a.right, b.right))


def da_para_ir(de: pygame.Rect, para: pygame.Rect, altura_max: float, dist_max: float) -> bool:
    """Saindo de cima de `de`, dá para pousar em `para`?"""
    if vao_horizontal(de, para) > dist_max:
        return False
    subida = de.top - para.top
    return subida <= altura_max  # descer (subida negativa) sempre dá


def alcancaveis(fase: Fase) -> set[int]:
    """Percorre a fase como um jogador: parte de onde ele começa e marca tudo o que alcança."""
    altura_max, dist_max = alcance_do_pulo()
    sup = fase.superficies
    x, y = fase.inicio
    pe = pygame.Rect(x, y, 1, 40)
    primeira = pe.collidelist(sup)
    visitadas = {primeira}
    fila = [primeira]
    while fila:
        atual = sup[fila.pop()]
        for i, s in enumerate(sup):
            if i not in visitadas and da_para_ir(atual, s, altura_max, dist_max):
                visitadas.add(i)
                fila.append(i)
    return visitadas


def test_toda_superficie_da_floresta_e_alcancavel(floresta):
    visitadas = alcancaveis(floresta)
    faltando = [tuple(s) for i, s in enumerate(floresta.superficies) if i not in visitadas]
    assert not faltando, f"lugares impossíveis de alcançar: {faltando}"


def test_da_para_chegar_na_bandeira(floresta):
    altura_max, _ = alcance_do_pulo()
    visitadas = alcancaveis(floresta)
    perto = [
        s
        for i, s in enumerate(floresta.superficies)
        if i in visitadas
        and vao_horizontal(s, floresta.chegada) == 0
        and 0 <= s.top - floresta.chegada.bottom <= altura_max
    ]
    assert perto, "nenhum chão alcançável embaixo da bandeira"


def test_o_teste_de_alcance_reprova_lugar_impossivel():
    """Confere que o próprio teste funciona: uma plataforma alta demais é pega."""
    fase = Fase.de_dados(
        {
            "tamanho": [2000, 1000],
            "inicio": [50, 900],
            "chegada": [1900, 850, 20, 50],
            "plataformas": [[0, 900, 2000, 100], [300, 500, 100, 20]],  # 400 px acima
        }
    )
    assert alcancaveis(fase) == {0}


# ---------- perigos e checkpoints da Floresta ----------


def test_floresta_tem_espinhos_e_um_checkpoint_no_meio(floresta):
    assert len(floresta.perigos) >= 4
    assert len(floresta.checkpoints) == 1
    meio = floresta.largura / 2
    assert abs(floresta.checkpoints[0].rect.centerx - meio) < floresta.largura * 0.1
    assert floresta.desenho_frente is not None  # a água


def test_area_de_dano_do_espinho_e_so_a_parte_de_baixo(floresta):
    bloco = 18 * ESCALA
    for p in floresta.perigos:
        assert p.height < bloco / 2
        assert p.width < bloco


def test_checkpoints_ficam_em_chao_alcancavel(floresta):
    visitadas = alcancaveis(floresta)
    for c in floresta.checkpoints:
        x, y = c.pes
        embaixo = pygame.Rect(x, y, 1, 4).collidelist(floresta.superficies)
        assert embaixo in visitadas, f"checkpoint em {c.pes} não está num chão alcançável"


def test_ponto_de_volta_e_o_ultimo_checkpoint_ativo(floresta):
    assert floresta.ponto_de_volta() == floresta.inicio
    (checkpoint,) = floresta.checkpoints
    floresta.ativar_checkpoints(pygame.Rect(checkpoint.rect.centerx - 100, 0, 32, 48))
    assert floresta.ponto_de_volta() == floresta.inicio  # ainda não passou
    floresta.ativar_checkpoints(pygame.Rect(checkpoint.rect.centerx + 10, 0, 32, 48))
    assert floresta.ponto_de_volta() == checkpoint.pes
    for c in floresta.checkpoints:  # não deixa o estado vazar para outros testes
        c.ativo = False
