"""Testes da fase de teste e das configurações."""

import pygame

from jogo.fases.fase import Fase
from jogo.nucleo import config
from jogo.personagens.personagem import carregar_config


def test_configs_carregam():
    assert config.carregar("jogo")["janela"]["fps"] == 60
    assert {"movimento", "angel", "dark"} <= config.carregar("personagens").keys()


def test_fase_teste_tem_chao_e_inicio_valido():
    fase = Fase(config.carregar("fase_teste"), altura_tela=540)
    assert len(fase.plataformas) >= 2
    x, y = fase.inicio
    assert 0 <= x < 960 and 0 <= y < 540


MARGEM = 0.85  # regra de design: usar no máximo 85% do pulo


def alcance_do_pulo():
    """Altura e distância máximas de um pulo, calculadas pela física da config."""
    alcances = []
    for chave in ("angel", "dark"):
        cfg = carregar_config(chave)
        v, g = cfg["forca_pulo"], cfg["gravidade"]
        altura = v**2 / (2 * g)
        distancia = (2 * v / g) * cfg["velocidade"]  # tempo no ar × velocidade
        alcances.append((altura * MARGEM, distancia * MARGEM))
    # A fase precisa funcionar para os dois: vale o pulo de quem alcança menos.
    return min(a for a, _ in alcances), min(d for _, d in alcances)


def vao_horizontal(a: pygame.Rect, b: pygame.Rect) -> int:
    return max(0, max(a.left, b.left) - min(a.right, b.right))


def test_toda_plataforma_e_alcancavel():
    """Cada plataforma precisa ter, abaixo dela, uma superfície de onde dê para pular até ela."""
    fase = Fase(config.carregar("fase_teste"), altura_tela=540)
    altura_max, distancia_max = alcance_do_pulo()
    chao = max(p.top for p in fase.plataformas)
    for alvo in fase.plataformas:
        if alvo.top == chao:
            continue
        alcancavel = any(
            0 < base.top - alvo.top <= altura_max and vao_horizontal(base, alvo) <= distancia_max
            for base in fase.plataformas
            if base is not alvo
        )
        assert alcancavel, (
            f"plataforma {tuple(alvo)} não é alcançável (pulo máx. {altura_max:.0f} px)"
        )


def test_detecta_queda_para_fora():
    fase = Fase(config.carregar("fase_teste"), altura_tela=540)
    assert not fase.caiu_para_fora(pygame.Rect(100, 400, 32, 48))
    assert fase.caiu_para_fora(pygame.Rect(100, 700, 32, 48))
