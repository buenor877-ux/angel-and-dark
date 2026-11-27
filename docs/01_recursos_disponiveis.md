# Jogo de plataforma (projeto de portfólio): recursos disponíveis
Criado em 25/11/2026. Marque com [x] o que quiser usar. Na reunião fechamos as escolhas.
Tudo gratuito, a menos que esteja indicado. Regra de ouro: **personagens, nomes, músicas e cenários próprios**. O estilo (plataforma 2D) pode ser parecido com o Mario, mas nada da Nintendo (nome, personagem, som, fase copiada).

---

## 1. Motor / linguagem (escolher 1)
| | Opção | Linguagem | Pontos fortes | Pontos fracos | Roda no navegador? |
|---|---|---|---|---|---|
| [ ] | **Pygame-CE** | Python | Você já sabe Python; mostra lógica "na mão" (física, colisão, câmera), que é ótimo para entrevista de dev | Tudo feito do zero, mais trabalhoso; visual depende de você | Sim, com **pygbag** |
| [ ] | **Arcade** | Python | Python mais moderno, com física de plataforma pronta e leitura de mapas do Tiled | Comunidade menor que a do Pygame | Limitado |
| [ ] | **Pyxel** | Python | Jogo retrô 8-bit; já vem com editor de sprites, mapas e música embutido; publica na web fácil | Visual limitado de propósito (16 cores, tela pequena) | Sim |
| [ ] | **Godot 4** | GDScript (parecida com Python) | Motor completo: editor de fases, animação, física, partículas; visual mais profissional; exporta para web, PC e Android | Linguagem nova (mas parecida); menos "Python" no currículo | Sim |
| — | Unity (C#), GameMaker, Phaser (JavaScript) | — | Fortes no mercado de jogos | Fogem do seu foco (Python/dados) | — |

**Resumo:** para o currículo de dev Python → **Pygame-CE**. Para o jogo mais bonito e mais rápido de ficar "jogável" → **Godot**. Para algo retrô simples e charmoso → **Pyxel**.

## 2. Fases (level design)
- [ ] **Tiled**: editor de mapas por blocos (tiles), salva em arquivo que Pygame/Arcade leem (biblioteca `pytmx`)
- [ ] **LDtk**: editor de fases moderno, feito para jogos de plataforma
- [ ] **TileMap do Godot**: já vem dentro do Godot
- [ ] Fases em texto/CSV (cada letra = um bloco): o mais simples, bom para começar

## 3. Arte (personagens, vilões, cenários)
**Ferramentas para desenhar pixel art**
- [ ] **Piskel**: no navegador, grátis, muito fácil
- [ ] **LibreSprite**: grátis, parecido com o Aseprite
- [ ] **Aseprite**: o padrão da indústria indie (pago, cerca de US$ 20 na Steam)
- [ ] **Krita**: desenho livre/pintura (para capa, menu e arte de divulgação)

**Pacotes prontos para cenário e itens** (para focar a sua arte nos personagens)
- [ ] **Kenney.nl**: milhares de assets de plataforma, licença CC0 (pode usar sem dar crédito)
- [ ] **itch.io > Assets > Free**: pacotes de tiles, inimigos, efeitos
- [ ] **OpenGameArt.org**: conferir a licença de cada um

**IA para ideias e conceito**
- [ ] **ChatGPT (imagem)**: você já usa nas capas; bom para *concept art* (como o herói e os vilões são), depois redesenhado em pixel art. Imagem de IA direto no jogo costuma ficar inconsistente entre os quadros de animação.
- [ ] Eu escrevo os prompts e a ficha de cada personagem (como faço com as capas do YouTube)

## 4. Som e música
- [ ] **jsfxr / sfxr**: gera efeitos retrô (pulo, moeda, dano) com um clique, no navegador
- [ ] **ChipTone**: efeitos 8-bit com mais controle
- [ ] **BeepBox**: compõe música chiptune no navegador
- [ ] **LMMS** ou **Bosca Ceoil**: compor músicas completas
- [ ] **Freesound.org** e **Pixabay Sound**: efeitos gravados (ver a licença)
- [ ] **Audacity**: cortar e ajustar áudio; gravar sua voz para personagens

## 5. Mecânicas que dá para ter (escolher no escopo)
**Básico (o "coração" do jogo)**
- [ ] Andar, pular (pulo variável: segurar = mais alto), gravidade
- [ ] Colisão com chão/paredes/plataformas
- [ ] Câmera que segue o herói
- [ ] Inimigos que andam e morrem ao levar pisão
- [ ] Moedas/itens colecionáveis e placar
- [ ] Vidas, morte, reinício da fase, tela de game over

**Intermediário**
- [ ] Power-ups próprios (você inventa: ex. um poder ligado à história)
- [ ] Plataformas móveis, que caem, molas
- [ ] Blocos quebráveis / blocos com item
- [ ] Checkpoint no meio da fase
- [ ] Menu inicial, pausa, opções de volume
- [ ] Mapa de seleção de fases e save do progresso (arquivo JSON)

**Avançado (o que impressiona)**
- [ ] **Chefão** com padrões de ataque e fases de vida
- [ ] Pulo duplo, dash, deslizar na parede
- [ ] Diálogos/história entre fases (cutscenes simples)
- [ ] Partículas (poeira no pulo, explosão), *screen shake*
- [ ] Ranking de pontuação (local ou online)
- [ ] Suporte a controle (gamepad)
- [ ] **Dados no jogo**: registrar mortes, tempo e onde o jogador morre → painel de **Power BI** com "mapa de dificuldade" das fases (une o jogo ao seu foco em dados — diferencial forte no portfólio)

## 6. Ferramentas de programação e organização
- [ ] **VS Code** + extensão Python (ou o editor do Godot)
- [ ] **Git + GitHub** (`buenor877-ux`): um repositório público com histórico de commits mostra evolução
- [ ] **GitHub Projects** (quadro kanban: a fazer / fazendo / feito)
- [ ] **pytest**: testes da lógica (colisão, pontuação, save) — raro em jogo de portfólio, chama atenção
- [ ] **GDD (Documento de Design do Jogo)**: 2–4 páginas com história, personagens, mecânicas, fases. Eu monto com você.

## 7. Publicação e divulgação
- [ ] **itch.io**: página do jogo, jogável no navegador (o recrutador clica e joga)
- [ ] **GitHub Pages**: alternativa para versão web
- [ ] **PyInstaller** (Python) ou exportação do Godot: versão `.exe` para Windows
- [ ] **README** com GIF do jogo (gravar com **ScreenToGif** ou **OBS**, que você já usa)
- [ ] **Devlog no YouTube / Twitch**: gravar o desenvolvimento ao vivo e postar episódios no seu canal (conteúdo novo + mostra o projeto). Eu corto e preparo como os outros vídeos.
- [ ] **Post no LinkedIn** no lançamento (eu escrevo o rascunho)
- [ ] Entrar numa **game jam** do itch.io (prazo curto, comunidade, linha a mais no currículo)

## 8. Como eu posso ajudar (você escolhe o nível)
- [ ] **Mentor (como no leitor de NF-e):** explico o conceito, você escreve o código, eu reviso e aponto erros. Aprende mais, conta mais em entrevista.
- [ ] **Par de programação:** eu escrevo partes difíceis (ex. câmera, chefão) explicando linha a linha; você faz o resto.
- [ ] Montar o GDD, a ficha dos personagens e os prompts de concept art
- [ ] Gerar sprites provisórios (blocos coloridos) para testar antes da arte final
- [ ] Pesquisar referências e tutoriais
- [ ] Testar o jogo, achar bugs, medir desempenho
- [ ] Preparar a página do itch.io, README, devlogs e post

## 9. Tamanhos de projeto (escopo)
| Tamanho | Conteúdo | Tempo estimado (1h30/dia) |
|---|---|---|
| **Mini** | 1 herói, 2 inimigos, 3 fases curtas, moedas, game over | 3 a 4 semanas |
| **Médio** | + 1 chefão, 2 power-ups, menu, checkpoints, 5–6 fases, música própria | 2 a 3 meses |
| **Grande** | + mundo com mapa, história com diálogos, save, 10+ fases, vários chefes | 6 meses ou mais |

Recomendação para portfólio: começar no **Mini**, publicar, e evoluir para o Médio em atualizações (versão 1.0 → 1.1 → 2.0). Projeto pequeno terminado vale mais que projeto grande pela metade.
