"""Cena de uma fase: personagem, inimigos, projéteis, câmera, fundo, perigos, vidas e chegada."""

from enum import Enum

import pygame

from jogo import inimigos
from jogo.cenas.cena import Cena
from jogo.fases import carregador_fases
from jogo.fases.camera import Camera
from jogo.fases.fundo import Fundo
from jogo.interface.hud import Hud
from jogo.nucleo import config
from jogo.nucleo.controles import ler_comandos

TEMPO_MENSAGEM = 2.0  # segundos mostrando "Fase concluída!" ou "Game Over"
AJUDA = "Setas/A D: andar   Espaço/W: pular   Esc: trocar personagem"


class EstadoFase(Enum):
    """Máquina de estados da cena: o que a fase está fazendo agora."""

    JOGANDO = "jogando"
    CONCLUIDA = "concluida"
    FIM_DE_JOGO = "fim_de_jogo"


class CenaFase(Cena):
    def __init__(self, jogo, classe_personagem, nome_fase: str, fase=None):
        """`fase` pronta é opcional (os testes usam fases simples, sem Tiled)."""
        super().__init__(jogo)
        self.cores = {k: tuple(v) for k, v in jogo.cfg["cores"].items()}
        janela = jogo.cfg["janela"]
        tela = (janela["largura"], janela["altura"])

        self.fase = fase or carregador_fases.carregar(nome_fase, jogo.cfg["mapa"]["escala"])
        self.personagem = classe_personagem.criar((0, 0))
        self.camera = Camera(jogo.cfg["camera"], tela, self.fase.tamanho)
        self.inimigos = [inimigos.criar(i.tipo, i.area, i.propriedades) for i in self.fase.inimigos]
        self.projeteis = []  # sementes (e depois flechas, bolas de fogo...) voando agora
        self._colocar_personagem(self.fase.inicio)

        cfg_fase = config.carregar("fases").get(nome_fase, {})
        cam_y_max = self.fase.altura - tela[1]
        self.fundo = Fundo(cfg_fase["fundo"], tela, cam_y_max) if "fundo" in cfg_fase else None
        self.titulo = cfg_fase.get("nome", self.fase.nome or nome_fase)
        self.hud = Hud(jogo.cfg["hud"], self.cores)

        self.estado = EstadoFase.JOGANDO
        self.tempo_mensagem = 0.0
        self.fonte_grande = pygame.font.Font(None, 64)

    # ---------- regras ----------

    def _colocar_personagem(self, pes: tuple[int, int]) -> None:
        """Põe o personagem com os pés em `pes`, parado, e leva a câmera junto."""
        p = self.personagem
        p.inicio = (pes[0] - p.rect.width // 2, pes[1] - p.rect.height)
        p.reiniciar()
        self.camera.centralizar(p.rect, p.olhando)

    def _perder_vida(self) -> None:
        if self.personagem.vida.perder_vida():
            self._colocar_personagem(self.fase.ponto_de_volta())
            for inimigo in self.inimigos:  # voltam todos, até os derrotados
                inimigo.reiniciar()
            self.projeteis.clear()  # recomeça o trecho sem semente no ar
        else:
            self.estado = EstadoFase.FIM_DE_JOGO

    def atualizar(self, dt: float, eventos: list[pygame.event.Event]) -> None:
        if any(e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE for e in eventos):
            self.jogo.ir_para_escolha(type(self.personagem))
            return

        if self.estado != EstadoFase.JOGANDO:
            antes = self.tempo_mensagem
            self.tempo_mensagem += dt
            if antes < TEMPO_MENSAGEM <= self.tempo_mensagem:  # só no quadro em que o tempo acaba
                if self.estado == EstadoFase.FIM_DE_JOGO:
                    # Game Over: recomeça a mesma fase do início (decisão de 28/11).
                    self.jogo.iniciar_fase(type(self.personagem))
                else:
                    self.jogo.ir_para_escolha(type(self.personagem))
            return

        p = self.personagem
        pes_antes = p.rect.bottom  # para saber se ele veio de cima ao encostar num inimigo
        p.atualizar(dt, ler_comandos(eventos), self.fase.solidos)
        self.fase.ativar_checkpoints(p.rect)
        self._inimigos(dt, pes_antes)
        self._projeteis(dt)

        perigo = self.fase.perigo_tocado(p.rect)
        if perigo is not None:
            p.levar_dano(perigo.centerx)

        if self.fase.caiu_para_fora(p.rect) or p.vida.sem_coracoes:
            self._perder_vida()
        elif self.fase.chegou(p.rect):
            self.estado = EstadoFase.CONCLUIDA
        else:
            self.camera.atualizar(dt, p.rect, p.olhando, p.no_chao)

    def _inimigos(self, dt: float, pes_antes: float) -> None:
        """Move os inimigos e resolve o contato: pisão derrota, encostar de lado machuca."""
        p = self.personagem
        cfg_geral = None
        for inimigo in self.inimigos:
            inimigo.atualizar(dt, self.fase.solidos, p.rect)
            self.projeteis.extend(inimigo.disparos)  # a cena passa a cuidar do que foi atirado
            inimigo.disparos.clear()
            if inimigo.foi_pisado(pes_antes, p.vel_y, p.rect):
                inimigo.derrotar()
                cfg_geral = inimigo.cfg
            elif inimigo.machuca(p.rect):
                p.levar_dano(inimigo.rect.centerx)
        if cfg_geral is not None:  # pulinho uma vez só, mesmo pisando em dois
            p.quicar(cfg_geral["quique"])

    def _projeteis(self, dt: float) -> None:
        """Move os projéteis; quem acerta o personagem tira 1 coração e some."""
        p = self.personagem
        for projetil in self.projeteis:
            projetil.atualizar(dt, self.fase.solidos)
            if projetil.acertou(p.rect):
                p.levar_dano(projetil.rect.centerx)
        self.projeteis = [pr for pr in self.projeteis if pr.ativo]

    # ---------- desenho ----------

    def desenhar(self, tela: pygame.Surface) -> None:
        if self.fundo:
            self.fundo.desenhar(tela, self.camera)
        else:
            tela.fill(self.cores["fundo"])
        self.fase.desenhar(tela, self.cores, self.camera)
        for inimigo in self.inimigos:
            inimigo.desenhar(tela, self.camera)
        for projetil in self.projeteis:
            projetil.desenhar(tela, self.camera)
        self.personagem.desenhar(tela, self.camera)
        self.fase.desenhar_frente(tela, self.camera)

        # O HUD fica fixo na tela: não usa a câmera.
        self.hud.desenhar(
            tela, self.personagem.vida, f"{self.titulo} - {self.personagem.nome}", AJUDA
        )

        mensagens = {EstadoFase.CONCLUIDA: "Fase concluída!", EstadoFase.FIM_DE_JOGO: "Game Over"}
        if self.estado in mensagens:
            imagem = self.fonte_grande.render(
                mensagens[self.estado], True, self.cores["destaque"], self.cores["caixa"]
            )
            tela.blit(imagem, imagem.get_rect(center=tela.get_rect().center))
