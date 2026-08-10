# Guia de Estudo — Air Hockey (Pygame)

## 1. Visão geral da arquitetura

O projeto é dividido em 3 módulos (separação de responsabilidades):

- **config.py** — constantes (LARGURA, ALTURA, FPS, cores), fontes e a função `carregar_e_escalar` (carrega/redimensiona imagens).
- **draws.py** — funções de desenho puras: `desenhar_raquete`, `desenhar_disco`, `desenhar_campo_personalizado`, `criar_botao`.
- **main.py** — orquestra tudo: inicializa o Pygame, carrega assets, guarda o estado do jogo e roda o game loop.

**Por que separar assim?** Facilita manutenção (mudar uma cor não exige mexer na lógica do jogo), permite reuso das funções de desenho em telas diferentes, e deixa o `main.py` focado só em "regras do jogo" + loop.

---

## 2. Máquina de estados (`estado_jogo`)

O jogo inteiro gira em torno de uma variável string: `estado_jogo`, que pode ser:
`"menu"`, `"tutorial"`, `"custom"`, `"singleplayer"`, `"multiplayer"`.

A cada frame, o código pergunta "em que estado estou?" e:
1. No bloco de eventos, decide **quais cliques/teclas fazem sentido** nesse estado.
2. No bloco de renderização (`if/elif estado_jogo == ...`), decide **o que desenhar**.

Isso é um padrão clássico de **máquina de estados finita (FSM)** aplicada a telas de jogo — cada estado é basicamente uma "tela" com sua própria lógica de entrada e saída.

Transições importantes:
- `menu → singleplayer/multiplayer` (clique nos botões) — sempre reseta o jogo via `reiniciar_jogo_completo`.
- `qualquer tela → menu` (botão "voltar" ou tecla ESC).
- `tutorial`: navegação interna com `tutorial_pg` (0, 1, 2) via setas back/forward.

---

## 3. As funções auxiliares de reinício

```python
reiniciar_posicoes_single(altura, largura, vel_base)
reiniciar_posicoes_multi(altura, largura, vel_base)
reiniciar_jogo_completo(estado_jogo, altura, largura, vel_base)
```

- As duas primeiras só recalculam **posição e velocidade inicial do disco e das raquetes**.
- `reiniciar_jogo_completo` zera o placar (`pontos_p1`, `pontos_p2`, `vencedor`) e **delega** para uma das duas anteriores dependendo do modo — evitando duplicar código (princípio DRY).

Repare a diferença de posição inicial do disco:
- Singleplayer: disco começa em 3/4 da largura, indo para a esquerda (`-vel_base`).
- Multiplayer: disco começa no centro, indo para a direita (`+vel_base`).

**Pergunta provável da banca:** "Por que você não usou uma única função para os dois modos?"
Resposta modelo: porque os modos têm número diferente de raquetes controláveis (single tem só uma raquete ativa) e posições iniciais diferentes; unificar geraria uma função cheia de `if` — separar deixa cada uma simples e legível.

---

## 4. O game loop principal

Estrutura clássica de jogo em tempo real:

```python
while True:
    relogio.tick(FPS)          # limita a taxa de quadros (delta time fixo)
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():   # 1) captura eventos
        ...
    # 2) atualiza física/lógica (dentro do bloco de renderização, por estado)
    # 3) desenha tudo
    pygame.display.update()
```

Pontos-chave para explicar:
- `relogio.tick(FPS)` garante velocidade consistente do jogo independente do hardware.
- Eventos (cliques, teclas) só são **capturados** uma vez por frame no loop `for event in pygame.event.get()`.
- **Movimento contínuo** (segurar uma tecla) não é feito no evento em si: `KEYDOWN` seta uma velocidade (`raq_vel_y = ±velocidade_raquete`) e `KEYUP` zera essa velocidade. A posição real só muda depois, no bloco de física (`raq_y += raq_vel_y`, com clamp). Isso é diferente de tratar cada tecla como um "passo único".

---

## 5. Física e colisões

### Movimento do disco
```python
disco_x += disco_vel_x
disco_y += disco_vel_y
```
Movimento linear simples baseado em velocidade constante por frame.

### Colisão com paredes (topo/base)
```python
if disco_y - disco_raio <= 0 or disco_y + disco_raio >= ALTURA:
    disco_vel_y *= -1
```
Reflexão simples: inverte o sinal da velocidade vertical (ricochete).

### Colisão disco–raquete (círculo-círculo)
```python
if math.hypot(disco_x - raq_x, disco_y - raq_y) <= (disco_raio + raq_raio):
    disco_vel_x = -abs(disco_vel_x)  # ou abs(), dependendo do lado
```
- `math.hypot(dx, dy)` calcula a distância euclidiana entre os centros.
- Regra de colisão círculo-círculo: **colidem se a distância entre centros for ≤ soma dos raios**.
- Em vez de simplesmente inverter o sinal (`*= -1`), usa `abs()`/`-abs()` para **forçar a direção** — evita bug de "disco grudado" trocando de sinal repetidamente enquanto ainda está dentro da raquete.

### Gol / pontuação
```python
if disco_x - disco_raio <= 0:
    if gol_topo <= disco_y <= gol_fundo:
        pontos_p2 += 1
        ... reinicia posições
    else:
        disco_vel_x = abs(disco_vel_x)  # bateu na parede lateral, não no gol
```
O "gol" é uma faixa vertical (`gol_topo` até `gol_fundo`) dentro da borda lateral. Se o disco chega na borda **fora** dessa faixa, é tratado como parede (ricocheteia); se está **dentro**, é gol (pontua e reseta).

### Clamping da raquete
```python
raq_y = max(raq_raio, min(ALTURA - raq_raio, raq_y + raq_vel_y))
```
Padrão de "clamp": garante que a raquete nunca saia da tela, usando `min`/`max` combinados.

---

## 6. Diferenças entre singleplayer e multiplayer

| Aspecto | Singleplayer | Multiplayer |
|---|---|---|
| Raquetes controláveis | Só `raq2` (setas ou W/S) | `raq1` (W/S) e `raq2` (setas) |
| Placar | Só `pontos_p2`, sem `vencedor` verificado | `pontos_p1` e `pontos_p2`, checa `limite_pontos` |
| Tela de vitória | Não existe | Existe (`vencedor`, `vencedor_scr`, botões novo jogo/voltar) |
| Reinício ao golear | Reseta com `reiniciar_posicoes_single` | Reseta com `reiniciar_posicoes_multi` |

**Possível crítica/pergunta da banca:** no singleplayer não há checagem de `limite_pontos` nem tela de "vencedor" — ou seja, tecnicamente o modo solo nunca "termina". Isso é um bom ponto para você comentar como limitação/melhoria futura.

---

## 7. Interface (menu, hover, botões)

- Botões usam `Rect.collidepoint(mouse_pos)` para saber se o mouse está em cima.
- Efeito de hover: troca a imagem exibida (`current_x = hover_img if colide else img_normal`) — não é animação, é **troca de sprite condicional**.
- `criar_botao(...)` (em `draws.py`) parece já encapsular esse padrão para botões de texto (usado na tela de configurações).
- Fundo com scroll infinito:
```python
for i in range(0, tiles):
    tela.blit(fundo, (i * largura_fundo + scroll, 0))
scroll -= 2
if abs(scroll) > largura_fundo:
    scroll = 0
```
Desenha várias cópias lado a lado (`tiles = ceil(LARGURA/largura_fundo)+1`, uma a mais que cabe na tela) e desloca todas para a esquerda a cada frame; quando o deslocamento passa da largura de uma imagem, reseta a 0 — criando ilusão de scroll infinito sem "buracos".

---

## 8. Tela de configurações (`custom`)

- Usa uma `Surface` com canal alfa (`pygame.SRCALPHA`) para desenhar um painel semitransparente por cima do fundo (`painel.fill((25,10,35,230))` — o 4º valor é a opacidade, 0–255).
- Cada opção (música, SFX, cor do disco, limite de pontos) é um "botão-toggle": clicar chama `criar_botao`, que retorna `True` se foi clicado, e aí o estado é alternado.
- `pygame.time.delay(150)` depois de cada toggle — um **debounce simples** para evitar múltiplos toggles no mesmo clique (efeito de clique "grudado" por causa da alta taxa de frames).
- Cor do disco: lista rotativa (`indice_cor_bola = (indice_cor_bola+1) % len(cores_bola)`) — padrão de índice circular.

---

## 9. Pontos de atenção / possíveis perguntas "pegadinha"

1. **`import draws` duplicado** — já existe `from draws import (...)` e depois `import draws` sem uso aparente. Se perguntarem, admita que é redundante/código residual.
2. **Singleplayer sem tela de vitória** — como discutido acima.
3. **`disco_x, disco_y = LARGURA // 2, ALTURA // 2` no início do `main()`** é sobrescrito assim que o jogador entra em qualquer modo (via `reiniciar_jogo_completo`) — ou seja, esses valores iniciais só importam antes do primeiro clique em single/multiplayer.
4. **Por que `math.hypot` e não `(dx**2+dy**2)**0.5`?** — `hypot` é mais legível, evita overflow em casos extremos e é a forma idiomática em Python para distância euclidiana.
5. **Por que resetar posição em vez de só zerar a velocidade ao golear?** — porque senão o disco continuaria vindo do lugar onde saiu, dando vantagem injusta pro próximo lance; resetar ao centro (ou à posição base) garante um "saque" justo.
6. **Onde fica a "IA"?** — Não existe IA no singleplayer! O disco simplesmente ricocheteia nas paredes; o jogador só controla uma raquete contra um rebote de parede/gol. Vale comentar isso se perguntarem sobre "como funciona o oponente".

---

## 10. Roteiro rápido de perguntas & respostas para treinar

**P: Como o jogo sabe em que tela está?**
R: Através da variável de estado `estado_jogo`, verificada tanto no tratamento de eventos quanto na renderização — uma máquina de estados simples baseada em string.

**P: Como funciona a detecção de colisão entre disco e raquete?**
R: Ambos são tratados como círculos; calculo a distância entre os centros com `math.hypot` e comparo com a soma dos raios. Se for menor ou igual, há colisão e eu forço a direção da velocidade horizontal do disco para "empurrá-lo" para longe.

**P: Como o placar é resetado sem duplicar código?**
R: Uma função `reiniciar_jogo_completo` zera o placar e delega o reposicionamento para `reiniciar_posicoes_single` ou `reiniciar_posicoes_multi`, conforme o modo — evitando repetição (DRY).

**P: Por que usar velocidade + clamp em vez de mover a raquete direto pela tecla?**
R: Permite movimento contínuo suave enquanto a tecla está pressionada (`KEYDOWN` define velocidade, `KEYUP` zera) e o `min/max` impede que a raquete saia da área jogável.

**P: O que aconteceria se removesse o `relogio.tick(FPS)`?**
R: O jogo rodaria na velocidade máxima que o hardware permitisse, tornando a física (movimento por frame) dependente do desempenho da máquina — em um PC mais rápido o disco se moveria "mais rápido" percentualmente.

**P: Como funciona o scroll do fundo?**
R: Desenho múltiplas cópias da imagem lado a lado cobrindo a tela, desloco todas para a esquerda a cada frame, e quando o deslocamento acumulado ultrapassa a largura de uma imagem, resето para 0 — criando um loop infinito sem cortes visíveis.

---

## 11. Sugestão de fala para abrir a apresentação

"O projeto é um Air Hockey feito em Pygame, organizado em três módulos: configuração/assets, funções de desenho e a lógica principal do jogo. O núcleo é uma máquina de estados que controla menu, tutorial, configurações e as duas modalidades de jogo. A física usa detecção de colisão círculo-círculo para o disco contra as raquetes, e reflexões simples de velocidade para as paredes e gols."
