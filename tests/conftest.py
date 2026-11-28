"""Preparação comum dos testes: pygame sem janela e sem som."""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402  (precisa vir depois das variáveis acima)
import pytest  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def pygame_iniciado():
    pygame.init()
    pygame.display.set_mode((1, 1))  # carregar imagens (convert) exige uma tela
    yield
    pygame.quit()
