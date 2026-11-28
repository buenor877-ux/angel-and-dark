# Relatório: Parte 5, vida, perigos e checkpoints
Data: 28/11/2026 | Branch: `parte-05-vida`

## O que foi pedido (escolhas do Leonardo)
- **Sistema de vida do docs/03, aprovado como está:**
  - 3 corações;
  - dano tira 1, faz o personagem piscar 1,5 s invulnerável e o empurra para trás;
  - zerar os corações ou cair num buraco tira 1 vida e volta ao checkpoint;
  - 3 vidas.
- **Perigos:** espinhos e água nos buracos.
- **2 checkpoints**, ativados ao passar.
- **Ao perder as 3 vidas:** tela "Fim de jogo" e volta para a escolha.

## O que foi feito
- **`jogo/personagens/vida.py`:** a classe `Vida` guarda corações, vidas e dois cronômetros (invulnerabilidade e empurrão). Ela só tem números, não sabe nada de pygame, e por isso é fácil de testar.
- **Personagem:**
  - ganhou `levar_dano(origem_x)`: perde 1 coração e é empurrado **para longe** do perigo;
  - durante o empurrão (0,25 s), o controle não responde. Sem isso, o jogador anularia o empurrão na hora;
  - enquanto está invulnerável, pisca 10 vezes por segundo.
- **No Tiled (`01_floresta.tmx`)**, duas camadas novas:
  - `perigos`: 6 espinhos, em 3 pares;
  - `agua`: nos dois buracos.
  - Também entraram 2 bandeirinhas `checkpoint` na camada de objetos.
- **Carregador:** entende as novas propriedades de camada:
  - `perigo`: encostou, leva dano;
  - `altura_dano`: quanto do bloco machuca. Nos espinhos, só os 40% de baixo, porque o espinho não ocupa o bloco todo;
  - `frente`: a camada é desenhada **na frente** do personagem. Por isso ele "afunda" na água.
- **Checkpoints:** ficam cinza até você passar e ganham cor depois. Pular por cima também ativa. Ao perder uma vida, você volta ao **último ativo**.
- **HUD** (`jogo/interface/hud.py`, a primeira coisa na pasta `interface/`): corações da própria folha da Kenney e o contador de vidas.
- **A cena ganhou máquina de estados:** `JOGANDO`, `CONCLUIDA` e `FIM_DE_JOGO`. É a mesma ideia dos estados do personagem, aplicada à fase.

## Os números ficaram na config
`config/personagens.toml`, bloco `[vida]`: corações, vidas, tempo invulnerável, tempo de empurrão e as duas forças do empurrão.

## Testes
- Ruff: sem problemas.
- pytest: **59 de 59 passando** (eram 42). Os novos conferem:
  - **Vida:** começa com 3 e 3; o dano tira 1 e um segundo dano logo depois é ignorado; a invulnerabilidade acaba depois de 1,5 s; o personagem pisca; perder uma vida recupera os corações; a última vida avisa que acabou.
  - **Personagem:** o empurrão vai para longe do perigo, o controle fica travado durante ele e volta depois.
  - **Regras da fase:** espinho tira coração; zerar os corações volta ao início; o checkpoint muda o ponto de volta; 3 vidas perdidas mostram "Fim de jogo" e voltam para a escolha.
  - **Mapa:** existem espinhos, 2 checkpoints e a água; a área de dano do espinho é só a parte de baixo; **cada checkpoint está num chão alcançável**; o ponto de volta é o último checkpoint ativo.
- O jogo rodou com comandos simulados. Na ordem: encostou no espinho (2 corações), passou no checkpoint (ativou), caiu na água (perdeu 1 vida), voltou ao checkpoint (3 corações, 2 vidas). Conferi as imagens.

## Problemas encontrados e corrigidos
1. **O carregador perderia checkpoints.** Ele guardava os objetos do Tiled num dicionário pelo nome, e com dois objetos chamados "checkpoint", o segundo apagaria o primeiro. Reescrevi para percorrer a lista. Esse problema já existia na Parte 4, mas só apareceu quando passou a existir um nome repetido.
2. **"Voltar para a escolha" era pedido a cada quadro** depois dos 2 segundos, e não uma vez só. No jogo não aparecia, porque o `Jogo` troca a cena no primeiro pedido, mas o teste pegou. Agora a cena pede uma única vez.
3. **Checkpoint rígido demais:** a primeira versão só ativava se você passasse **pelo chão**. Pular por cima não contava. Corrigi para ativar ao passar em qualquer altura.

## Decisões que tomei sozinho (para você revisar)
- Posição dos espinhos e dos checkpoints na fase.
- Força do empurrão (320 para o lado, 380 para cima) e 0,25 s sem controle.
- A área de dano do espinho: os 40% de baixo do bloco, menos 15% de cada lado.
- Bandeirinha cinza quando apagada e colorida quando ativa.
- O contador "Quedas" saiu do HUD, porque agora quem mostra isso são as vidas.

## Pendências
- Ainda não existem orbes, itens de cura nem "+1 vida". Estão no docs/03 e podem entrar depois.
- O dano não tem som. Os sons entram numa parte própria, com o sfxr.
- pygbag continua sem teste.

## Para debater
1. O empurrão está forte ou fraco? O piscar está claro?
2. Os espinhos estão bem colocados? Difícil demais ou fácil demais?
3. Parte 6: sugestão de **primeiro inimigo da Floresta** (o javali), agora que já existe dano e vida.
