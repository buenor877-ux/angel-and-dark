"""Corações, vidas e invulnerabilidade (sistema aprovado em 28/11, docs/03).

- Levou dano: perde 1 coração, fica piscando e invulnerável por um tempo.
- Zerou os corações (ou caiu num buraco): perde 1 vida e volta ao checkpoint.
- Perdeu todas as vidas: fim de jogo.

Esta classe só guarda números e cronômetros; não desenha nem mexe no personagem.
"""


class Vida:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.max_coracoes = cfg["coracoes"]
        self.coracoes = self.max_coracoes
        self.vidas = cfg["vidas"]
        self.tempo_invulneravel = 0.0
        self.tempo_sem_controle = 0.0

    @property
    def invulneravel(self) -> bool:
        return self.tempo_invulneravel > 0

    @property
    def sem_controle(self) -> bool:
        """Verdadeiro durante o empurrão: o jogador não controla o personagem."""
        return self.tempo_sem_controle > 0

    @property
    def sem_coracoes(self) -> bool:
        return self.coracoes <= 0

    @property
    def visivel(self) -> bool:
        """Pisca 10 vezes por segundo enquanto invulnerável."""
        return not self.invulneravel or int(self.tempo_invulneravel * 10) % 2 == 0

    def atualizar(self, dt: float) -> None:
        self.tempo_invulneravel = max(0.0, self.tempo_invulneravel - dt)
        self.tempo_sem_controle = max(0.0, self.tempo_sem_controle - dt)

    def levar_dano(self) -> bool:
        """Tira 1 coração. Devolve False se o dano foi ignorado (estava invulnerável)."""
        if self.invulneravel or self.sem_coracoes:
            return False
        self.coracoes -= 1
        self.tempo_invulneravel = self.cfg["tempo_invulneravel"]
        self.tempo_sem_controle = self.cfg["tempo_empurrao"]
        return True

    def perder_vida(self) -> bool:
        """Tira 1 vida e recupera os corações. Devolve False se acabaram as vidas."""
        self.vidas -= 1
        self.recuperar()
        return self.vidas > 0

    def recuperar(self) -> None:
        self.coracoes = self.max_coracoes
        self.tempo_invulneravel = 0.0
        self.tempo_sem_controle = 0.0
