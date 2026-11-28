# Relatório: Parte 1, a Angel se mexendo
Data: 27/11/2026 | Branch: `parte-01-movimento` | Commits: `cb41e44` (estrutura) e `dca8096` (Parte 1)

## O que foi pedido
Janela com chão e plataformas; Angel como quadrado branco; setas/A D andam, espaço pula; não atravessa chão nem plataformas; ao cair da tela volta ao início; pulo gostoso de controlar.

## O que foi feito
Todos os itens do pedido. Além disso:
- **Pulo variável:** segurar o botão pula mais alto; tocar rápido dá um pulinho.
- **Tempo de coiote (0,10 s):** ainda dá para pular logo depois de sair da borda. Sem isso, o jogador sente que "apertou e não pulou".
- **Buffer de pulo (0,12 s):** apertar um pouco antes de tocar o chão ainda vale.
- **Aceleração e freio:** a Angel não sai na velocidade máxima nem para seco.
- **Contador de quedas e estado na tela,** para ajudar nos testes.

Esses quatro truques são usados em quase todo jogo de plataforma bom. É isso que faz o pulo ficar "gostoso".

## Como a arquitetura escolhida apareceu
| Escolha | Onde está |
|---|---|
| Herança | `Angel` herda de `Personagem` (`jogo/personagens/`). A Dark vai herdar o mesmo movimento. |
| Cenas | `Cena` é o modelo; `CenaTeste` é a primeira. O menu vai ser outra cena. |
| Máquina de estados | `Estado`: parado, andando, pulando, caindo. Vai decidir qual animação toca. |
| Config fora do código | `config/personagens.toml` (controle), `config/jogo.toml` (janela e cores), `config/fase_teste.toml` (plataformas). |
| Um módulo por tecnologia | Só `jogo/nucleo/config.py` sabe que existe TOML; só `jogo/nucleo/controles.py` sabe quais teclas existem. |
| pygbag | `main.py` com loop `async` e `await asyncio.sleep(0)` a cada quadro. |

## Arquivos
- **Raiz:** `main.py`, `pyproject.toml`, `uv.lock`, `.python-version` (3.12), `.gitignore`, `.gitattributes`, `README.md`, `LICENSE`
- **Código:** `jogo/nucleo/` (jogo, config, controles), `jogo/personagens/` (personagem, angel), `jogo/fases/fase.py`, `jogo/cenas/` (cena, cena_teste)
- **Testes:** `tests/test_angel.py` (10 testes), `tests/test_fase.py` (3 testes)
- **Automação:** `.github/workflows/ci.yml` roda Ruff e pytest a cada push e PR
- **Docs:** documentos 01 a 08 e as artes de conceito copiados para `docs/`

## Testes
- `ruff check` e `ruff format`: sem problemas.
- `pytest`: **13 de 13 passando.** Cobrem cair e parar no chão, andar, velocidade máxima, pular e voltar, pulo variável, não pular no ar, tempo de coiote, parede, teto e reinício.
- O jogo rodou de verdade, sem janela, com comandos simulados: a Angel pulou, caiu no buraco e voltou ao início.

## Problemas encontrados e corrigidos
1. **Bug achado pelos testes:** parada no chão, a Angel "piscava" entre parada e caindo. A gravidade a empurrava meio pixel, o arredondamento a deixava só encostada, e encostar não contava como colisão. **Correção:** um sensor que olha 1 pixel abaixo dos pés. Sem os testes, esse bug só apareceria depois, nas animações.
2. **Corte do pulo dependia do FPS:** a primeira versão multiplicava a velocidade a cada quadro, então o pulo seria diferente a 30 e a 60 FPS. Troquei por um limite fixo.
3. **Plataforma impossível:** a da esquerda, no alto, ficava 170 px acima da mais próxima, e o pulo alcança uns 107 px. Baixei para 90 px. Conta usada: altura do pulo = força² ÷ (2 × gravidade) = 620² ÷ 3600 ≈ 107 px.

## Decisões que tomei sozinho (para você revisar)
- **Python 3.12** no projeto (o PC tem 3.14), por compatibilidade com o pygbag. O uv baixou o 3.12 só para este projeto.
- **Licença MIT** no código. É a mais comum em portfólio e deixa qualquer um usar com crédito. **Você pode trocar.** Artes e músicas de terceiros terão as licenças próprias delas.
- **Janela 960×540:** metade do Full HD, cresce sem distorcer.
- **`.gitkeep`:** o Git não guarda pastas vazias, então coloquei um arquivo vazio nas pastas que ainda não têm nada.

## Pendências
- **Repositório no GitHub ainda não criado.** Está tudo só no seu PC. Para abrir o Pull Request, precisa criar o repositório e enviar. O CI só roda depois disso.
- **pygbag (versão web) ainda não testado.** O código já está preparado para ele (loop async), mas o primeiro teste no navegador fica para uma próxima parte, junto da configuração para não empacotar docs, testes e conceitos.
- Números do pulo ainda estão no "chute inicial". **Você precisa jogar e dizer o que sentiu.**

## Para debater
1. O pulo está alto, baixo, "flutuante" ou "pesado"? Dá para ajustar em `config/personagens.toml`: `forca_pulo` muda a altura e `gravidade` muda o peso.
2. A velocidade de andar está boa?
3. Mantém MIT ou prefere outra licença?
4. O que entra na Parte 2? Sugestões: a Dark e a troca entre as duas; a câmera seguindo numa fase maior que a tela; ou a primeira fase vinda do Tiled.

---

## Revisão 1 (28/11/2026): depois do primeiro teste de jogo
**O que o Leonardo achou:** a altura do pulo está boa; o peso (cai rápido e sobe devagar segurando) ficou bom; o controle responde na hora. Ele teve dificuldade para alcançar uma plataforma e se preocupou com o jogador não conseguir voltar.

**Diagnóstico:** o problema não era o pulo, era o desenho da fase. A plataforma da direita ficava 120 px acima do chão, e o pulo alcança cerca de 107 px, ou seja, era impossível. Outras duas estavam no limite.

**O que mudou:**
- `config/fase_teste.toml`: todas as subidas agora ficam entre 80 e 90 px.
- `tests/test_fase.py`: novo teste `test_toda_plataforma_e_alcancavel`. Ele calcula o alcance do pulo a partir da config e reprova plataformas impossíveis. Com a fase antiga, o teste **reprovou** (como devia); com a nova, passa. Agora são **14 testes**.
- `docs/04_fases_angel_and_dark.md`: novas seções "Regras de design das fases" e "Ideias em aberto" (pulo duplo).
- `docs/03` e `docs/05`: o ataque 2 da Dark passou a ser "poderes da escuridão" (esferas negras e buracos negros que sugam inimigos), no lugar de "ataque de sombras".

**O que não mudou, de propósito:** os números do pulo e do controle, porque o teste de jogo aprovou.
