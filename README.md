# Angel and Dark

Jogo de plataforma 2D em Python (Pygame-CE), feito para rodar no navegador pelo itch.io.
Angel é a luz, Dark é a sombra. Dez fases até o chefe final, Kaothar.

> Em desenvolvimento. Versão atual: **v0.1, Parte 5**: Floresta 1 com corações, vidas, espinhos, água e checkpoints.

## Como jogar no PC
Precisa do [uv](https://docs.astral.sh/uv/) instalado.

```
uv sync
uv run python main.py
```

| Tecla | Ação |
|---|---|
| ← → ou A D | Andar |
| Espaço, ↑ ou W | Pular (segure para pular mais alto) |
| Enter ou Espaço | Confirmar a escolha de personagem |
| Esc | Na fase: voltar à escolha. Na escolha: sair |

## Para desenvolver
```
uv run ruff check .      # procura erros e problemas de estilo
uv run ruff format .     # arruma a formatação
uv run pytest            # roda os testes
```

## Versão para navegador (itch.io)
```
uv run python scripts/montar_web.py            # monta build/angel-and-dark/build/web.zip
uv run python scripts/montar_web.py --servir   # monta e abre em http://localhost:8000
```
- Na página, **clique uma vez** antes de jogar (o navegador só libera teclado e som depois de um clique).
- Para ver as mensagens do Python, abra `http://localhost:8000/#debug`.
- O `web.zip` é o arquivo que vai para o itch.io.
- Só `main.py`, `jogo/`, `assets/` e `config/` entram no pacote (lista em `scripts/montar_web.py`).

## Estrutura
A organização das pastas e o motivo de cada uma estão em [docs/08_estrutura_final.md](docs/08_estrutura_final.md).
Os números do jogo (velocidade, pulo, gravidade) ficam em `config/` e podem ser ajustados sem mexer no código.

## Editar as fases
As fases são desenhadas no [Tiled](https://www.mapeditor.org/) (gratuito). Abra `assets/mapas/01_floresta.tmx`:
- camada **chao**: blocos em que o personagem pisa (tem a propriedade `solido`);
- camada **decoracao**: árvores, matinhos e bandeira, só enfeite;
- camada **perigos**: espinhos (propriedade `perigo`; `altura_dano` diz quanto do bloco machuca);
- camada **agua**: desenhada na frente do personagem (propriedade `frente`);
- camada **objetos**: o ponto `inicio`, a área `chegada` e as bandeirinhas `checkpoint` (pode ter várias).

Depois de salvar no Tiled, rode `uv run pytest`: o teste de alcance avisa se algum lugar ficou impossível de alcançar.

## Créditos
- Arte de cenário: [Pixel Platformer](https://kenney.nl/assets/pixel-platformer), da **Kenney** (licença CC0). Detalhes em `assets/cenarios/01_floresta/LICENCA_kenney.txt`.

## Autoria
Roteiro, design e direção: Leonardo Henrique Bueno.
Programação feita em par com o Claude (Anthropic).
