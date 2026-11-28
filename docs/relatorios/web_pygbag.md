# Relatório: a versão para navegador (pygbag)
Data: 28/11/2026 | Branch: `teste-web-pygbag`

## O que foi pedido
Testar a versão do jogo para navegador. Ela estava pendente desde a Parte 1, e o objetivo do itch.io depende dela. É um trabalho técnico, sem decisão de design: conferir se o jogo roda no navegador, se o `pytmx` funciona lá e se o cenário de 6 telas não pesa demais.

## Resultado em uma frase
**O jogo roda no navegador**: tela de escolha, Angel e Dark, a Floresta inteira com arte, vidas e câmera. Ele também ficou **12 vezes mais rápido** de desenhar.

## O que foi feito
- **pygbag instalado** como ferramenta de desenvolvimento (só para quem monta o jogo, não vai para o jogador).
- **`scripts/montar_web.py`**: monta a versão web com um comando só (veja o README).
- **`main.py`** agora declara as dependências do jogo (`pygame-ce` e `pytmx`).
- **Desenho do cenário mais leve** (`carregador_fases.py` e `fundo.py`).
- **Tela de escolha:** no navegador, a dica "Esc: sair" some, porque lá não existe fechar o programa.

## Problemas encontrados e corrigidos
Foram 5, e cada um ensina alguma coisa sobre projeto real.

1. **O Windows bloqueou o `pygbag.exe`.** O Smart App Control (proteção do Windows 11) barra executáveis novos sem assinatura digital.
   **Correção:** rodar pelo próprio Python (`python -m pygbag`), que já é confiável para o Windows.

2. **O pacote saía com 19 MB, quando o jogo tem 30 KB.** O pygbag empacota a pasta do projeto e tem uma lista do que ignorar, mas essa lista **não funciona no Windows**: ela espera caminhos com `/` (como no Linux), e o Windows usa `\`. Resultado: ele levava a `.venv` inteira (1.954 arquivos), os documentos, as artes de conceito e os caches. O build ainda quebrava, porque achou um som `.wav` de exemplo dentro da `.venv` (no navegador, só OGG).
   **Correção:** em vez de dizer "empacote tudo, menos isto" (**lista de bloqueio**), o script copia **só** o que o jogo precisa (`main.py`, `jogo/`, `assets/` e `config/`) para uma pasta separada e empacota essa pasta (**lista de permissão**). O que não está na lista nunca vaza, em nenhum sistema. O pacote caiu de 19 MB para **30 KB**.

3. **No navegador, o jogo quebrava logo no início** com `module 'pygame' has no attribute 'event'`. O pygbag descobre quais bibliotecas baixar **lendo só o `main.py`**, e o nosso `main.py` não importava nem o pygame nem o pytmx (eles aparecem nos outros arquivos).
   **Correção:** um bloco padrão no topo do `main.py` (o PEP 723, que lista as dependências) e os dois imports ali. Agora o log do navegador mostra o pygame-ce e o **PyTMX baixados e instalados**.

4. **O jogo rodaria a uns 28 FPS no navegador.** Medi cada parte do desenho, dentro do navegador:

   | Parte | Antes | Depois |
   |---|---|---|
   | Cenário atrás do personagem | 16,1 ms | 1,8 ms |
   | Água, na frente | 16,6 ms | 0,2 ms |
   | Fundo de morros | 3,1 ms | 1,2 ms |
   | **Quadro inteiro** | **35,7 ms** | **3,0 ms** |

   Para 60 FPS, cada quadro precisa caber em 16,7 ms.
   **Causa:** as duas imagens grandes do cenário usavam **transparência por pixel**. A cada quadro, o navegador misturava os 518 mil pixels da tela de cada camada, até os vazios. A da água é quase toda vazia e custava o mesmo.
   **Correção:** pixel art não tem "meio transparente" (conferi: **nenhum** pixel semitransparente na arte da Kenney). Então troquei por uma **cor-chave**: um rosa que não aparece na arte, tratado como "vazio", com compressão **RLE**, que pula os trechos vazios de uma vez. O visual é idêntico, e conferi numa captura.
   No fundo de morros, a transparência nem era necessária, porque os blocos são 100% opacos.

5. **"Esc: sair" no navegador não fazia nada.** O texto agora só aparece no PC.

## Como testei
- **No navegador interno do app**, com o servidor do pygbag (`--servir`):
  - li o terminal do Python dentro da página (`#debug`);
  - conferi a tela de escolha com o teclado de verdade;
  - escolhi a Dark e entrei na Floresta.
- **Lógica dentro do navegador:** rodei 150 quadros simulando a seta segurada e um pulo. A personagem andou 530 px, pulou 102 px (no PC são uns 107) e voltou ao chão, e a câmera acompanhou.
- **No PC:** Ruff sem problemas e **59 de 59 testes passando**. O desenho de um quadro no PC caiu para cerca de 1 ms.

## Decisões que tomei sozinho (para você revisar)
- **Lista de permissão** em vez de consertar a lista de bloqueio do pygbag. É mais segura e funciona em qualquer sistema.
- **Cor-chave rosa** `(255, 0, 255)` para "vazio" no cenário. Se um dia entrar uma arte com esse rosa exato, ou com pixels semitransparentes (sombra suave, brilho), essa parte precisa ser revista. Deixei o aviso no código.
- O `web.zip` (para o itch.io) é gerado a cada montagem, em `build/`, que fica fora do GitHub.

## Pendências
- **FPS real com a janela visível:** o painel do navegador estava escondido durante o teste, e assim o navegador pausa a animação. Por isso medi o tempo de desenho, e não o FPS na tela. **Teste você mesmo** com o comando `--servir` e jogue um pouco.
- **Publicar no itch.io:** o `web.zip` já sai pronto, mas a publicação precisa da sua conta e está prevista para a v0.3.
- **Sons:** quando entrarem, precisam estar em **OGG** (regra do navegador).
- O GitHub Actions ainda não monta a versão web. Dá para automatizar depois.

## Para debater
1. Rode `uv run python scripts/montar_web.py --servir`, clique na página e jogue. O jogo está rápido no seu navegador?
2. Quer que o GitHub Actions monte a versão web automaticamente a cada merge? Seria o primeiro passo para publicar no itch.io sem trabalho manual.
