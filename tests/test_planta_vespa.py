"""Testes da planta (ritmo, aviso, sementes) e da vespa (zigue-zague), sozinhas, na cena
e no mapa da Floresta."""

import pygame
import pytest

from jogo import inimigos
from jogo.cenas.cena_fase import CenaFase
from jogo.fases import carregador_fases
from jogo.fases.fase import Fase
from jogo.inimigos.planta import EstadoPlanta, Planta
from jogo.inimigos.vespa import Vespa
from jogo.nucleo import config
from jogo.personagens.angel import Angel

DT = 1 / 60
CHAO = pygame.Rect(0, 1000, 3000, 80)
LONGE = pygame.Rect(-5000, -5000, 10, 10)  # jogador fora da vista
PERTO = pygame.Rect(400, 952, 32, 48)  # jogador no chão, à esquerda da planta


def planta(propriedades=None):
    p = Planta.criar(pygame.Rect(600, 964, 36, 36), propriedades)
    p.atualizar(DT, [CHAO], LONGE)  # assenta no chão
    return p


def rodar(inimigo, segundos, alvo=PERTO, solidos=(CHAO,)):
    """Roda e devolve em que segundo saiu cada semente."""
    tiros = []
    for i in range(round(segundos * 60)):
        inimigo.atualizar(DT, list(solidos), alvo)
        if inimigo.disparos:
            tiros.append((i + 1) * DT)
            inimigo.disparos.clear()
    return tiros


# ---------- planta: ritmo e aviso ----------


def test_planta_dorme_com_o_jogador_longe():
    p = planta()
    assert rodar(p, 10, alvo=LONGE) == []
    assert p.estado == EstadoPlanta.ESPERA


def test_planta_atira_em_ritmo_fixo():
    p = planta()
    tiros = rodar(p, 10)
    ciclo = p.cfg["tempo_espera"] + p.cfg["tempo_aviso"]
    assert tiros[0] == pytest.approx(ciclo, abs=2 * DT)
    intervalos = [b - a for a, b in zip(tiros, tiros[1:], strict=False)]
    assert len(intervalos) >= 3
    for intervalo in intervalos:
        assert intervalo == pytest.approx(ciclo, abs=2 * DT)  # sempre o mesmo ritmo


def test_todo_tiro_tem_aviso_antes_inchando_e_vermelha():
    p = planta()
    quadros_avisando = 0
    cor_normal = p.cor_atual()
    for _ in range(60 * 8):
        avisando = p.estado == EstadoPlanta.AVISO
        p.atualizar(DT, [CHAO], PERTO)
        if p.disparos:
            # Antes de cada tiro, ficou avisando o tempo todo do aviso.
            assert avisando
            assert quadros_avisando >= round(p.cfg["tempo_aviso"] * 60) - 1
            p.disparos.clear()
            quadros_avisando = 0
        elif p.estado == EstadoPlanta.AVISO:
            quadros_avisando += 1
            assert p.cor_atual() != cor_normal  # mudou de cor
    # E incha: no fim do aviso, o desenho é maior que o corpo.
    p.estado, p.cronometro = EstadoPlanta.AVISO, 0.01
    desenho = p.forma_desenho(pygame.Rect(p.rect))
    assert desenho.width > p.rect.width and desenho.bottom == p.rect.bottom


def test_aviso_comecado_sempre_termina_em_tiro():
    p = planta()
    p.estado, p.cronometro = EstadoPlanta.AVISO, p.cfg["tempo_aviso"]
    assert len(rodar(p, 1, alvo=LONGE)) == 1  # o jogador fugiu, mas o tiro avisado sai


def test_planta_nao_anda():
    p = planta()
    x = p.rect.x
    rodar(p, 5)
    assert p.rect.x == x and p.no_chao


def test_semente_sai_da_boca_para_o_lado_em_que_ela_olha():
    p = planta()
    p.cuspir()
    semente = p.disparos[0]
    assert semente.vel_x < 0
    assert semente.rect.centerx == p.rect.left
    assert p.rect.top < semente.rect.centery < p.rect.bottom

    virada = planta({"olhando": "direita"})
    virada.cuspir()
    assert virada.disparos[0].vel_x > 0
    assert virada.disparos[0].rect.centerx == virada.rect.right


def test_semente_bate_na_altura_de_quem_esta_em_pe():
    p = planta()
    p.cuspir()
    semente = p.disparos[0]
    em_pe = pygame.Rect(0, CHAO.top - 48, 32, 48)
    assert em_pe.top < semente.rect.top and semente.rect.bottom < em_pe.bottom


# ---------- vespa: zigue-zague ----------


def vespa():
    return Vespa.criar(pygame.Rect(1000, 600, 200, 180))


def test_vespa_nasce_no_meio_do_territorio_e_nao_cai():
    v = vespa()
    assert v.rect.center == v.area.center
    rodar(v, 3, alvo=LONGE)
    assert v.area.contains(v.rect)  # sem gravidade: continua no ar


def test_vespa_voa_em_zigue_zague_sem_sair_do_territorio():
    v = vespa()
    viradas_x = viradas_y = 0
    vx, vy = v.vel_x, v.vel_y
    for _ in range(60 * 20):
        v.atualizar(DT, [CHAO], LONGE)
        assert v.area.contains(v.rect)
        viradas_x += (v.vel_x > 0) != (vx > 0)
        viradas_y += (v.vel_y > 0) != (vy > 0)
        vx, vy = v.vel_x, v.vel_y
        assert abs(v.vel_x) == v.cfg["velocidade_x"]  # velocidade constante: legível
        assert abs(v.vel_y) == v.cfg["velocidade_y"]
    assert viradas_x >= 4  # vai e volta na horizontal...
    assert viradas_y > viradas_x  # ...e sobe e desce mais vezes: zigue-zague
    assert v.olhando == (1 if v.vel_x > 0 else -1)  # olha para onde voa


def test_vespa_repete_sempre_o_mesmo_caminho():
    a, b = vespa(), vespa()
    caminho_a = []
    for _ in range(60 * 6):
        a.atualizar(DT, [], LONGE)
        caminho_a.append(a.rect.topleft)
    b.atualizar(DT, [], LONGE)
    b.reiniciar()  # reiniciar volta para o começo do mesmo desenho
    caminho_b = []
    for _ in range(60 * 6):
        b.atualizar(DT, [], LONGE)
        caminho_b.append(b.rect.topleft)
    assert caminho_a == caminho_b


def test_vespa_pisada_cai_e_some():
    v = vespa()
    y = v.rect.y
    v.derrotar()
    rodar(v, 0.3, alvo=LONGE)
    assert v.rect.y > y
    rodar(v, 1, alvo=LONGE)
    assert v.sumiu


# ---------- na cena: dano, pisão e sementes ----------


class JogoFalso:
    def __init__(self):
        self.cfg = config.carregar("jogo")

    def ir_para_escolha(self, ultimo=None):
        pass

    def iniciar_fase(self, classe):
        pass


def cena_com(*lugares):
    fase = Fase.de_dados(
        {
            "tamanho": [3000, 1080],
            "inicio": [100, 1000],
            "chegada": [2900, 900, 30, 100],
            "plataformas": [[0, 1000, 3000, 80]],
            "inimigos": [list(lugar) for lugar in lugares],
        }
    )
    c = CenaFase(JogoFalso(), Angel, "teste", fase=fase)
    c.atualizar(DT, [])
    return c


def por_jogador(c, x, pes):
    p = c.personagem
    p.x, p.y = float(x), float(pes - p.rect.height)
    p._sincronizar_rect()


def test_semente_acerta_o_jogador_tira_um_coracao_e_some():
    c = cena_com(["planta", 900, 964, 36, 36])
    por_jogador(c, 600, 1000)  # parado no chão, na mira
    for _ in range(60 * 4):
        c.atualizar(DT, [])
        if c.personagem.vida.coracoes < 3:
            break
    assert c.personagem.vida.coracoes == 2
    assert c.personagem.vel_x < 0  # empurrado para longe da semente
    assert c.projeteis == []  # a semente sumiu ao acertar


def test_semente_some_na_parede():
    c = cena_com(["planta", 900, 964, 36, 36])
    c.fase.plataformas.append(pygame.Rect(700, 900, 36, 100))  # parede entre os dois
    por_jogador(c, 500, 1000)
    for _ in range(60 * 4):
        c.atualizar(DT, [])
    assert c.personagem.vida.coracoes == 3  # a parede protegeu
    assert all(pr.rect.left > 700 for pr in c.projeteis)


def test_pular_a_semente_nao_machuca():
    c = cena_com(["planta", 900, 964, 36, 36])
    planta_ = c.inimigos[0]
    por_jogador(c, 600, 1000)
    planta_.cuspir()  # semente nova, saindo agora
    c.atualizar(DT, [])
    c.personagem.vel_y = -620  # pulou
    c.personagem.no_chao = False
    for _ in range(50):
        c.atualizar(DT, [])
    assert c.personagem.vida.coracoes == 3


def test_pisar_na_planta_derrota_e_quica():
    c = cena_com(["planta", 900, 964, 36, 36])
    pl = c.inimigos[0]
    por_jogador(c, pl.rect.centerx - 16, pl.rect.top - 4)
    c.personagem.vel_y = 300.0
    c.atualizar(DT, [])
    assert not pl.vivo
    assert c.personagem.vel_y < 0
    assert c.personagem.vida.coracoes == 3
    assert rodar(pl, 5) == []  # pisada não atira mais


def test_encostar_na_planta_de_lado_machuca():
    c = cena_com(["planta", 900, 964, 36, 36])
    pl = c.inimigos[0]
    por_jogador(c, pl.rect.left - 30, 1000)
    c.atualizar(DT, [])
    c.atualizar(DT, [])
    assert c.personagem.vida.coracoes == 2


def test_pisar_na_vespa_derrota_e_quica():
    c = cena_com(["vespa", 900, 800, 200, 180])
    v = c.inimigos[0]
    por_jogador(c, v.rect.centerx - 16, v.rect.top - 2)
    c.personagem.vel_y = 300.0
    c.atualizar(DT, [])
    assert not v.vivo
    assert c.personagem.vel_y < 0
    assert c.personagem.vida.coracoes == 3


def test_encostar_na_vespa_machuca():
    c = cena_com(["vespa", 900, 800, 200, 180])
    v = c.inimigos[0]
    c.personagem.vel_y = -100.0  # subindo: não é pisão
    por_jogador(c, v.rect.centerx - 16, v.rect.bottom + 10)
    c.atualizar(DT, [])
    assert c.personagem.vida.coracoes == 2


def test_perder_vida_limpa_as_sementes_e_traz_a_planta_de_volta():
    c = cena_com(["planta", 900, 964, 36, 36])
    c.inimigos[0].cuspir()
    c.inimigos[0].derrotar()
    c.atualizar(DT, [])
    assert c.projeteis
    c.personagem.y = 2000.0
    c.personagem._sincronizar_rect()
    c.atualizar(DT, [])
    assert c.projeteis == []
    assert c.inimigos[0].vivo


def test_cena_desenha_planta_vespa_e_sementes():
    c = cena_com(["planta", 900, 964, 36, 36], ["vespa", 1200, 800, 200, 180])
    tela = pygame.Surface((960, 540))
    c.inimigos[0].estado = EstadoPlanta.AVISO
    c.inimigos[0].cuspir()
    c.atualizar(DT, [])
    c.desenhar(tela)
    for inimigo in c.inimigos:
        inimigo.derrotar()
    c.desenhar(tela)


# ---------- no mapa da Floresta ----------

TELA = 960


@pytest.fixture(scope="module")
def floresta():
    return carregador_fases.carregar("01_floresta", 2)


def do_tipo(fase, tipo):
    return [i for i in fase.inimigos if i.tipo == tipo]


def test_floresta_tem_7_inimigos_nos_lugares_combinados(floresta):
    tela = {
        tipo: [i.area.centerx // TELA + 1 for i in do_tipo(floresta, tipo)]
        for tipo in ("javali", "planta", "vespa")
    }
    assert tela == {"javali": [2, 4, 5], "planta": [3, 5], "vespa": [4, 6]}
    assert not [i for i in floresta.inimigos if i.area.centerx < TELA]  # tela 1 livre


def test_volta_de_vida_nao_cai_dentro_de_inimigo(floresta):
    pontos = [floresta.inicio] + [c.pes for c in floresta.checkpoints]
    for lugar in floresta.inimigos:
        perto = lugar.area.inflate(128, 128)  # 64 px de folga para cada lado
        for x, y in pontos:
            assert not perto.collidepoint(x, y - 24), (lugar.tipo, lugar.area)


def test_territorio_das_vespas_fica_no_ar_livre(floresta):
    for lugar in do_tipo(floresta, "vespa"):
        assert lugar.area.collidelist(floresta.solidos) == -1, lugar.area


def test_vespas_da_floresta_dao_para_passar_por_baixo_e_para_pisar(floresta):
    """Em parte do caminho ela fica acima da cabeça (dá para passar) e em parte
    desce até onde o pulo alcança (dá para pisar)."""
    for lugar in do_tipo(floresta, "vespa"):
        v = inimigos.criar("vespa", lugar.area)
        cabeca = lugar.area.bottom - 48  # jogador em pé no chão embaixo dela
        alturas = []
        for _ in range(60 * 10):
            v.atualizar(DT, floresta.solidos, LONGE)
            alturas.append(v.rect.bottom)
        assert min(alturas) < cabeca - 40
        assert max(alturas) > cabeca


def test_plantas_da_floresta_ficam_no_chao(floresta):
    for lugar in do_tipo(floresta, "planta"):
        p = inimigos.criar("planta", lugar.area, lugar.propriedades)
        rodar(p, 2, alvo=LONGE, solidos=floresta.solidos)
        assert p.no_chao
        assert p.rect.collidelist(floresta.solidos) == -1


def test_semente_da_primeira_planta_some_antes_do_buraco_com_agua(floresta):
    """Ensinar sem castigo: o empurrão da semente não joga ninguém na água."""
    lugar = do_tipo(floresta, "planta")[0]
    p = inimigos.criar("planta", lugar.area, lugar.propriedades)
    p.cuspir()
    semente = p.disparos[0]
    menor_x = semente.rect.left
    while semente.ativo:
        semente.atualizar(DT, floresta.solidos)
        menor_x = min(menor_x, semente.rect.left)
    agua_fim = 60 * 36  # o buraco da tela 3 vai até a coluna 59
    assert menor_x > agua_fim + 36
