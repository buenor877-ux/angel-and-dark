# Relatório: Parte 6, o javali (primeiro inimigo da Floresta)
Data: 28/11/2026 | Branch: `parte-06-javali`

## O que foi pedido (escolhas do Leonardo)
- **Primeiro inimigo:** o **javali** (planta e vespa ficam para depois).
- **Comportamento:** patrulha + investida.
  - Anda devagar de um lado para o outro e vira na borda ou na parede.
  - Ao ver o jogador na frente, para, **treme** (o aviso) e investe rápido em linha reta.
- **Encostar nele** tira 1 coração, com o empurrão que já existia.
- **Pular em cima derrota**, com um quiquinho para cima (estilo Mario). Os poderes viram outra forma de derrotar quando existirem.
- **3 javalis na Floresta 1**, um a cada 2 telas:
  - tela 2, em chão plano, para aprender;
  - tela 4, depois do checkpoint;
  - tela 5, perto de um buraco.
  - Nenhum na tela 1 nem perto do checkpoint.

## O que foi feito
- **`jogo/inimigos/inimigo.py`, a classe base `Inimigo`.** Tudo o que qualquer inimigo vai ter:
  - corpo, gravidade e colisão com o chão e as paredes;
  - **território**: um retângulo de onde ele nunca sai;
  - "tem chão à frente?" (para não cair de borda nem entrar na água);
  - levar pisão, ser derrotado (fica amassado 0,4 s e some) e machucar quem encosta.
- **`jogo/inimigos/javali.py`, a classe `Javali`,** herda de `Inimigo` e só escreve o próprio comportamento. Tem uma **máquina de estados** com 4 estados:

  | Estado | O que faz | Quando muda |
  |---|---|---|
  | `PATRULHA` | anda a 60 px/s, vira na borda, na parede ou no fim do território | viu o jogador → `AVISO` |
  | `AVISO` | para, **treme** e fica avermelhado | depois de 0,6 s → `INVESTIDA` |
  | `INVESTIDA` | corre a 330 px/s em linha reta (o jogador anda a 260) | chegou na borda ou na parede → `DESCANSO` |
  | `DESCANSO` | parado, "cansado" | depois de 0,8 s → `PATRULHA` |

  Ele só enxerga **para a frente**: se você chega por trás, ele não vê.
- **`jogo/inimigos/__init__.py`:** uma tabelinha `TIPOS` que liga o nome do objeto no Tiled (`"javali"`) à classe. Quando a planta e a vespa chegarem, é só acrescentar uma linha.
- **No Tiled (`assets/mapas/01_floresta.tmx`):** 3 retângulos chamados `javali` na camada `objetos`. **O retângulo é o território:** o javali nasce no meio, com os pés no fundo do retângulo, e anda só até as pontas. Para mudar um javali de lugar ou aumentar a área dele, é só mexer no retângulo no Tiled.
- **Carregador (`carregador_fases.py`):** lê esses retângulos e entrega para a fase como "lugar de inimigo" (`LugarInimigo`: tipo + área). A fase não conhece as classes de inimigo; quem cria o javali de verdade é a cena.
- **Cena da fase:**
  - cria os inimigos, move e desenha todos a cada quadro;
  - **pisão:** se os pés do jogador estavam acima do topo do javali no quadro anterior e ele está caindo, o javali é derrotado e o jogador quica para cima;
  - **segurar o pulo** no pisão faz o quique ser mais alto, porque o "corte do pulo" que já existia vale aqui também;
  - encostar de qualquer outro jeito: 1 coração e o empurrão para longe do javali.
- **Personagem:** ganhou `quicar(forca)`.
- **Arte provisória:** retângulo marrom com uma "presa" clara e um olho do lado para onde ele olha. A folha da Kenney que temos (`kenney_tiles.png`) só tem blocos de cenário, sem bichos, por isso ficou o retângulo.

## Os números ficaram na config
Arquivo novo **`config/inimigos.toml`**:
- `[geral]`: gravidade, tolerância do pisão, força do quique e tempo do amassado;
- `[javali]`: tamanho, cores, velocidades, distância de visão, tempo de aviso, tremida e descanso.

## Conceitos novos
- **Herança de novo, agora nos inimigos.** `Inimigo` tem o que é comum; `Javali` só tem o método `pensar()`, que decide para onde andar. A física fica na classe base. A planta e a vespa vão herdar da mesma classe.
- **"Padrão legível"** (docs/04): todo ataque tem um aviso antes. O javali para, treme e fica vermelho antes de investir. Quem presta atenção tem tempo de pular por cima ou de pisar nele.
- **Separar "onde" de "o quê":** o mapa diz *onde* fica o inimigo (retângulo no Tiled); o código diz *o que* ele faz; a config diz *quanto* (velocidade, tempo). Dá para ajustar cada coisa sem tocar nas outras.
- **Detectar o pisão pela posição anterior:** no quadro do contato, o jogador já está "dentro" do javali, então não dá para saber de onde veio olhando só para agora. Por isso a cena guarda onde estavam os pés **antes** de mover.

## Arquivos
- Novos: `jogo/inimigos/inimigo.py`, `jogo/inimigos/javali.py`, `config/inimigos.toml`, `tests/test_inimigos.py`, este relatório.
- Alterados: `jogo/inimigos/__init__.py`, `jogo/fases/fase.py`, `jogo/fases/carregador_fases.py`, `jogo/cenas/cena_fase.py`, `jogo/personagens/personagem.py`, `assets/mapas/01_floresta.tmx`.

## Testes
- Ruff: sem problemas.
- pytest: **77 de 77 passando** (eram 59). Os 18 novos conferem:
  - **Patrulha:** nasce no meio da área com os pés no chão; vai e volta sem sair da área; vira na borda do chão sem cair; vira na parede.
  - **Visão e ataque:** vê o jogador na frente, mas não atrás, nem longe, nem muito acima; avisa **parado e tremendo** e só então investe; a investida para no fim da área, descansa e volta a patrulhar; a investida não cai da borda; reiniciar volta ao começo, vivo.
  - **Na cena:** cair em cima derrota e quica, sem perder coração; encostar de lado tira 1 coração e empurra para longe; o derrotado some e não machuca; perder uma vida traz os inimigos de volta; o desenho funciona em todos os estados.
  - **No mapa:** há 3 javalis, nas telas 2, 4 e 5; nenhum perto do início nem do checkpoint; cada javali da Floresta patrulha 20 segundos sem cair e sem ficar preso; os nomes do carregador e da tabela de inimigos combinam.
- **Jogo rodado sem janela**, com comandos simulados. Na ordem:
  1. cheguei perto do javali 1 andando para a direita;
  2. ele me viu, parou e tremeu (vermelho);
  3. investiu e me acertou (perdi 1 coração);
  4. caí em cima do javali 2: ele amassou e sumiu, e eu quiquei;
  5. o javali 3 patrulhava no alto, logo depois do buraco com água.

  Conferi as imagens.
- **Versão web:** `scripts/montar_web.py` montou normalmente (104 KB), já com `config/inimigos.toml` e os arquivos novos.

## Problemas encontrados e corrigidos
1. **Quebras de linha do Windows.** O script que editou `fase.py` e `carregador_fases.py` gravou as linhas no formato do Windows (CRLF), e o git avisou. Voltei para o formato normal (LF) antes do commit, para o diff mostrar só o que mudou de verdade.
2. **Um teste meu estava errado, não o javali.** No teste "vira na borda", o meio da área ficava fora do chão, então o javali nascia no ar e caía. Corrigi o teste para a área começar em cima do chão. (Fica a lição: quando um teste falha, primeiro conferir se o teste está certo.)
3. **Teste frágil demais:** "nasce exatamente no x 600" falhava por 1 pixel, porque no primeiro quadro ele já deu um passinho. Agora aceita até 2 px.

## Decisões que tomei sozinho (para você revisar)
- **Lugar exato de cada javali:**
  - javali 1 no chão baixo da tela 2, entre o bloco alto e a água (colunas 45 a 56). Tem uma plataforma em cima dele; por isso o javali tem 30 px de altura, para passar por baixo dela;
  - javali 2 no chão logo depois da água da tela 4 (colunas 99 a 111), até o bloco alto;
  - javali 3 em cima do bloco alto logo depois da água da tela 5 (colunas 127 a 135). Cuidado: o empurrão pode jogar você na água!
- **O javali não sai do território, nem investindo.** Você tinha dito "até bater ou chegar na borda". Ficou assim, mas o fim do território também conta como borda. Sem isso, o javali 2 poderia correr até o checkpoint.
- **Ao perder uma vida, todos os javalis voltam**, até os derrotados. É o mais comum nos jogos de plataforma e deixa o trecho igual a cada tentativa.
- Os inimigos **não se machucam** nos espinhos (passam por cima deles).
- **Números:** patrulha 60, investida 330, visão de 300 px, aviso de 0,6 s, descanso de 0,8 s, quique de 480.
- O javali começa olhando para a esquerda, porque o jogador vem da esquerda.

## Pendências
- **Arte de verdade do javali** (andar, aviso, investida, amassado). Por enquanto é um retângulo.
- **Som** do aviso, da investida e do pisão (parte dos sons, com o sfxr).
- **Planta e vespa**, os outros 2 inimigos da Floresta no docs/04. O docs/03 pede 2 tipos de inimigo na versão 0.1.
- **Corações ao derrotar inimigos** (docs/03): ainda não caem.
- Derrotar com **poderes** (luz e raios negros), quando os poderes existirem.

## Para debater
1. A investida está rápida demais, ou o aviso de 0,6 s está curto?
2. Os 3 javalis estão bem colocados? O da tela 5, perto da água, está difícil demais?
3. Os javalis devem voltar ao perder uma vida, ou quem foi derrotado fica derrotado?
4. Parte 7: o segundo inimigo (planta que cospe sementes ou vespa)? Ou começar os poderes?
