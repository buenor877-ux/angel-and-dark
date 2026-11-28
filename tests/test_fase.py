"""Testes da fase de teste e das configurações."""

import pygame

from jogo.fases.fase import Fase
from jogo.nucleo import config
from jogo.personagens.personagem import carregar_config

MARGEM = 0.85  # regra de design: usar no máximo 85% do pulo


def fase_teste():
    return Fase(config.carregar("fase_teste"))


def test_configs_carregam():
    assert config.carregar("jogo")["janela"]["fps"] == 60
    assert {"movimento", "angel", "dark"} <= config.carregar("personagens").keys()


def test_fase_e_maior_que_a_tela_e_inicio_valido():
    fase = fase_teste()
    assert fase.largura >= 960 * 3
    x, y = fase.inicio
    assert 0 <= x < fase.largura and 0 <= y < fase.altura


def test_plataformas_e_chegada_dentro_do_mundo():
    fase = fase_teste()
    mundo = pygame.Rect(0, 0, fase.largura, fase.altura)
    for p in fase.plataformas + [fase.chegada]:
        assert mundo.contains(p), f"{tuple(p)} está fora do mundo"


def test_detecta_queda_para_fora():
    fase = fase_teste()
    assert not fase.caiu_para_fora(pygame.Rect(100, 900, 32, 48))
    assert fase.caiu_para_fora(pygame.Rect(100, fase.altura + 200, 32, 48))


def test_detecta_chegada():
    fase = fase_teste()
    assert fase.chegou(fase.chegada.copy())
    assert not fase.chegou(pygame.Rect(*fase.inicio, 32, 48))


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
    """Percorre a fase como um jogador: parte do chão e marca tudo o que alcança."""
    altura_max, dist_max = alcance_do_pulo()
    plats = fase.plataformas
    chao = max(p.top for p in plats)
    visitadas = {i for i, p in enumerate(plats) if p.top == chao}
    fila = list(visitadas)
    while fila:
        atual = plats[fila.pop()]
        for i, p in enumerate(plats):
            if i not in visitadas and da_para_ir(atual, p, altura_max, dist_max):
                visitadas.add(i)
                fila.append(i)
    return visitadas


def test_toda_plataforma_e_alcancavel():
    fase = fase_teste()
    visitadas = alcancaveis(fase)
    faltando = [tuple(p) for i, p in enumerate(fase.plataformas) if i not in visitadas]
    assert not faltando, f"plataformas impossíveis de alcançar: {faltando}"


def test_o_teste_de_alcance_reprova_plataforma_impossivel():
    """Confere que o próprio teste funciona: uma plataforma alta demais é pega."""
    dados = config.carregar("fase_teste")
    dados["plataformas"] = dados["plataformas"] + [[100, 600, 100, 20]]  # 440 px acima do chão
    fase = Fase(dados)
    assert len(fase.plataformas) - 1 not in alcancaveis(fase)
