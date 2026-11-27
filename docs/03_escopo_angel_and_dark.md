# Angel and Dark: escopo (em construção)
Início da conversa: 26/11/2026.

## Decisões já tomadas
- Nome do jogo: **Angel and Dark**
- Estratégia: começar **pequeno (versão Mini)**, publicar e crescer aos poucos até o projeto grande (1.0 → 1.1 → 2.0).
- Gênero: plataforma 2D **com quebra-cabeças de cenário**, com personagens, vilões e história próprios. Inspiração de estilo no Mario, mas nada da Nintendo.
- **Dois personagens jogáveis**, cada um com 4 habilidades: 2 para atravessar o cenário (remover obstáculos, abrir caminhos) e 2 para atacar.

## Personagens (ideia do Leonardo, 26/11)
| | **Angel** (feminina) | **Dark** (masculino) |
|---|---|---|
| Tema | Luz | Escuridão |
| Cenário 1 | **Teletransporte** | **Supervelocidade** |
| Cenário 2 | **Super inteligência** | **Sombras** (usar as sombras para passar e acessar áreas) |
| Ataque 1 | **Poder de luz** | **Raios negros** |
| Ataque 2 | **Super força** | **Ataque de sombras** (manipular sombras para atacar) |

## Como cada habilidade pode funcionar no jogo (sugestões para discutir)
- **Teletransporte (Angel):** atravessar paredes finas, grades ou buracos grandes, aparecendo do outro lado.
- **Super inteligência (Angel):** "visão analítica" que revela caminhos escondidos e pontos fracos, ou resolve mecanismos (alavancas, portas com código, máquinas).
- **Supervelocidade (Dark):** corrida rápida para passar por pontes que desabam, portas que fecham rápido e saltos longos.
- **Sombras (Dark):** virar sombra para passar por frestas, ou andar por superfícies escuras que só ele consegue usar.
- **Ataques:** cada personagem com 1 ataque à distância (luz / raios negros) e 1 de perto (super força / sombras).
- **Regra de design:** cada obstáculo pede um personagem específico. Isso obriga a **trocar de personagem**, e a troca vira a marca do jogo.
- Ideia extra: a luz de Angel cria sombras que Dark pode usar (os dois poderes se completam).

## Proposta revisada (26/11): publicar por partes até as 10 fases
| Versão | Conteúdo | Para quê |
|---|---|---|
| 0.1 "fatia" | 1 fase completa (fase 1) com os dois personagens, 2 inimigos, checkpoint e o chefe | Provar que tudo funciona junto; primeira coisa jogável |
| 0.3 Demo | Fases 1 a 3 com seus chefes, menu de escolha de personagem | **Primeira publicação** (itch.io + GitHub + post) |
| 0.5 / 0.7 | +2 fases a cada atualização | Crescer aos poucos, cada versão publicada |
| 1.0 | As 10 fases e o chefe final | Jogo completo |

## (proposta anterior, substituída pela tabela acima) Versão Mini
- **Os dois personagens**, trocando com uma tecla (a troca é a essência do jogo, então já entra na Mini).
- **2 habilidades de cada** (1 de cenário + 1 de ataque):
  - Angel: teletransporte + poder de luz
  - Dark: supervelocidade + raios negros
- **3 fases curtas:** fase 1 ensina Angel, fase 2 ensina Dark, fase 3 mistura os dois e termina num chefe simples.
- 2 tipos de inimigo, itens para coletar, vidas, game over e tela de vitória.
- Publicação: itch.io (jogável no navegador) + GitHub.

## Para as próximas versões
- Super inteligência e sombras (Angel e Dark): segunda habilidade de cenário
- Super força e ataque de sombras: segundo ataque
- Mais fases, mais inimigos e mais chefes, mundo com mapa, história com diálogos, save

## Respostas do Leonardo (26/11)
1. **Um jogador**, que **escolhe jogar com Angel ou com Dark** (não os dois juntos na fase). Pegada do Mario: passar a fase sobrevivendo.
   - Consequência: **toda fase precisa poder ser vencida com qualquer um dos dois** (dois caminhos, ou obstáculos que os dois resolvem cada um do seu jeito). Isso substitui a ideia de "trocar de personagem na fase".
2. **História:** Angel e Dark eram rivais, acabaram gostando um do outro e uniram forças para vencer um mal maior e trazer a paz. (Falta definir quem é o vilão principal.)
   - Visão do jogo: **10 fases** com temas diferentes, cada uma com mecânicas próprias, dificuldade crescente, **inimigos únicos** do tema da fase e **um chefe no fim de cada fase**. O jogador precisa **ler o padrão** dos inimigos para vencer; o chefe tem o padrão mais difícil.
3. **Vida:** 3 vidas. Perdeu uma, volta do último **checkpoint**. Perdeu as 3, recomeça do início da fase onde parou.
4. **Visual:** ele pediu explicação de 8-bit × 16-bit (respondida em 26/11).

## Ponto de atenção: tamanho
10 fases × inimigos únicos × 10 chefes × 2 personagens jogáveis é o **jogo completo (v1.0)**, não a Mini. Proposta: manter as 10 fases como meta e publicar por partes (ver abaixo).

## Decisões de 26/11 (segunda rodada)
- **Escolha do personagem: antes de cada fase** (o jogador pode alternar para não enjoar).
- **Visual: 16-bit** (estilo Super Nintendo / Mega Drive, com bastante detalhe).
- **Chefes:** cada fase 1–9 tem um **sub-chefe** (desafiador, mas não tanto); o **vilão principal é o chefe da fase 10**, o mais difícil.
- **Dano (ideia dele):** levou ataque, perde 1, fica piscando e volta ao normal; perdeu as 3, morre de verdade.
- **Proposta de sistema (para ele aprovar):**
  - Cada tentativa tem **3 corações**. Levou dano: perde 1 coração, pisca ~1,5 s invulnerável e é empurrado para trás.
  - Zerou os corações ou caiu num buraco: perde **1 vida** e volta ao último **checkpoint** com os corações cheios.
  - **3 vidas.** Perdeu as 3: recomeça a fase do início (e pode trocar de personagem).
  - Corações aparecem às vezes ao derrotar inimigos; juntar 100 orbes (luz para Angel, sombra para Dark) = +1 vida.
  - Barra de **energia** para os poderes especiais (gasta ao usar, recarrega com o tempo ou com orbes).
  - 3 **itens secretos** por fase, para dar motivo de jogar de novo com o outro personagem.
- **Temas das 10 fases:** ele já tem todos (enviar).

## Estimativa de esforço (explicada a ele em 26/11)
- Base do jogo (movimento, física, câmera, colisões, 2 personagens com poderes, menus, checkpoints, save): ~100 h.
- Arte 16-bit dos 2 protagonistas (andar, pular, 4 poderes, dano, morte): ~50 h.
- Cada fase (desenho com 2 caminhos, 2–3 inimigos únicos com padrão, sub-chefe, arte do tema, som, testes): ~70–100 h.
- Total para 10 fases: ~800–1.100 h. Com semanas alternadas (~15 h/mês no jogo), passa de 4 anos; por isso publicar por partes (0.1 → 0.3 → ... → 1.0).

- **Aprovado em 26/11:** sistema de corações, vidas, orbes, energia e itens secretos ("deixa mais equilibrado, tem cara de ser viciante").
- **Foco declarado:** variedade (cenários e inimigos), desafio na medida certa, jogador analítico, vontade de continuar.
- **Temas das 10 fases e vilão:** ver `04_fases_angel_and_dark.md`.

## Perguntas em aberto
- Nome e visual do vilão principal (deus da guerra)
- Revisão das sugestões de mecânicas, inimigos e sub-chefes por fase

## Decisões técnicas (27/11/2026)
- **Motor:** Pygame-CE (Python), para reforçar o currículo de dev Python.
- **Plataforma:** navegador primeiro (itch.io, usando **pygbag** para rodar Pygame na web).
- **Papel do Claude:** par de programação. Ele escreve as partes difíceis (câmera, chefes) explicando linha a linha, e o Leonardo faz o resto.
- **Tempo por semana e prazo:** em aberto. Depois da conversa com um profissional de TI (27/11), o Leonardo está repensando a estratégia (foco em automação para pequenos negócios).

## Novo modelo de trabalho (27/11/2026)
- **Leonardo:** escreve o roteiro, escolhe as tecnologias e monta a estrutura de pastas, sempre com os motivos.
- **Claude:** comenta cada escolha (se funciona, pontos positivos e negativos, sugestões), constrói o jogo e entrega um **relatório a cada parte** (o que fez, por quê, arquivos alterados, testes, pendências) para debater antes da próxima.
- Objetivo: o Leonardo aprender como funciona um projeto real tomando as decisões, mesmo sem escrever todo o código.
- As escolhas técnicas anteriores (Pygame-CE, itch.io, par de programação) serão revistas com a lista completa: `06_tecnologias.md`. Pastas: `07_pastas.md`.
