# Relatório: Parte 7, a planta e a vespa (fechando os inimigos da Floresta)
Data: 28/11/2026 | Branch: `parte-07-planta-vespa`

## O que foi pedido
- **Planta que cospe sementes:**
  - fica parada e atira num ritmo fixo, sempre com aviso antes;
  - a semente é um projétil que machuca e some ao bater em parede, chão ou no personagem;
  - o **sistema de projéteis** tem que ser genérico, para servir depois ao arqueiro, à salamandra e a outros;
  - decidir se dá para pisar nela e explicar a escolha.
- **Vespa em zigue-zague:** voa num padrão previsível; encostar machuca; pisar derrota, com o quique do javali.
- Números em `config/inimigos.toml`, posições no Tiled.
- **Quantos e onde:** decisão minha, seguindo "ensinar → testar → surpreender" e mantendo a fase justa.

## O que foi feito

### 1. Sistema de projéteis (`jogo/projeteis/`)
A classe nova `Projetil` é "qualquer coisa que voa sozinha e machuca". Ela não sabe se é semente, flecha ou bola de fogo. Quem atira passa os números:

| Número | Semente (hoje) | Flecha do arqueiro (futuro) |
|---|---|---|
| `velocidade` | 220 | mais rápida |
| `velocidade_y` | 0 (sai reta) | negativa (sai para cima) |
| `gravidade` | 0 (voa reto) | positiva (faz arco) |
| `alcance` | 360 px | o que fizer sentido |

As regras valem para todo projétil:
- some ao bater em bloco sólido;
- some ao acertar o personagem, e acerta **uma vez só**;
- some depois de voar o `alcance`, para não ficar voando para sempre fora da tela.

**Quem cuida dos projéteis é a cena, não o inimigo.** O inimigo só coloca o que atirou numa lista (`disparos`), e a cena recolhe. Assim a semente continua voando mesmo se você pisar na planta logo depois do tiro. Mais tarde, os poderes da Angel e da Dark também podem soltar projéteis nessa mesma lista.

### 2. Planta (`jogo/inimigos/planta.py`)
Funciona como um **metrônomo** com 2 estados:

| Estado | O que faz | Quanto tempo |
|---|---|---|
| `ESPERA` | parada, verde | 1,6 s |
| `AVISO` | **incha e fica vermelha** aos poucos | 0,6 s, e então cospe |

- Um tiro a cada **2,2 s**, sempre igual. Quem observa um ciclo já sabe quando pular.
- Ela só "acorda" com o jogador a até 560 px (um pouco mais de meia tela). Longe, ela **dorme e guarda onde parou**, então o ritmo continua o mesmo quando você volta.
- **Aviso começado sempre termina em tiro.** Se o aviso pudesse "desistir", o jogador aprenderia que vermelho nem sempre é perigo.
- Cospe sempre **para o mesmo lado**. Por padrão é a esquerda, de onde o jogador vem. No Tiled dá para virar com a propriedade `olhando = "direita"` no objeto (vale para qualquer inimigo).
- A semente sai na **altura do peito** de quem está em pé: em pé, ela acerta; pulando, passa por baixo.

**Dá para pisar na planta? Sim**, como no javali. Os motivos:
1. **Uma regra só para a Floresta inteira:** "caiu em cima, derrota". Se cada inimigo tivesse uma regra, o jogador precisaria decorar exceções logo na primeira fase.
2. **Dá uma recompensa a quem observa:** quem aprende o ritmo pode pular a semente e cair em cima da planta, em vez de só fugir.
3. **Ela não fica invencível:** sem o pisão, a planta seria só um obstáculo até os poderes existirem.

Encostar nela **de lado** machuca, como no javali. Um inimigo que não dá para pisar (um cacto com espinhos em cima, por exemplo) fica guardado como "surpresa" para uma fase mais à frente.

### 3. Vespa (`jogo/inimigos/vespa.py`)
- Anda na horizontal e na vertical ao mesmo tempo, sempre na **mesma velocidade**, e rebate nas bordas do território, como uma bolinha numa caixa.
- Como sobe e desce bem mais rápido (120) do que anda (55), o caminho vira um **zigue-zague** de umas 3 dobras por travessia. Conferi desenhando o rastro dela numa captura: dá um "W".
- **Sempre o mesmo desenho:** um teste confere que, depois de reiniciar, ela faz exatamente o mesmo caminho.
- Não sente gravidade e **não bate em blocos**, por isso o território dela tem que ficar no ar livre (há um teste para isso no mapa).
- **Pisada**, pisca branco e cai reta até sumir.
- **Arte provisória:** retângulo amarelo com 2 listras, ferrão atrás e asas que batem.

### 4. A classe base `Inimigo` ganhou 3 coisas
- `propriedades`: o que vier do objeto no Tiled (hoje só `olhando`);
- `disparos`: a lista do que ele atirou neste quadro;
- **o desenho foi separado em pedaços** (`forma_desenho` e `desenhar_detalhes`). Antes, a presa do javali estava desenhada na classe base, e toda planta ia nascer com presa de javali! Agora cada inimigo desenha os próprios detalhes.

## Distribuição na Floresta (minha decisão)
Ficaram **7 inimigos**: os 3 javalis de antes, 2 plantas e 2 vespas. A tela 1 continua livre.

| Tela | Inimigo | Papel | Por quê |
|---|---|---|---|
| 2 | javali 1 | ensinar javali | já existia |
| 3 | **planta 1** | **ensinar planta** | chão plano e comprido. O bloco flutuante logo antes é um **mirante seguro**: em cima dele, a semente passa por baixo. Dá para assistir ao ritmo sem risco e só então descer. |
| 4 | **vespa 1** | **ensinar vespa** | logo depois do checkpoint, em chão plano, sem buraco embaixo. Errar aqui custa pouco: você volta do lado. |
| 4 | javali 2 | testar javali | já existia |
| 5 | **planta 2** | **testar planta** | em cima do bloco alto, com os **espinhos** entre você e ela. A semente vem na altura do peito: um pulo bem calculado passa a semente e os espinhos juntos. |
| 5 | javali 3 | testar javali | já existia (perto da água) |
| 6 | **vespa 2** | **surpreender** | guarda o chão logo **abaixo** do último bloco alto, onde você desce perto do fim. A novidade é ver a vespa **de cima**: quem espera ela subir desce tranquilo; quem pula sem olhar cai no caminho dela. |

**Como mantive a fase justa:**
- **A semente da planta 1 some antes do buraco com água** (alcance de 10 blocos). O empurrão de uma semente nunca joga ninguém na água num trecho de ensinar. Há um teste para isso.
- **Afastei a planta 1 duas colunas** depois de rodar o jogo. Na primeira posição, o empurrão da semente jogava o jogador em cima dos espinhos (veja "Problemas").
- **Nenhum território a menos de 64 px** do início ou do checkpoint. Os javalis continuam com a regra de 200 px, porque eles investem; a vespa e a planta não vêm atrás de você.
- **As duas vespas dão para passar por baixo e para pisar.** No ponto mais alto, ela fica acima da cabeça de quem está em pé. No mais baixo, desce até onde o pulo alcança. Um teste confere isso nas duas do mapa.
- As duas plantas olham para a esquerda. Quem volta no checkpoint fica **atrás** delas.

## Os números ficaram na config
Em `config/inimigos.toml`, três blocos novos:
- `[planta]`: tamanho, cores, `tempo_espera` (1,6), `tempo_aviso` (0,6), `inchaco` (4 px), `altura_boca` e a distância em que ela acorda;
- `[planta.semente]`: tamanho, cor, velocidade, gravidade e alcance da semente;
- `[vespa]`: tamanho, cores, `velocidade_x` (55), `velocidade_y` (120) e a velocidade da queda quando pisada.

## Conceitos novos
- **Separar "quem atira" de "o que voa".** A planta só decide *quando* atirar. A semente sabe *voar e bater*. A cena decide *o que acontece* quando acerta. Por isso o arqueiro vai poder reaproveitar o projétil sem mexer nele.
- **Tabela dentro de tabela no TOML** (`[planta.semente]`): a config da semente fica "dentro" da planta, e o código recebe um dicionário dentro de outro.
- **Método "gancho"** (`forma_desenho`, `desenhar_detalhes`): a classe base faz o trabalho comum e chama um método que cada filha pode trocar. É a mesma ideia do `pensar()` da Parte 6.
- **Movimento sem física:** a vespa troca o `_mover` da classe base (gravidade e colisão) pelo dela (rebater na caixa). Herdar não obriga a usar tudo o que veio da classe mãe.

## Arquivos
- **Novos:**
  - `jogo/projeteis/__init__.py` e `jogo/projeteis/projetil.py`;
  - `jogo/inimigos/planta.py` e `jogo/inimigos/vespa.py`;
  - `tests/test_projeteis.py` e `tests/test_planta_vespa.py`;
  - este relatório.
- **Alterados:**
  - `jogo/inimigos/inimigo.py`, `jogo/inimigos/javali.py` e `jogo/inimigos/__init__.py`;
  - `jogo/fases/fase.py` e `jogo/fases/carregador_fases.py`;
  - `jogo/cenas/cena_fase.py`;
  - `config/inimigos.toml`;
  - `assets/mapas/01_floresta.tmx` (4 objetos novos; nada do que já existia foi mexido);
  - `tests/test_inimigos.py`.

## Testes
- Ruff: sem problemas (`check` e `format`).
- pytest: **112 de 112 passando** (eram 78). Os 34 novos conferem:
  - **Projétil (8):**
    - sai no lugar certo e anda reto;
    - com gravidade, faz arco;
    - some na parede, no chão e depois do alcance;
    - acerta uma vez só e some;
    - não acerta quem está longe;
    - o desenho funciona.
  - **Planta (7):**
    - dorme com o jogador longe;
    - atira em **ritmo fixo** (todos os intervalos iguais a 2,2 s);
    - **todo tiro tem aviso antes**: ela fica o aviso inteiro vermelha e termina inchada;
    - aviso começado sempre vira tiro;
    - não anda;
    - a semente sai da boca, para o lado em que ela olha (e `olhando = "direita"` vira);
    - a semente vem na altura de quem está em pé.
  - **Vespa (4):**
    - nasce no meio e não cai;
    - faz **zigue-zague** (vira mais vezes na vertical do que na horizontal) sem sair do território, com velocidade constante;
    - repete **sempre o mesmo caminho**;
    - pisada, cai e some.
  - **Na cena (9):**
    - a semente acerta, tira 1 coração, empurra e some;
    - uma parede no meio bloqueia a semente;
    - pular a semente não machuca;
    - pisar na planta derrota e quica, e ela não atira mais;
    - encostar na planta de lado machuca;
    - pisar na vespa derrota e quica;
    - encostar na vespa machuca;
    - perder uma vida limpa as sementes no ar e traz a planta de volta;
    - o desenho funciona com tudo junto.
  - **No mapa (6):**
    - os 7 inimigos estão nas telas combinadas, com a tela 1 livre;
    - a volta de vida não cai dentro de nenhum território;
    - o território das vespas fica no ar livre;
    - as vespas dão para passar por baixo e para pisar;
    - as plantas ficam no chão;
    - a semente da planta 1 some antes do buraco com água.
- **Jogo rodado sem janela**, na Floresta de verdade, com comandos simulados e capturas que conferi:
  1. parado longe da planta 1, ela avisou (vermelha e inchada) e cuspiu; a semente sumiu antes de me alcançar;
  2. em cima do bloco flutuante, a semente passou por baixo, sem dano;
  3. parado na frente da planta 1, a semente acertou: 1 coração a menos e a semente sumiu;
  4. caí em cima da planta 1 e da vespa 1: as duas foram derrotadas, sem dano;
  5. desenhei o rastro da vespa 1: zigue-zague em "W";
  6. a planta 2 cuspiu por cima dos espinhos, no bloco alto;
  7. a vespa 2 aparece logo abaixo do último bloco alto.
- **Versão web:**
  - `scripts/montar_web.py` montou normalmente (120 KB);
  - no navegador interno do app, a tela de escolha abriu e a Floresta carregou com os inimigos novos, sem erro.

## Problemas encontrados e corrigidos
1. **O primeiro zigue-zague era quase uma diagonal.** Com o território quadrado e as velocidades parecidas (90 e 120), o rastro saía um losango torto, e não um zigue-zague. Deixei o território mais baixo (2 blocos de altura, no Tiled) e a vespa mais lenta na horizontal (55). Agora ela faz umas 3 dobras por travessia.
2. **O empurrão da semente jogava o jogador nos espinhos.** Na primeira posição da planta 1, quem levava a semente parado logo na frente dela era empurrado para trás, em cima dos espinhos. Só não doía por causa da invulnerabilidade depois do dano. Afastei a planta 2 colunas: agora o empurrão para antes dos espinhos.
3. **A presa do javali estava na classe base.** Se eu não separasse o desenho, a planta e a vespa nasceriam com presa de javali. Separei o desenho em `forma_desenho` e `desenhar_detalhes`.
4. **Duas falhas do meu roteiro de simulação, e não do jogo:** num pisão, eu pulei longe demais e passei por cima da planta; numa foto, deixei o jogador em cima de um espinho. Corrigi o roteiro. A lição da Parte 6 de novo: antes de culpar o jogo, conferir o teste.

## Decisões que tomei sozinho (para você revisar)
- **A planta pode ser pisada.** Os motivos estão lá em cima.
- **A planta não vira para o jogador.** Ela cospe sempre para o mesmo lado, e o Tiled decide qual. Ficou mais previsível, e quem volta no checkpoint fica atrás dela.
- **A semente voa reta e não cai.** A gravidade fica para a flecha do arqueiro (Medieval).
- **A semente passa por baixo dos blocos flutuantes de 1 bloco.** É por isso que o bloco antes da planta 1 serve de mirante.
- **Os números:**
  - planta: um tiro a cada 2,2 s (1,6 de espera + 0,6 de aviso);
  - semente: 220 px/s, mais devagar que o jogador, e alcance de 10 blocos;
  - vespa: 55 px/s na horizontal e 120 na vertical.
- **A vespa atravessa blocos** em vez de bater neles. Ela fica sempre no ar livre, e um teste confere isso.
- **O território da vespa vai até o chão.** No ponto mais baixo, ela raspa o chão, então você não passa por baixo dela a qualquer hora: precisa esperar ela subir.
- **Ao perder uma vida, as sementes no ar somem**, junto com a volta dos inimigos.
- **Propriedade `olhando` no Tiled** para qualquer inimigo: é útil para as próximas fases.

## Pendências
- **Arte de verdade** da planta, da vespa e da semente (por enquanto são retângulos e elipses).
- **Sons:** o "inchar" e o "cuspir" da planta e o zumbido da vespa.
- **Corações ao derrotar inimigos** (docs/03): ainda não caem.
- Derrotar com os **poderes**, quando existirem.

## Para debater
1. O ritmo da planta (um tiro a cada 2,2 s) e o aviso de 0,6 s estão bons? A semente está lenta demais?
2. A vespa está fácil ou difícil? Quer que ela **não** desça até o chão (aí sempre dá para passar por baixo)?
3. A vespa 2, no fim da fase, ficou uma boa "surpresa"? Ou prefere uma variação mais clara, como uma vespa mais rápida (dá para ter números diferentes por vespa, pelo Tiled)?
4. 7 inimigos numa fase de 6 telas: está bom para a primeira fase, ou cheio demais?
5. Próximas partes: 8 (orbes e itens secretos), 9 (fundo mais rico) e 10 (cipós). Segue nessa ordem?
