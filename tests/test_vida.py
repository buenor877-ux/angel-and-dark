"""Sistema de vida: corações, vidas, invulnerabilidade, empurrão, checkpoints e fim de jogo."""

import pygame
import pytest

from jogo.cenas.cena_fase import CenaFase, EstadoFase
from jogo.fases.fase import Fase
from jogo.nucleo import config
from jogo.nucleo.controles import Comandos
from jogo.personagens.angel import Angel
from jogo.personagens.vida import Vida

DT = 1 / 60


@pytest.fixture
def cfg_vida():
    return config.carregar("personagens")["vida"]


# ---------- a classe Vida, sozinha ----------


def test_comeca_com_3_coracoes_e_3_vidas(cfg_vida):
    vida = Vida(cfg_vida)
    assert (vida.coracoes, vida.vidas) == (3, 3)


def test_dano_tira_um_coracao_e_deixa_invulneravel(cfg_vida):
    vida = Vida(cfg_vida)
    assert vida.levar_dano()
    assert vida.coracoes == 2
    assert vida.invulneravel
    assert not vida.levar_dano()  # segundo dano logo em seguida é ignorado
    assert vida.coracoes == 2


def test_invulnerabilidade_acaba_depois_de_1_5_segundos(cfg_vida):
    vida = Vida(cfg_vida)
    vida.levar_dano()
    for _ in range(int(1.4 / DT)):
        vida.atualizar(DT)
    assert vida.invulneravel
    for _ in range(int(0.2 / DT)):
        vida.atualizar(DT)
    assert not vida.invulneravel
    assert vida.levar_dano()


def test_pisca_enquanto_invulneravel(cfg_vida):
    vida = Vida(cfg_vida)
    vida.levar_dano()
    visivel = set()
    for _ in range(30):
        vida.atualizar(DT)
        visivel.add(vida.visivel)
    assert visivel == {True, False}


def test_perder_vida_recupera_os_coracoes(cfg_vida):
    vida = Vida(cfg_vida)
    vida.levar_dano()
    assert vida.perder_vida()
    assert (vida.coracoes, vida.vidas) == (3, 2)
    assert not vida.invulneravel


def test_perder_a_ultima_vida_avisa(cfg_vida):
    vida = Vida(cfg_vida)
    assert vida.perder_vida()
    assert vida.perder_vida()
    assert not vida.perder_vida()  # acabaram
    assert vida.vidas == 0


# ---------- o personagem levando dano ----------

CHAO = pygame.Rect(0, 500, 2000, 40)


def angel_no_chao():
    a = Angel.criar((500, 450))
    for _ in range(30):
        a.atualizar(DT, Comandos(), [CHAO])
    return a


def test_dano_empurra_para_longe_do_perigo():
    a = angel_no_chao()
    x0 = a.rect.centerx
    assert a.levar_dano(origem_x=x0 - 50)  # perigo à esquerda
    assert a.vel_x > 0 and a.vel_y < 0  # vai para a direita e para cima
    for _ in range(10):
        a.atualizar(DT, Comandos(esquerda=True), [CHAO])  # tenta voltar
    assert a.rect.centerx > x0  # durante o empurrão o controle não responde


def test_controle_volta_depois_do_empurrao():
    a = angel_no_chao()
    a.levar_dano(origem_x=a.rect.centerx - 50)
    for _ in range(30):  # meio segundo: o empurrão já passou
        a.atualizar(DT, Comandos(), [CHAO])
    x = a.rect.x
    for _ in range(20):
        a.atualizar(DT, Comandos(esquerda=True), [CHAO])
    assert a.rect.x < x


# ---------- regras da fase ----------


class JogoFalso:
    def __init__(self):
        self.cfg = config.carregar("jogo")
        self.pedidos = []

    def ir_para_escolha(self, ultimo=None):
        self.pedidos.append(("escolha", ultimo))


def fase_simples():
    """Chão comprido, um espinho e um checkpoint no meio."""
    return Fase.de_dados(
        {
            "tamanho": [3000, 1080],
            "inicio": [100, 1000],
            "chegada": [2900, 900, 30, 100],
            "plataformas": [[0, 1000, 3000, 80]],
            "perigos": [[700, 990, 30, 10]],
            "checkpoints": [[1500, 964, 36, 36]],
        }
    )


def cena():
    return CenaFase(JogoFalso(), Angel, "teste", fase=fase_simples())


def mover(c, x):
    p = c.personagem
    p.x = float(x)
    p._sincronizar_rect()


def rodar(c, quadros):
    for _ in range(quadros):
        c.atualizar(DT, [])


def test_encostar_no_espinho_tira_um_coracao():
    c = cena()
    rodar(c, 10)
    mover(c, 700)
    rodar(c, 2)
    assert c.personagem.vida.coracoes == 2


def test_zerar_os_coracoes_perde_uma_vida_e_volta_ao_inicio():
    c = cena()
    rodar(c, 10)
    p = c.personagem
    p.vida.coracoes = 1
    mover(c, 700)
    rodar(c, 2)
    assert p.vida.vidas == 2
    assert p.vida.coracoes == 3
    assert abs(p.rect.centerx - 100) < 5  # de volta ao início


def test_passar_no_checkpoint_muda_o_ponto_de_volta():
    c = cena()
    rodar(c, 10)
    mover(c, 1600)  # passou do checkpoint (x 1500)
    rodar(c, 2)
    assert c.fase.checkpoints[0].ativo
    c.personagem.y = 2000.0  # cai para fora do mundo
    c.personagem._sincronizar_rect()
    rodar(c, 1)
    assert c.personagem.vida.vidas == 2
    assert abs(c.personagem.rect.centerx - c.fase.checkpoints[0].pes[0]) < 5


def test_perder_as_3_vidas_mostra_fim_de_jogo_e_volta_a_escolha():
    c = cena()
    for _ in range(3):
        c.personagem.y = 2000.0
        c.personagem._sincronizar_rect()
        rodar(c, 1)
    assert c.estado == EstadoFase.FIM_DE_JOGO
    assert c.jogo.pedidos == []
    rodar(c, 130)  # pouco mais de 2 segundos
    assert c.jogo.pedidos == [("escolha", Angel)]


def test_fase_de_teste_desenha_com_perigo_e_checkpoint():
    c = cena()
    tela = pygame.Surface((960, 540))
    c.desenhar(tela)
    c.estado = EstadoFase.FIM_DE_JOGO
    c.desenhar(tela)
