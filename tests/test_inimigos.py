"""Testes dos inimigos: o javali (patrulha, aviso, investida), o pisão e o lugar no mapa."""

import pygame
import pytest

from jogo import inimigos
from jogo.cenas.cena_fase import CenaFase
from jogo.fases import carregador_fases
from jogo.fases.fase import Fase
from jogo.inimigos.javali import EstadoJavali, Javali
from jogo.nucleo import config
from jogo.personagens.angel import Angel

DT = 1 / 60
CHAO = pygame.Rect(0, 1000, 2000, 80)
LONGE = pygame.Rect(-5000, -5000, 10, 10)  # jogador fora da vista


def javali(area=(300, 980, 600, 20), solidos=(CHAO,)):
    j = Javali.criar(pygame.Rect(area))
    rodar(j, 1, list(solidos))  # assenta no chão
    return j


def rodar(j, quadros, solidos=(CHAO,), alvo=LONGE):
    for _ in range(quadros):
        j.atualizar(DT, list(solidos), alvo)


# ---------- patrulha ----------


def test_nasce_no_meio_da_area_com_os_pes_no_chao():
    j = javali()
    assert abs(j.rect.centerx - 600) <= 2  # já deu um passinho
    assert j.rect.bottom == 1000
    assert j.no_chao
    assert j.estado == EstadoJavali.PATRULHA


def test_patrulha_vira_no_fim_da_area_e_nunca_sai_dela():
    j = javali()
    viradas = 0
    olhando = j.olhando
    for _ in range(60 * 30):  # 30 segundos
        rodar(j, 1)
        assert j.area.left <= j.rect.left and j.rect.right <= j.area.right
        if j.olhando != olhando:
            viradas += 1
            olhando = j.olhando
    assert viradas >= 2  # foi e voltou


def test_patrulha_vira_na_borda_do_chao():
    plataforma = pygame.Rect(400, 1000, 300, 40)  # chão curto, área maior que ele
    j = javali(area=(0, 980, 1100, 20), solidos=(plataforma,))
    for _ in range(60 * 20):
        rodar(j, 1, [plataforma])
        assert j.no_chao, "caiu da borda"


def test_patrulha_vira_na_parede():
    parede = pygame.Rect(500, 900, 36, 100)
    j = javali(area=(300, 980, 600, 20), solidos=(CHAO, parede))
    j.rect.left = parede.right + 1
    j.x = float(j.rect.x)
    j.olhando = -1
    rodar(j, 20, [CHAO, parede])
    assert j.olhando == 1


# ---------- vê, avisa e investe ----------


def jogador_em(x):
    return pygame.Rect(x, 952, 32, 48)


def test_ve_o_jogador_na_frente_mas_nao_atras():
    j = javali()  # olhando para a esquerda, no x 600
    assert j.ve(jogador_em(400))
    assert not j.ve(jogador_em(800))  # atrás
    assert not j.ve(jogador_em(100))  # longe demais
    assert not j.ve(pygame.Rect(400, 700, 32, 48))  # muito acima


def test_nao_ve_quem_vem_caindo_logo_acima_dele():
    j = javali()
    pes = j.rect.top - 5  # quase pisando, mas ainda acima da cabeça dele
    assert not j.ve(pygame.Rect(j.rect.left - 40, pes - 48, 32, 48))


def test_avisa_parado_e_depois_investe_rapido():
    j = javali()
    alvo = jogador_em(400)
    rodar(j, 1, alvo=alvo)
    assert j.estado == EstadoJavali.AVISO
    x = j.rect.x
    rodar(j, int(0.5 * 60), alvo=alvo)
    assert j.estado == EstadoJavali.AVISO
    assert j.rect.x == x  # parado durante o aviso
    assert j.deslocamento_desenho() != 0  # tremendo
    rodar(j, int(0.2 * 60), alvo=alvo)
    assert j.estado == EstadoJavali.INVESTIDA
    assert abs(j.vel_x) == j.cfg["velocidade_investida"]


def test_investida_para_no_fim_da_area_descansa_e_volta_a_patrulhar():
    j = javali()
    j.estado, j.cronometro = EstadoJavali.INVESTIDA, 0.0
    rodar(j, 60)  # 1 s a 330 px/s passa do fim da área
    assert j.rect.left == j.area.left
    assert j.estado == EstadoJavali.DESCANSO
    rodar(j, 60)
    assert j.estado == EstadoJavali.PATRULHA


def test_investida_nao_cai_na_borda():
    plataforma = pygame.Rect(400, 1000, 300, 40)
    j = javali(area=(0, 980, 1100, 20), solidos=(plataforma,))
    j.estado = EstadoJavali.INVESTIDA
    rodar(j, 90, [plataforma])
    assert j.no_chao
    assert j.estado in (EstadoJavali.DESCANSO, EstadoJavali.PATRULHA)


def test_reiniciar_volta_ao_comeco_vivo():
    j = javali()
    j.estado = EstadoJavali.INVESTIDA
    rodar(j, 30)
    j.derrotar()
    j.reiniciar()
    assert j.vivo and j.estado == EstadoJavali.PATRULHA
    assert j.rect.midbottom == j.area.midbottom


# ---------- pisão e dano, na cena ----------


class JogoFalso:
    def __init__(self):
        self.cfg = config.carregar("jogo")
        self.pedidos = []

    def ir_para_escolha(self, ultimo=None):
        self.pedidos.append(("escolha", ultimo))

    def iniciar_fase(self, classe):
        self.pedidos.append(("fase", classe))


def cena_com_javali():
    fase = Fase.de_dados(
        {
            "tamanho": [3000, 1080],
            "inicio": [100, 1000],
            "chegada": [2900, 900, 30, 100],
            "plataformas": [[0, 1000, 3000, 80]],
            "inimigos": [["javali", 900, 980, 400, 20]],
        }
    )
    c = CenaFase(JogoFalso(), Angel, "teste", fase=fase)
    for _ in range(5):
        c.atualizar(DT, [])
    return c


def por_jogador(c, x, pes):
    p = c.personagem
    p.x, p.y = float(x), float(pes - p.rect.height)
    p._sincronizar_rect()


def test_cair_em_cima_derrota_e_da_um_pulinho():
    c = cena_com_javali()
    j = c.inimigos[0]
    por_jogador(c, j.rect.centerx - 16, j.rect.top - 4)
    c.personagem.vel_y = 300.0  # caindo
    c.atualizar(DT, [])
    assert not j.vivo
    assert j.piscando_dano  # branco logo depois do pisão
    assert j.estado == EstadoJavali.PATRULHA  # não chegou a ficar vermelho (aviso)
    assert c.personagem.vel_y < 0  # quicou para cima
    assert c.personagem.vida.coracoes == 3  # sem dano


def test_encostar_de_lado_tira_um_coracao_e_empurra():
    c = cena_com_javali()
    j = c.inimigos[0]
    por_jogador(c, j.rect.left - 30, 1000)  # no chão, encostando pela esquerda
    c.atualizar(DT, [])
    c.atualizar(DT, [])
    assert j.vivo
    assert c.personagem.vida.coracoes == 2
    assert c.personagem.vel_x < 0  # empurrado para longe do javali


def test_derrotado_some_e_nao_machuca():
    c = cena_com_javali()
    j = c.inimigos[0]
    j.derrotar()
    for _ in range(60):
        c.atualizar(DT, [])
    assert j.sumiu
    por_jogador(c, j.rect.x, 1000)
    c.atualizar(DT, [])
    assert c.personagem.vida.coracoes == 3


def test_perder_uma_vida_traz_os_inimigos_de_volta():
    c = cena_com_javali()
    j = c.inimigos[0]
    j.derrotar()
    c.personagem.y = 2000.0  # cai para fora do mundo
    c.personagem._sincronizar_rect()
    c.atualizar(DT, [])
    assert c.personagem.vida.vidas == 2
    assert j.vivo


def test_cena_desenha_os_inimigos():
    c = cena_com_javali()
    tela = pygame.Surface((960, 540))
    c.inimigos[0].estado = EstadoJavali.AVISO
    c.desenhar(tela)
    c.inimigos[0].derrotar()
    c.desenhar(tela)


# ---------- no mapa da Floresta ----------

TELA = 960  # largura da tela, em pixels do jogo


@pytest.fixture(scope="module")
def floresta():
    return carregador_fases.carregar("01_floresta", 2)


def test_tipos_do_carregador_e_dos_inimigos_combinam():
    assert carregador_fases.TIPOS_INIMIGO == set(inimigos.TIPOS)


def test_floresta_tem_3_javalis_nas_telas_2_4_e_5(floresta):
    assert [i.tipo for i in floresta.inimigos] == ["javali"] * 3
    telas = [i.area.centerx // TELA + 1 for i in floresta.inimigos]
    assert telas == [2, 4, 5]


def test_nenhum_javali_perto_do_inicio_nem_do_checkpoint(floresta):
    pontos = [floresta.inicio[0]] + [c.rect.centerx for c in floresta.checkpoints]
    for lugar in floresta.inimigos:
        for x in pontos:
            assert lugar.area.left - x > 200 or x - lugar.area.right > 200


def test_cada_javali_patrulha_no_chao_sem_cair(floresta):
    for lugar in floresta.inimigos:
        j = inimigos.criar(lugar.tipo, lugar.area)
        for _ in range(60 * 20):
            j.atualizar(DT, floresta.solidos, LONGE)
            assert j.area.left <= j.rect.left and j.rect.right <= j.area.right
            assert j.no_chao, "caiu do chão"
        assert not j.rect.collidelistall(floresta.solidos)  # não ficou preso dentro de bloco
