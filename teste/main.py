import pygame
import sys

# 1. INICIALIZAÇÃO
pygame.init()

LARGURA = 800
ALTURA = 500
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Air Hockey - Jogo Completo")
relogio = pygame.time.Clock()

# 2. CORES
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (230, 50, 50)
AZUL = (50, 100, 230)
CINZA = (180, 180, 180)
CINZA_ESCURO = (50, 50, 50)
VERDE = (40, 180, 80)

# 3. FONTES
fonte_titulo = pygame.font.SysFont(None, 60)
fonte_texto = pygame.font.SysFont(None, 32)
fonte_placar = pygame.font.SysFont(None, 50)

# 4. VARIÁVEIS DO JOGO
# Estado da Tela: "MENU", "JOGO", "CONFIG"
estado = "MENU"

# Configurações padrão
limite_pontos = 5
velocidade_disco_base = 5

# Disco
disco_x = LARGURA // 2
disco_y = ALTURA // 2
disco_raio = 15
disco_vel_x = velocidade_disco_base
disco_vel_y = velocidade_disco_base

# Raquetes
raq1_x, raq1_y = 50, ALTURA // 2
raq2_x, raq2_y = LARGURA - 50, ALTURA // 2
raq_raio = 30
raq1_vel_y = 0
raq2_vel_y = 0
velocidade_raquete = 7

# Placar e Vencedor
pontos_p1 = 0
pontos_p2 = 0
vencedor = ""


# 5. FUNÇÕES AUXILIARES (Para manter a organização sem POO)

def reiniciar_posicoes():
    """Reseta a posição do disco e das raquetes."""
    global disco_x, disco_y, disco_vel_x, disco_vel_y, raq1_y, raq2_y
    disco_x, disco_y = LARGURA // 2, ALTURA // 2
    raq1_y = ALTURA // 2
    raq2_y = ALTURA // 2
    disco_vel_x = velocidade_disco_base if disco_vel_x > 0 else -velocidade_disco_base
    disco_vel_y = velocidade_disco_base

def reiniciar_jogo_completo():
    """Reseta o placar e reinicia a partida."""
    global pontos_p1, pontos_p2, vencedor
    pontos_p1 = 0
    pontos_p2 = 0
    vencedor = ""
    reiniciar_posicoes()

def criar_botao(texto, x, y, largura, altura, cor_normal, cor_hover, pos_mouse):
    """Desenha um botão clicável e retorna True se ele for clicado."""
    retangulo = pygame.Rect(x, y, largura, altura)
    clicado = False

    # Efeito Hover (mudar de cor quando o mouse passa por cima)
    if retangulo.collidepoint(pos_mouse):
        pygame.draw.rect(tela, cor_hover, retangulo, border_radius=10)
        if pygame.mouse.get_pressed()[0]:  # Clique do botão esquerdo
            clicado = True
    else:
        pygame.draw.rect(tela, cor_normal, retangulo, border_radius=10)

    # Desenhar Borda
    pygame.draw.rect(tela, BRANCO, retangulo, 2, border_radius=10)

    # Desenhar Texto no centro do botão
    texto_surf = fonte_texto.render(texto, True, BRANCO)
    tela.blit(texto_surf, (x + (largura - texto_surf.get_width()) // 2, 
                           y + (altura - texto_surf.get_height()) // 2))

    return clicado


# 6. LOOP PRINCIPAL
rodando = True
while rodando:
    pos_mouse = pygame.mouse.get_pos()
    
    # -------------------------------------------------------------
    # A) PROCESSAMENTO DE EVENTOS (TECLADO / FECHAR TELA)
    # -------------------------------------------------------------
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if estado == "JOGO":
            # Pressionar Teclas
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w: raq1_vel_y = -velocidade_raquete
                if evento.key == pygame.K_s: raq1_vel_y = velocidade_raquete
                if evento.key == pygame.K_UP: raq2_vel_y = -velocidade_raquete
                if evento.key == pygame.K_DOWN: raq2_vel_y = velocidade_raquete
                if evento.key == pygame.K_ESCAPE: estado = "MENU"

            # Soltar Teclas
            if evento.type == pygame.KEYUP:
                if evento.key in (pygame.K_w, pygame.K_s): raq1_vel_y = 0
                if evento.key in (pygame.K_UP, pygame.K_DOWN): raq2_vel_y = 0

    # -------------------------------------------------------------
    # B) TELA: MENU PRINCIPAL
    # -------------------------------------------------------------
    if estado == "MENU":
        tela.fill(PRETO)
        
        # Título
        titulo = fonte_titulo.render("AIR HOCKEY", True, BRANCO)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 80))

        # Botões
        if criar_botao("JOGAR", LARGURA // 2 - 100, 200, 200, 50, VERDE, (60, 210, 100), pos_mouse):
            reiniciar_jogo_completo()
            estado = "JOGO"
            pygame.time.delay(150) # Pequeno atraso para evitar cliques duplos

        if criar_botao("CONFIGURAÇÕES", LARGURA // 2 - 100, 270, 200, 50, AZUL, (80, 130, 250), pos_mouse):
            estado = "CONFIG"
            pygame.time.delay(150)

        if criar_botao("SAIR", LARGURA // 2 - 100, 340, 200, 50, VERMELHO, (250, 80, 80), pos_mouse):
            rodando = False

    # -------------------------------------------------------------
    # C) TELA: CONFIGURAÇÕES
    # -------------------------------------------------------------
    elif estado == "CONFIG":
        tela.fill(CINZA_ESCURO)
        
        titulo = fonte_titulo.render("CONFIGURAÇÕES", True, BRANCO)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 60))

        txt_limite = fonte_texto.render(f"Pontos para vencer: {limite_pontos}", True, BRANCO)
        tela.blit(txt_limite, (LARGURA // 2 - txt_limite.get_width() // 2, 180))

        # Botões para alterar o limite de pontos
        if criar_botao("-1 Ponto", LARGURA // 2 - 130, 230, 110, 40, CINZA_ESCURO, CINZA, pos_mouse):
            if limite_pontos > 1:
                limite_pontos -= 1
                pygame.time.delay(150)

        if criar_botao("+1 Ponto", LARGURA // 2 + 20, 230, 110, 40, CINZA_ESCURO, CINZA, pos_mouse):
            limite_pontos += 1
            pygame.time.delay(150)

        # Botão Voltar
        if criar_botao("VOLTAR", LARGURA // 2 - 100, 360, 200, 50, VERMELHO, (250, 80, 80), pos_mouse):
            estado = "MENU"
            pygame.time.delay(150)

    # -------------------------------------------------------------
    # D) TELA: JOGO
    # -------------------------------------------------------------
    elif estado == "JOGO":
        if vencedor == "":
            # --- MOVIMENTAÇÃO E COLISÕES ---
            raq1_y = max(raq_raio, min(ALTURA - raq_raio, raq1_y + raq1_vel_y))
            raq2_y = max(raq_raio, min(ALTURA - raq_raio, raq2_y + raq2_vel_y))

            disco_x += disco_vel_x
            disco_y += disco_vel_y

            # Colisão Bordas Sup/Inf
            if disco_y - disco_raio <= 0 or disco_y + disco_raio >= ALTURA:
                disco_vel_y *= -1

            # Colisão Raquetes (Fórmula de distância entre círculos)
            dist_p1 = ((disco_x - raq1_x)**2 + (disco_y - raq1_y)**2)**0.5
            if dist_p1 <= (disco_raio + raq_raio):
                disco_vel_x = abs(disco_vel_x)

            dist_p2 = ((disco_x - raq2_x)**2 + (disco_y - raq2_y)**2)**0.5
            if dist_p2 <= (disco_raio + raq_raio):
                disco_vel_x = -abs(disco_vel_x)

            # Placar / Pontuação
            if disco_x < 0:
                pontos_p2 += 1
                reiniciar_posicoes()
            elif disco_x > LARGURA:
                pontos_p1 += 1
                reiniciar_posicoes()

            # Checar Fim de Jogo
            if pontos_p1 >= limite_pontos:
                vencedor = "Jogador 1 Venceu!"
            elif pontos_p2 >= limite_pontos:
                vencedor = "Jogador 2 Venceu!"

        # --- DESENHO DA TELA DE JOGO ---
        tela.fill(PRETO)

        # Campo
        pygame.draw.line(tela, CINZA, (LARGURA // 2, 0), (LARGURA // 2, ALTURA), 5)
        pygame.draw.circle(tela, CINZA, (LARGURA // 2, ALTURA // 2), 70, 5)

        # Raquetes e Disco
        pygame.draw.circle(tela, VERMELHO, (int(raq1_x), int(raq1_y)), raq_raio)
        pygame.draw.circle(tela, AZUL, (int(raq2_x), int(raq2_y)), raq_raio)
        pygame.draw.circle(tela, BRANCO, (int(disco_x), int(disco_y)), disco_raio)

        # Placar
        txt_p = fonte_placar.render(f"{pontos_p1}   {pontos_p2}", True, BRANCO)
        tela.blit(txt_p, (LARGURA // 2 - txt_p.get_width() // 2, 20))

        # Tela de Vitória (Fim da partida)
        if vencedor != "":
            txt_venc = fonte_titulo.render(vencedor, True, BRANCO)
            tela.blit(txt_venc, (LARGURA // 2 - txt_venc.get_width() // 2, ALTURA // 2 - 50))
            
            if criar_botao("MENU PRINCIPAL", LARGURA // 2 - 110, ALTURA // 2 + 30, 220, 50, VERDE, (60, 210, 100), pos_mouse):
                estado = "MENU"
                pygame.time.delay(150)

    # -------------------------------------------------------------
    # 7. ATUALIZAÇÃO DA TELA
    # -------------------------------------------------------------
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()