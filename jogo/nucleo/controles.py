"""Tradução do teclado em comandos do jogo.

O personagem não sabe quais teclas existem: ele só recebe "esquerda", "pular" etc.
Assim dá para trocar teclas, ligar um controle de videogame ou simular comandos
nos testes sem mexer no personagem.
"""

from dataclasses import dataclass

import pygame

TECLAS_ESQUERDA = (pygame.K_LEFT, pygame.K_a)
TECLAS_DIREITA = (pygame.K_RIGHT, pygame.K_d)
TECLAS_PULO = (pygame.K_SPACE, pygame.K_UP, pygame.K_w)


@dataclass
class Comandos:
    esquerda: bool = False
    direita: bool = False
    pulo_apertado: bool = False  # verdadeiro só no quadro em que a tecla desceu
    pulo_segurado: bool = False  # verdadeiro enquanto a tecla está pressionada


def ler_comandos(eventos: list[pygame.event.Event]) -> Comandos:
    teclas = pygame.key.get_pressed()
    return Comandos(
        esquerda=any(teclas[t] for t in TECLAS_ESQUERDA),
        direita=any(teclas[t] for t in TECLAS_DIREITA),
        pulo_apertado=any(e.type == pygame.KEYDOWN and e.key in TECLAS_PULO for e in eventos),
        pulo_segurado=any(teclas[t] for t in TECLAS_PULO),
    )
