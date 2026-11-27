


# Angel and Dark: pastas do projeto
Criado em 27/11/2026. **Você monta a estrutura, eu digo se funciona.**

## A lógica por trás das pastas
Projeto real separa as coisas por **tipo** e por **quem mexe nelas**. Quatro motivos:
1. **Achar rápido:** daqui a 6 meses, com 10 fases, você precisa saber onde está a sprite do javali sem procurar.
2. **Separar o que muda junto:** o código muda com frequência; a arte muda com outro ritmo; os documentos quase não mudam. Misturar tudo deixa cada mudança mais confusa.
3. **Ferramentas esperam um padrão:** o pytest procura testes numa pasta, o pygbag empacota uma pasta para a web, o Git ignora pastas que você listar.
4. **O que é gerado não se mistura com o que é feito à mão:** arquivos que o computador cria (o jogo empacotado, saves, registros) ficam separados e **não vão para o GitHub**.

## Pastas que você provavelmente vai precisar
Escolha quais usar, que nome dar e onde cada uma fica (dentro de qual). Pode juntar, separar ou inventar outras. Escreva o motivo das suas escolhas.

### Código
| Pasta (sugestão de nome) | O que guarda | Pergunta para você pensar |
|---|---|---|
| `src/` ou `jogo/` | Todo o código Python do jogo | Código fica direto na raiz do projeto ou dentro de uma pasta? |
| `cenas/` | Telas: menu, escolha de personagem, fase, pausa, game over | — |
| `personagens/` ou `jogadores/` | Angel, Dark e o que os dois têm em comum | Angel e Dark juntos numa pasta ou um arquivo para cada? |
| `inimigos/` | Inimigos comuns | Organizar por tipo ou por fase (floresta, vulcão...)? |
| `chefes/` | Sub-chefes e o Kaothar | Chefe é um tipo de inimigo (dentro de `inimigos/`) ou merece pasta própria? |
| `mundo/` ou `fases/` | Carregar mapa, colisão, câmera, checkpoints, plataformas móveis | — |
| `poderes/` ou `habilidades/` | Teletransporte, sombras, raios, luz... | Poder fica junto do personagem ou separado? |
| `interface/` ou `ui/` | Corações, vidas, barra de energia, contador de orbes, diálogos | — |
| `nucleo/` ou `core/` | Peças usadas por tudo: loop do jogo, controles, som, save | — |

### Conteúdo do jogo (assets)
| Pasta | O que guarda | Pergunta para você pensar |
|---|---|---|
| `assets/` | Tudo que não é código | — |
| `sprites/` ou `imagens/` | Personagens, inimigos, itens | Organizar por personagem ou por tipo? |
| `cenarios/` ou `tilesets/` | Blocos e fundos de cada tema | Uma pasta por fase? |
| `sons/` | Efeitos (pulo, dano, orbe) | Separar efeitos de música? |
| `musicas/` | Trilhas de cada fase | — |
| `fontes/` | Fonte das letras do menu e dos diálogos | — |
| `mapas/` ou `niveis/` | Arquivos das fases feitos no Tiled | Fica junto dos assets ou separado? |

### Dados e configuração
| Pasta | O que guarda | Pergunta para você pensar |
|---|---|---|
| `config/` ou `dados/` | Números do jogo: velocidade, altura do pulo, vida dos inimigos | — |
| `dialogos/` ou `roteiro/` | Falas das cenas entre as fases (o seu roteiro vira arquivo aqui) | — |
| `saves/` | Progresso do jogador | **Vai para o GitHub ou não?** |
| `telemetria/` ou `logs/` | Registro de mortes e tempo, para o Power BI | Vai para o GitHub ou não? |

### Projeto e ferramentas
| Pasta / arquivo | O que guarda | Pergunta para você pensar |
|---|---|---|
| `tests/` ou `testes/` | Testes automáticos (pytest) | Nome em inglês ou português? |
| `docs/` | GDD, estes documentos, relatórios das partes | Os relatórios ficam aqui ou só no GitHub? |
| `conceitos/` | Artes de IA de referência (Angel, Dark, Kaothar) | Vai para o jogo final ou só para o repositório? |
| `ferramentas/` ou `scripts/` | Programinhas de apoio (converter áudio, exportar telemetria) | — |
| `build/` ou `dist/` | Jogo empacotado para web ou .exe (gerado pelo computador) | Vai para o GitHub ou não? |
| `.github/` | Automação do GitHub Actions e modelos de Issue | — |
| Arquivos da raiz | `README.md`, `CHANGELOG.md`, `LICENSE`, `.gitignore`, `pyproject.toml` ou `requirements.txt`, `main.py` | Qual é o arquivo que inicia o jogo? |

## Decisões que valem mais pensar
1. **Português ou inglês nos nomes?** Pastas, arquivos e código (`personagem.py` ou `player.py`). Isso tem impacto em portfólio e em quem vai ler o código.
2. **Organizar por tipo ou por fase?** Por exemplo, `sprites/javali.png` ou `fases/floresta/javali.png`. Cada jeito facilita uma coisa e complica outra.
3. **Quantos níveis de pasta?** Muitas pastas dentro de pastas fica organizado, mas cansa para navegar. Poucas fica simples, mas lota.
4. **O que fica de fora do GitHub?**

## Como entregar a sua estrutura
Do jeito que for mais fácil para você. Pode ser assim, com o motivo ao lado:
```
angel-and-dark/
  jogo/            ← porque...
    personagens/   ← porque...
  assets/
  ...
```
Ou em tópicos, ou desenhada no papel (manda foto). Eu respondo com: o que funciona, o que pode dar problema mais para frente, o que eu mudaria e por quê.

## Estrutura aprovada (27/11/2026)
A estrutura final, com as regras e o que mudou, está em `08_estrutura_final.md`.
