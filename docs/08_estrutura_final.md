# Angel and Dark: estrutura de pastas final
Aprovada em 27/11/2026. Montada pelo Bueno a partir do `07_pastas.md`, revisada com o Claude.

## A estrutura
```
angel-and-dark/
  jogo/                  ← todo o código Python
    cenas/               ← menu, escolha de personagem, fase, pausa, game over
    personagens/         ← Angel, Dark e o que os dois têm em comum
      habilidades/       ← poderes dos personagens (mudam junto com eles)
    inimigos/            ← inimigos comuns
      chefes/            ← sub-chefes e Kaothar (Chefe herda de Inimigo)
    fases/               ← carregar mapa, colisão, câmera, checkpoints, plataformas
    interface/           ← corações, energia, orbes, diálogos, menus (uma pasta só)
    nucleo/              ← loop do jogo, controles, som, save (save.py)
  assets/                ← tudo que não é código
    imagens/             ← sprites de personagens, inimigos, itens
    sons/                ← efeitos sonoros
      personagens/       ← pulo, dano, poderes
      inimigos/          ← inimigos e chefes
      cenario/           ← orbes, portas, plataformas, água
      interface/         ← cliques do menu, pausa
    musicas/             ← trilhas (streaming), uma subpasta por fase
      01_floresta/ ... 10_guerra/
    cenarios/            ← tilesets e fundos, uma subpasta por fase
      01_floresta/ ... 10_guerra/
    mapas/               ← arquivos do Tiled, um por fase: 01_floresta.tmx ...
    fontes/
  config/                ← números do jogo em TOML (feito à mão)
  dialogos/              ← o roteiro, um arquivo por fase: 01_floresta.toml ...
  tests/                 ← testes do pytest
  scripts/               ← programinhas de apoio
  docs/                  ← documentos 01 a 08 e relatórios
    conceitos/           ← artes de IA de referência (não vão para o jogo)
  .github/               ← GitHub Actions
  saves/                 ← GERADO: fora do GitHub
  logs/                  ← GERADO: fora do GitHub
  build/                 ← GERADO: fora do GitHub
  main.py                ← inicia o jogo (o pygbag exige este nome)
  pyproject.toml
  README.md
  LICENSE
  .gitignore
```

## Regras combinadas
1. **Nomes de arquivos e pastas:** minúsculas, sem acento e sem espaço (`pulo_angel.ogg`). No navegador, maiúsculas fazem diferença.
2. **Fases numeradas e com o mesmo nome em todo lugar:** `03_vulcao` em `cenarios/`, em `musicas/`, em `mapas/03_vulcao.tmx` e em `dialogos/03_vulcao.toml`. O código acha tudo de uma fase pelo nome.
3. **Idioma:** o conteúdo do jogo fica em português; as pastas que as ferramentas conhecem ficam com o nome padrão em inglês (`tests/`, `scripts/`, `docs/`, `build/`, `.github/`).
4. **Gerado ≠ feito à mão:** `saves/`, `logs/` e `build/` ficam na raiz e entram no `.gitignore`.
5. **Save isolado em `nucleo/save.py`:** no PC grava em `saves/`; no navegador grava no armazenamento do navegador.
6. **O pygbag não deve empacotar** `docs/`, `tests/`, `scripts/` nem os conceitos. O Claude configura e confere isso na montagem.

## O que mudou da proposta original, e por quê
| Proposta | Ficou | Motivo |
|---|---|---|
| `interface/` também dentro de `personagens/` | Só `jogo/interface/` | A interface lê os dados do personagem, mas não mora nele. Duas pastas iguais geram dúvida. |
| `inimigos/` e `chefes/` dentro de `fases/` | `jogo/inimigos/chefes/` | `fases/` cuida de como a fase funciona; inimigos são quem vive nela. Kaothar e inimigos repetidos não pertencem a uma fase só. |
| Dois `sons/` em `assets/` | Um `sons/` com subpastas | Duas pastas com o mesmo nome não existem no mesmo lugar. A ideia de separar por origem virou subpastas. |
| `dialogos/`, `saves/` e `logs/` dentro de `config/` | `config/` e `dialogos/` lado a lado; `saves/` e `logs/` na raiz | Config são números, diálogos são o roteiro. Saves e logs são gerados e não podem ir para o GitHub. |
| `conceitos/` na raiz | `docs/conceitos/` | São referência, não fazem parte do jogo. |

## Próximo passo
O Bueno escreve o roteiro da **Parte 1**. Sugestão: a Angel andando e pulando numa tela de teste, para montar o esqueleto do projeto. Depois o Claude cria o repositório e a estrutura, constrói a Parte 1 e entrega o relatório.
