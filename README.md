# Angel and Dark

Jogo de plataforma 2D em Python (Pygame-CE), feito para rodar no navegador pelo itch.io.
Angel é a luz, Dark é a sombra. Dez fases até o chefe final, Kaothar.

> Em desenvolvimento. Versão atual: **v0.1, Parte 4**: o começo da Floresta, desenhado no Tiled, com arte da Kenney e fundo com profundidade.

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

## Estrutura
A organização das pastas e o motivo de cada uma estão em [docs/08_estrutura_final.md](docs/08_estrutura_final.md).
Os números do jogo (velocidade, pulo, gravidade) ficam em `config/` e podem ser ajustados sem mexer no código.

## Editar as fases
As fases são desenhadas no [Tiled](https://www.mapeditor.org/) (gratuito). Abra `assets/mapas/01_floresta.tmx`:
- camada **chao**: blocos em que o personagem pisa (tem a propriedade `solido`);
- camada **decoracao**: árvores, matinhos e bandeira, só enfeite;
- camada **objetos**: o ponto `inicio` e a área `chegada`.

Depois de salvar no Tiled, rode `uv run pytest`: o teste de alcance avisa se algum lugar ficou impossível de alcançar.

## Créditos
- Arte de cenário: [Pixel Platformer](https://kenney.nl/assets/pixel-platformer), da **Kenney** (licença CC0). Detalhes em `assets/cenarios/01_floresta/LICENCA_kenney.txt`.

## Autoria
Roteiro, design e direção: Leonardo Henrique Bueno.
Programação feita em par com o Claude (Anthropic).
