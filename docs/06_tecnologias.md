# Angel and Dark: todas as tecnologias possíveis
Criado em 27/11/2026. **Você escolhe, eu construo.** Marque com [x] o que escolher e, se quiser, escreva o motivo ao lado. Depois eu comento cada escolha com pontos positivos e negativos.

Legenda: ⭐ = minha sugestão para este projeto · 🔁 = já escolhido antes (pode mudar) · 💲 = pago

---

## 1. Linguagem e motor do jogo (escolher 1)
O motor é a base: desenha na tela, lê o teclado, toca som e roda o "loop" do jogo (60 vezes por segundo: ler controles → mover tudo → desenhar).

| | Opção | Linguagem | Positivo | Negativo |
|---|---|---|---|---|
| [x] 🔁 | **Pygame-CE** | Python | Você já conhece Python; mostra lógica feita "na mão"; muito material de estudo; roda no navegador com pygbag | Tudo do zero: física, câmera, colisão, animação, menus. Mais código para manter **Escolha (27/11): aprendizado.** |
| [ ] | **Arcade** | Python | Python moderno; física de plataforma pronta; lê mapas do Tiled direto | Comunidade menor; versão web limitada |
| [ ] | **Pyxel** | Python | Muito simples; editor de sprite e música embutido; publica na web fácil | Limite de 16 cores e tela pequena: **não combina com 16-bit detalhado** |
| [ ] | **Godot 4** | GDScript (parecida com Python) | Editor visual de fases e animação; física e partículas prontas; o mais fácil de ficar bonito | Não é Python; parte do trabalho é clicando no editor (menos código para você ler nos relatórios) |
| [ ] | Phaser | JavaScript | Feito para navegador; leve | Foge do seu foco (Python e dados) |
| [ ] | Unity / GameMaker | C# / GML | Fortes no mercado de jogos | Pesados para web; fogem do seu foco |

**Versão do Python** (se escolher Pygame ou Arcade): [ ] ⭐ a versão que o pygbag suportar na hora de começar (eu confiro antes) · [ ] a mais nova do Python

## 2. Rodar no navegador (itch.io)
| | Opção | Para que serve | Positivo | Negativo |
|---|---|---|---|---|
| [x] ⭐ | **pygbag** | Transforma o jogo Pygame em página web | Oficial da comunidade Pygame; funciona no itch.io | Impõe regras no código: o loop precisa ser `async`; áudio em **OGG**; sem *threads*; nomes de arquivo sensíveis a maiúsculas **Escolha (27/11): já é o padrão para publicar Pygame no itch.io.** |
| [ ] | Só PC primeiro (sem web) | — | Menos regras no começo | Recrutador ou cliente precisa baixar para jogar |

## 3. Ambiente e dependências (como o projeto instala as bibliotecas)
| | Opção | Positivo | Negativo |
|---|---|---|---|
| [ ] | **venv + pip + requirements.txt** | O jeito clássico; você já viu nos outros projetos | Mais manual; não trava as versões tão bem |
| [x] ⭐ | **uv + pyproject.toml** | Ferramenta nova e muito rápida; cria o ambiente e trava as versões num comando; padrão moderno | Mais uma ferramenta para aprender **Escolha (27/11): mais rápida, mais nova e mais um aprendizado.** |
| [ ] | Poetry | Popular em empresas | Mais lento e complexo que o uv |

## 4. Editor de fases (level design)
| | Opção | Positivo | Negativo |
|---|---|---|---|
| [x] ⭐ | **Tiled** + biblioteca **pytmx** | Você desenha a fase com blocos, como num Paint; marca onde ficam inimigos, checkpoints e segredos; padrão da indústria indie | Mais um programa; o arquivo da fase precisa seguir regras que vamos combinar **Escolha (27/11): melhor para trabalhar as fases.** |
| [ ] | **LDtk** | Moderno, feito para plataforma; ótimo para fases ligadas | Biblioteca para Python menos madura |
| [ ] | Fases em texto/CSV (cada letra = um bloco) | Simples; dá para escrever a fase no bloco de notas | Fica difícil com 10 fases grandes, dois caminhos e segredos |

## 5. Arte (16-bit)
**Importante:** eu consigo criar **arte provisória** (bonecos e blocos simples) para o jogo funcionar e ser testado. A **arte final 16-bit** precisa vir de você desenhando, de pacotes prontos ou de um artista. Conceitos de IA ajudam como referência, mas não servem direto como sprite (mudam entre um quadro e outro da animação).

| | Opção | Para que serve | Positivo | Negativo |
|---|---|---|---|---|
| [ ] ⭐ | **Aseprite** 💲 (~US$ 20) | Desenhar e animar pixel art | Padrão indie; exporta *spritesheet* + JSON que o código lê | Pago |
| [x] | **LibreSprite** | Mesmo, grátis | Parecido com o Aseprite | Menos recursos **Escolha (27/11): para adaptar os pacotes e fazer os sprites.** |
| [ ] | **Piskel** | Mesmo, no navegador | Muito fácil | Simples demais para 16-bit detalhado |
| [ ] | **Krita** | Capa, menu, arte de divulgação | Grátis e profissional | Não é para sprite animado |
| [x] ⭐ | **Pacotes prontos** (itch.io, Kenney, OpenGameArt) | Cenários, blocos, efeitos | Rápido; deixa você focar nos personagens | Conferir a licença de cada um; o estilo precisa combinar **Escolha (27/11), com dúvida entre pacotes e IA: pediu análise detalhada.** |
| [ ] | **Contratar artista** 💲 | Personagens e chefes | Resultado profissional | Custo |
| [x] 🔁 | **IA de imagem (ChatGPT)** | Conceitos e referência | Já usamos para Angel, Dark e Kaothar | Não vira sprite direto |

**Modelo de arte escolhido (27/11): híbrido.** Cenários, blocos, itens e efeitos vêm de pacotes prontos. Angel, Dark e chefes usam arte provisória feita pelo Claude na versão 0.1 e, na versão final, pixel art feita a partir dos conceitos da IA. Capa, menu e retratos dos diálogos ficam com a IA.

## 6. Som e música
| | Opção | Para que serve | Positivo | Negativo |
|---|---|---|---|---|
| [x] ⭐ | **jsfxr / sfxr** | Efeitos (pulo, dano, orbe) | Um clique, no navegador | Som bem retrô **Escolha (27/11): mais prática e rápida.** |
| [ ] | **ChipTone** | Efeitos | Mais controle | Um pouco mais difícil |
| [ ] | **BeepBox** | Música chiptune | No navegador, fácil | Som 8-bit; 16-bit pede algo mais rico |
| [ ] ⭐ | **LMMS** ou **Furnace Tracker** | Música estilo Super Nintendo / Mega Drive | Grátis; o Furnace imita os chips de som da época | Curva de aprendizado |
| [x] | **Músicas prontas** (itch.io, OpenGameArt, Pixabay) | Trilha | Rápido | Conferir licença; menos identidade **Escolha (27/11): não sabe compor; conferir a licença de cada música.** |
| [x] | **Audacity** | Cortar, ajustar volume, converter para OGG | Grátis | — **Escolha (27/11): converter as músicas prontas para OGG.** |

## 7. Arquitetura do código (como o código é organizado por dentro)
Isso é o que mais vai aparecer nos meus relatórios. Vale escolher com calma.

| | Opção | Explicação | Positivo | Negativo |
|---|---|---|---|---|
| [x] ⭐ | **Cenas (estados)** | O jogo é uma pilha de telas: Menu → Escolha de personagem → Fase → Pausa → Game over. Cada uma é uma classe | Simples de entender e de crescer | — (quase todo jogo usa) **Escolha (27/11).** |
| [x] ⭐ | **Orientação a objetos** com herança | `Personagem` → `Angel` e `Dark`; `Inimigo` → `Javali`, `Vespa`... | Fácil de ler; combina com o que você estudou | Herança demais vira bagunça; usar com moderação **Escolha (27/11): fácil de ler, facilita edições futuras e combina com o que já fez.** |
| [ ] | **ECS** (Entidade-Componente-Sistema) | Cada coisa é um "saco de componentes" (posição, vida, sprite) e sistemas processam tudo | Muito usado em motores profissionais; escala bem | Complexo para começar; exagero para este tamanho |
| [x] ⭐ | **Máquina de estados** nos personagens e chefes | Parado → Correndo → Pulando → Atacando → Dano. Chefe: Fase 1 → Transformação → Fúria | Deixa os padrões dos chefes claros e "legíveis" | — **Escolha (27/11).** |
| [x] ⭐ | **Configurações fora do código** (arquivos JSON/TOML) | Velocidade, pulo, vida dos inimigos ficam num arquivo, não no código | Você ajusta a dificuldade sem mexer em Python | Mais arquivos **Escolha (27/11).** |

## 8. Save e dados
| | Opção | Positivo | Negativo |
|---|---|---|---|
| [x] ⭐ | **JSON** para o save (fases liberadas, itens secretos, recordes) | Simples; dá para abrir e ler; no navegador o pygbag guarda no armazenamento do browser | — **Escolha (27/11): mais simples.** |
| [ ] | **SQLite** | Você já usa nos outros projetos; bom para muitos registros | Exagero para um save; no navegador é mais chato |
| [ ] ⭐ | **Telemetria** (registro de mortes, tempo e posição de cada morte) → **CSV** → **Power BI** | Junta jogo e análise de dados: "mapa de dificuldade" das fases. Diferencial forte no portfólio | Na versão web, os dados precisam ser exportados ou enviados para algum lugar |

## 9. Qualidade do código
| | Opção | Para que serve | Positivo | Negativo |
|---|---|---|---|---|
| [x] ⭐ | **pytest** | Testes automáticos da lógica (colisão, dano, save) | Raro em jogo de portfólio, chama atenção; pega erro antes de você jogar | Mais código **Escolha (27/11): junto com o Ruff (não competem: Ruff confere a escrita, pytest confere o comportamento).** |
| [x] ⭐ | **Ruff** | Verifica estilo e erros comuns, e formata o código | Muito rápido; um só programa | — **Escolha (27/11): velocidade e menos espaço; quase escolheu o pytest.** |
| [ ] | **mypy** (tipagem) | Confere os tipos das variáveis | Pega erros sutis; código mais profissional | Mais rigor, às vezes chato no começo |
| [ ] | **pre-commit** | Roda Ruff e testes antes de cada commit | Nunca sobe código quebrado | Mais configuração |

## 10. Versionamento e organização
| | Opção | Positivo | Negativo |
|---|---|---|---|
| [ ] ⭐ | **Git + GitHub** (repositório público em `buenor877-ux`) | Histórico mostra a evolução; portfólio | — |
| [ ] | **Git LFS** | Para arquivos grandes (arte, música) | Limite de espaço grátis no GitHub |
| [x] ⭐ | **Branches por parte** (`fase-1`, `chefe-arvore`...) + Pull Request | Cada parte que eu fizer vira um PR que você revisa e aprova: **é exatamente o seu modelo de relatório** | Um passo a mais antes de juntar **Escolha (27/11): quer saber de tudo o que aconteceu em cada parte.** |
| [ ] ⭐ | **GitHub Issues + Projects** (quadro a fazer / fazendo / feito) | Organiza o roteiro em tarefas; é como empresas trabalham | Precisa manter atualizado |
| [ ] | Trello / Notion | Visual | Fora do GitHub (não aparece no portfólio) |

## 11. Automação (CI/CD)
| | Opção | Para que serve | Positivo | Negativo |
|---|---|---|---|---|
| [x] ⭐ | **GitHub Actions** | Roda os testes sozinho a cada envio | Mostra prática de empresa; combina com seu foco em automação | Configuração inicial **Escolha (27/11): muito usado em empresas e combina com o foco em automação.** |
| [ ] | **butler** (ferramenta do itch.io) + Actions | Publica a nova versão no itch.io automaticamente | Lançar versão vira um comando | Mais uma configuração |
| [ ] | **GitHub Pages** | Versão web alternativa ao itch.io | Grátis, no mesmo lugar do código | Menos visibilidade para jogadores |

## 12. Publicação e documentação
| | Opção | Positivo | Negativo |
|---|---|---|---|
| [x] ⭐ | **itch.io** (jogável no navegador) | Clica e joga | — **Escolha (27/11): fácil de usar.** |
| [ ] | **PyInstaller** (.exe para Windows) | Versão offline | Antivírus às vezes reclama de .exe novo |
| [x] ⭐ | **README** com GIF do jogo (ScreenToGif ou OBS) | Primeira coisa que alguém vê | — **Escolha (27/11).** |
| [x] ⭐ | **CHANGELOG** (o que mudou em cada versão 0.1, 0.3...) | Mostra organização | — **Escolha (27/11): a partir da versão 0.3.** |
| [x] ⭐ | **LICENSE** (licença do código) | Deixa claro o que outros podem fazer com ele | Escolher qual (MIT é a mais comum) **Escolha (27/11).** |
| [ ] | **Devlog** no YouTube / LinkedIn | Divulga e mostra o processo | Tempo extra |

---

## Como vamos trabalhar (modelo combinado em 27/11)
1. **Você** escreve o roteiro de cada parte (o que deve acontecer, como deve ser).
2. **Você** escolhe as tecnologias e a estrutura de pastas, com os seus motivos.
3. **Eu** comento cada escolha: se funciona, pontos positivos e negativos, e minha sugestão.
4. **Eu** construo a parte.
5. **Eu** entrego um **relatório**: o que fiz, por quê, quais arquivos mudaram, o que testei e o que ficou pendente.
6. **A gente debate** e você aprova ou pede mudanças antes da próxima parte.
