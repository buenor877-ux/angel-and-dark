# Relatório: Parte 2, a Dark entra no jogo
Data: 28/11/2026 | Branch: `parte-02-dark`

## O que foi pedido
Tela para escolher entre Angel e Dark; Dark como quadrado provisório; mesmos controles; **movimento igual nos dois, diferentes só nos poderes**; voltar à escolha por uma tecla.

## O que foi feito
- **Tela de escolha:** setas ou A/D escolhem, Enter ou Espaço confirmam, Esc sai. O personagem selecionado ganha uma moldura dourada.
- **A Dark:** quadrado roxo. Preto sumiria no fundo escuro, e o roxo é da paleta dele.
- **Esc na fase volta à escolha** já marcando o último personagem usado, para trocar e voltar rápido.
- **Decisão registrada** em `docs/05_personagens.md`: movimento igual, com a possibilidade de rever depois de forma equilibrada.

## A herança em ação
A Parte 1 preparou isto. A classe da Dark inteira é:
```python
class Dark(Personagem):
    nome = "Dark"
    chave = "dark"
```
Andar, pular, coiote, buffer e colisão vêm de `Personagem`, sem copiar nenhuma linha. Quando os poderes entrarem, cada um vai escrever só o que é dele.

## Config: um bloco compartilhado
`config/personagens.toml` agora tem três blocos:
- `[movimento]`: os números que os dois usam.
- `[angel]` e `[dark]`: só o que é de cada um (por enquanto, a cor).

Se um dia você quiser a Dark 10% mais rápida, basta escrever `velocidade = 286` no bloco `[dark]`, porque o valor do personagem vence o compartilhado. Está explicado no próprio arquivo.

## O Jogo virou o "gerente" das cenas
A escolha precisa abrir a fase, e a fase precisa voltar para a escolha. Se uma importasse a outra, o Python acusaria **importação circular** (A precisa de B, que precisa de A). A solução foi as cenas pedirem ao `Jogo`: `iniciar_fase()`, `ir_para_escolha()` e `sair()`. Assim, nenhuma cena conhece a outra, e adicionar o menu ou o game over depois fica fácil.

## Arquivos
- **Novos:** `jogo/personagens/dark.py`, `jogo/cenas/cena_escolha.py`, `tests/conftest.py`, `tests/test_personagens.py`, `tests/test_cenas.py`, este relatório.
- **Alterados:** `jogo/nucleo/jogo.py` (troca de cenas), `jogo/cenas/cena_teste.py` (recebe qualquer personagem), `jogo/personagens/personagem.py` (`carregar_config` e `criar`), `jogo/personagens/angel.py`, `config/personagens.toml`, `config/jogo.toml` (cor de destaque), `README.md`, `docs/05_personagens.md`, `tests/test_angel.py` e `tests/test_fase.py`.

## Testes
- Ruff: sem problemas.
- pytest: **23 de 23 passando** (eram 14). Os novos testes conferem:
  - os dois herdam de `Personagem`;
  - as cores são diferentes;
  - **Angel e Dark fazem exatamente o mesmo trajeto num pulo**, quadro a quadro. Esse teste protege a sua decisão: se alguém mudar o movimento de um sem querer, ele reprova;
  - a navegação na escolha, Enter iniciando a fase com o personagem certo, Esc na escolha e Esc na fase.
- O teste de alcance das plataformas agora calcula o pulo **dos dois** e usa o menor.
- O jogo rodou com teclas simuladas: escolheu a Dark, entrou na fase, pulou e voltou para a escolha com Esc.

## Problema encontrado e corrigido
Na primeira versão, a tela de escolha criava os dois personagens **a cada quadro** só para pegar nome e cor. Isso fazia o jogo ler o arquivo de config 60 vezes por segundo. Não travaria agora, mas é o tipo de desperdício que pesa no navegador. Agora os personagens são criados uma vez só.

## Decisões que tomei sozinho (para você revisar)
- A cor roxa da Dark, a moldura dourada e o Esc para voltar (os espaços do roteiro que ficaram em branco).
- Espaço confirma a escolha, além do Enter, para usar a mesma mão do pulo.

## Pendências
- No navegador, "Esc: sair" não faz nada, porque lá não existe fechar o programa. O texto vai ser ajustado quando testarmos o pygbag.
- O pygbag continua sem teste.

## Para debater
1. A tela de escolha está clara? Faltou algo, como uma frase sobre cada personagem?
2. Para a Parte 3, a sugestão é **câmera e fase maior que a tela**.
