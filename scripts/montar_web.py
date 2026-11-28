"""Monta a versão para navegador (itch.io) com o pygbag.

Uso:  uv run python scripts/montar_web.py           (monta)
      uv run python scripts/montar_web.py --servir  (monta e abre em http://localhost:8000)

Por que um script: o pygbag empacota a pasta inteira e, no Windows, o filtro dele
não reconhece as pastas a ignorar (ele espera caminhos com "/", e o Windows usa "\\").
Resultado: ele levava junto a .venv, os docs e os caches (19 MB).

Aqui é o contrário: uma LISTA DE PERMISSÃO. Só o que está em PARA_O_JOGO é copiado
para build/angel-and-dark/, e o pygbag roda lá. O que não está na lista nunca vaza.
"""

import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PACOTE = RAIZ / "build" / "angel-and-dark"  # a pasta que o pygbag vai empacotar
PARA_O_JOGO = ["main.py", "jogo", "assets", "config"]
IGNORAR = shutil.ignore_patterns("__pycache__", "*.pyc", ".gitkeep", "*.txt")


def copiar() -> None:
    if PACOTE.exists():
        shutil.rmtree(PACOTE)
    PACOTE.mkdir(parents=True)
    for nome in PARA_O_JOGO:
        origem = RAIZ / nome
        if origem.is_dir():
            shutil.copytree(origem, PACOTE / nome, ignore=IGNORAR)
        else:
            shutil.copy2(origem, PACOTE / nome)


def tamanho(pasta: Path) -> int:
    return sum(f.stat().st_size for f in pasta.rglob("*") if f.is_file())


def main() -> int:
    copiar()
    print(f"Copiado para {PACOTE} ({tamanho(PACOTE) // 1024} KB)")

    servir = "--servir" in sys.argv
    comando = [sys.executable, "-m", "pygbag", "--title", "Angel and Dark"]
    if not servir:
        comando += ["--build", "--archive"]  # --archive gera o web.zip para o itch.io
    comando.append(str(PACOTE))
    # Pelo "python -m": no Windows, o atalho pygbag.exe pode ser bloqueado pelo
    # controle de aplicativos (Smart App Control).
    return subprocess.call(comando)


if __name__ == "__main__":
    sys.exit(main())
