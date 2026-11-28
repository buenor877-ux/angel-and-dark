# Relatório: Parte 3, câmera e fase maior
Data: 28/11/2026 | Branch: `parte-03-camera`

## O que foi pedido (escolhas do Leonardo)
- Fase de **3 telas** de largura.
- Câmera **suave e olhando à frente**.
- No pulo, a câmera **só muda de altura ao pisar num lugar mais alto**.
- **Bandeira de chegada**: ao tocar nela, aparece "Fase concluída!" e o jogo volta para a escolha.

## O que foi feito
- **Fase de 2880 × 1080 px** (3 telas de largura, 2 de altura), dividida em três trechos:
  - **tela 1:** aquecimento;
  - **tela 2:** uma escada que sobe até um mirante, para a câmera ter o que acompanhar;
  - **tela 3:** um caminho no alto e a descida até a bandeira.
  - O chão tem dois buracos, e as medidas respeitam a regra dos 85%.
- **Câmera** (`jogo/fases/camera.py`):
  - **Horizontal:** segue com atraso suave e mostra 120 px a mais para o lado em que o personagem anda.
  - **Vertical:** guarda a altura do último lugar em que o personagem pisou. Durante o pulo, ela não se mexe. Só acompanha no ar se o personagem chegar perto da borda de cima ou de baixo da tela, para ele nunca sumir de vista (numa queda num buraco, por exemplo).
  - **Nunca mostra o lado de fora do mundo:** nas bordas, ela para.
  - **Depois de uma queda,** pula direto para o personagem, sem suavizar, para o jogador não ver a câmera "viajando" pela fase.
- **Paredes invisíveis** nas laterais: o personagem não sai do mundo.
- **Bandeira dourada:** ao tocar nela, o personagem congela, aparece "Fase concluída!" e, 2 segundos depois, o jogo volta para a escolha.
- **Otimização:** a fase só desenha as plataformas que aparecem na tela. Com 14 plataformas, isso não faz diferença, mas uma fase real vai ter centenas.

## Conceitos novos desta parte
**Mundo × tela.** Agora existem duas coordenadas. O personagem está na posição 2.000 do **mundo**, mas aparece na posição 400 da **tela**. A câmera faz essa conversão em `na_tela()`. O texto do topo não passa pela câmera, por isso fica parado.

**Suavizar igual em qualquer FPS.** Uma câmera que anda "10% do caminho por quadro" ficaria mais lenta a 30 FPS do que a 60. Usei uma fórmula com exponencial (`1 - e^(-velocidade × dt)`) que dá o mesmo resultado em qualquer FPS. É o mesmo cuidado que tivemos com o corte do pulo na Parte 1.

## Os números ficaram na config
Em `config/jogo.toml`, bloco `[camera]`: `suavidade_x`, `suavidade_y`, `olhar_frente`, `altura_personagem` (onde ficam os pés na tela), `margem_topo` e `margem_base`. Dá para ajustar a sensação da câmera sem mexer no código.

## O teste de alcance ficou mais esperto
A fase nova tem um caminho no alto que se alcança **pelo lado**, na mesma altura, e não por baixo. O teste antigo só olhava para baixo e reprovaria uma fase válida. Agora ele **percorre a fase como um jogador**: parte do chão, vê aonde dá para pular, depois aonde dá para pular dali, e assim por diante. Se sobrar alguma plataforma sem visita, o teste reprova e diz qual é.
Também criei um teste para **o próprio teste**: ele coloca de propósito uma plataforma impossível e confere se ela é pega. Um teste que nunca reprova não protege nada.

## Arquivos
- **Novos:** `jogo/fases/camera.py`, `tests/test_camera.py` (6 testes), este relatório.
- **Alterados:**
  - `jogo/fases/fase.py`: tamanho, chegada, paredes, desenho com a câmera;
  - `jogo/cenas/cena_teste.py`: câmera e bandeira;
  - `jogo/personagens/personagem.py`: lado para onde o personagem olha e desenho com a câmera;
  - `config/fase_teste.toml` e `config/jogo.toml`;
  - testes de fase, cenas e personagens;
  - acentos nos textos da tela ("Espaço", "concluída").

## Testes
- Ruff: sem problemas.
- pytest: **35 de 35 passando** (eram 23). Os novos conferem que a câmera:
  - não mostra fora do mundo;
  - segue suave;
  - olha para o lado certo;
  - **não acompanha o pulo**;
  - sobe ao pisar mais alto;
  - desce numa queda.
  
  Também conferem as paredes, a bandeira e a volta para a escolha depois de 2 segundos, e que todas as plataformas são alcançáveis.
- O jogo rodou com comandos simulados. Conferi nas imagens: a câmera no início (canto de baixo), no mirante (subiu e deixou o personagem a 70% da tela) e na bandeira ("Fase concluída!" e volta para a escolha).

## Problemas encontrados e corrigidos
1. **O teste de alcance reprovaria uma fase válida** (o caminho no alto alcançado pelo lado). Reescrevi o teste para percorrer a fase.
2. **Textos sem acento:** eu tinha escrito "Espaco" com medo de a fonte não ter "ç". Testei, a fonte tem, e corrigi.

## Decisões que tomei sozinho (para você revisar)
- A altura da fase (2 telas) e o desenho dela.
- Personagem a 70% da altura da tela e 120 px de "olhar à frente".
- 2 segundos na tela de "Fase concluída!".
- Bandeira dourada, na mesma cor da moldura da escolha.

## Pendências
- O fundo ainda é liso. Sem desenhos no fundo, a sensação de movimento da câmera fica menor. Isso muda quando a arte entrar (Parte 4, com Tiled e tileset).
- pygbag continua sem teste.

## Para debater
1. A câmera está confortável? Rápida, lenta, olha demais ou de menos para a frente?
2. Na escada, a câmera subir só ao pisar ficou bom?
3. Parte 4: **primeira fase no Tiled, com um pacote de arte pronto**, o começo da Floresta. Vai ser preciso baixar um pacote gratuito (Kenney, por exemplo), e eu peço a sua permissão antes.
