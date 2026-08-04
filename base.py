import pygame
import sys
import math

def main():
    # 1. INICIALIZAÇÃO
    pygame.init()

    # Resolução 960x540
    LARGURA = 960
    ALTURA = 540
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Air Hockey com Menu")
    relogio = pygame.time.Clock()
    FPS = 60

    # 2. CORES E FONTES
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    VERMELHO = (230, 50, 50)
    AZUL = (50, 100, 230)
    CINZA = (180, 180, 180)
    VERDE = (40, 180, 80)

    fonte_titulo = pygame.font.SysFont(None, 45)
    fonte_texto = pygame.font.SysFont(None, 24)
    fonte_placar = pygame.font.SysFont(None, 35)

    def carregar_e_escalar(caminho, proporcao=0.5):
        img = pygame.image.load(caminho).convert_alpha()
        novo_tam = (int(img.get_width() * proporcao), int(img.get_height() * proporcao))
        return pygame.transform.scale(img, novo_tam)

    # 3. IMAGENS E BOTÕES DE MENU
    tutorial_img = carregar_e_escalar('Pygame/teste/images/button_tutorial.png')
    hovert_img = carregar_e_escalar('Pygame/teste/images/button_hover2.png')
    tutorial_button = tutorial_img.get_rect(center=(794, 42))

    singleplayer_img = carregar_e_escalar('Pygame/teste/images/button_singleplayer.png')
    singleplayer_button = singleplayer_img.get_rect(center=(456, 266))

    multiplayer_img = carregar_e_escalar('Pygame/teste/images/button_multiplayer.png')
    multiplayer_button = multiplayer_img.get_rect(center=(519, 348))

    customize_img = carregar_e_escalar('Pygame/teste/images/button_customize.png')
    hover_img = carregar_e_escalar('Pygame/teste/images/button_hover.png')
    customize_button = customize_img.get_rect(center=(456, 431))

    tutorial_0_img = carregar_e_escalar('Pygame/teste/images/tutorial0.png')
    tutorial_1_img = carregar_e_escalar('Pygame/teste/images/tutorial1.png')
    tutorial_2_img = carregar_e_escalar('Pygame/teste/images/tutorial2.png')

    tutorial_0 = tutorial_0_img.get_rect(center=(480, 300))
    tutorial_1 = tutorial_1_img.get_rect(center=(480, 300))
    tutorial_2 = tutorial_2_img.get_rect(center=(480, 300))

    tutorial_imgs = {0: tutorial_0_img, 1: tutorial_1_img, 2: tutorial_2_img} 
    tutorial_coords = {0: tutorial_0, 1: tutorial_1, 2: tutorial_2} 

    tutorial_back_img = carregar_e_escalar('Pygame/teste/images/tutorial_back.png')
    tutorial_back = tutorial_back_img.get_rect(center=(252, 275))

    tutorial_forward_img = carregar_e_escalar('Pygame/teste/images/tutorial_forward.png')
    tutorial_forward = tutorial_forward_img.get_rect(center=(702, 275))

    # Botão Sair no canto inferior esquerdo
    quit_img = carregar_e_escalar('Pygame/teste/images/button_quit.png')
    quit_btn = quit_img.get_rect(bottomleft=(20, ALTURA - 20))

    fundo = pygame.image.load("Pygame/teste/images/main4.png").convert()
    fundo = pygame.transform.scale(fundo, (int(fundo.get_width() * 0.5), ALTURA))
    largura_fundo = fundo.get_width()
    rect_fundo = fundo.get_rect()
    scroll = 0
    tiles = math.ceil(LARGURA / largura_fundo) + 1

    current_tutorial = tutorial_img
    current_custom = customize_img
    current_single = singleplayer_img
    current_multi = multiplayer_img

    # 4. VARIÁVEIS DE JOGO E FÍSICA
    limite_pontos = 5
    velocidade_disco_base = 5.0

    disco_x = LARGURA // 2
    disco_y = ALTURA // 2
    disco_raio = 12
    disco_vel_x = -velocidade_disco_base
    disco_vel_y = velocidade_disco_base

    raq1_x, raq1_y = 50, ALTURA // 2
    raq2_x, raq2_y = LARGURA - 50, ALTURA // 2
    raq_raio = 22
    raq1_vel_y = 0
    raq2_vel_y = 0
    velocidade_raquete = 6

    pontos_p1 = 0
    pontos_p2 = 0
    vencedor = ""

    # Estados do jogo: "menu", "tutorial", "custom", "singleplayer", "multiplayer"
    estado_jogo = "menu"
    tutorial_pg = 0

    def reiniciar_posicoes_single():
        nonlocal disco_x, disco_y, disco_vel_x, disco_vel_y, raq2_y
        disco_x = (LARGURA // 4) * 3
        disco_y = ALTURA // 2
        raq2_y = ALTURA // 2
        disco_vel_x = -velocidade_disco_base
        disco_vel_y = velocidade_disco_base

    def reiniciar_posicoes_multi():
        nonlocal disco_x, disco_y, disco_vel_x, disco_vel_y, raq1_y, raq2_y
        disco_x = LARGURA // 2
        disco_y = ALTURA // 2
        raq1_y = ALTURA // 2
        raq2_y = ALTURA // 2
        disco_vel_x = velocidade_disco_base
        disco_vel_y = velocidade_disco_base

    def reiniciar_jogo_completo():
        nonlocal pontos_p1, pontos_p2, vencedor
        pontos_p1 = 0
        pontos_p2 = 0
        vencedor = ""
        if estado_jogo == "singleplayer":
            reiniciar_posicoes_single()
        else:
            reiniciar_posicoes_multi()

    # 5. LOOP PRINCIPAL
    while True:
        relogio.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        # PROCESSAMENTO DE EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # CLIQUES NO MENU
                if estado_jogo == "menu":
                    if tutorial_button.collidepoint(event.pos):
                        estado_jogo = "tutorial"
                    elif customize_button.collidepoint(event.pos):
                        estado_jogo = "custom"
                    elif singleplayer_button.collidepoint(event.pos):
                        estado_jogo = "singleplayer"
                        reiniciar_jogo_completo()
                    elif multiplayer_button.collidepoint(event.pos):
                        estado_jogo = "multiplayer"
                        reiniciar_jogo_completo()

                # CLIQUES NO BOTÃO SAIR
                elif estado_jogo in ("tutorial", "custom", "singleplayer", "multiplayer"):
                    if quit_btn.collidepoint(event.pos):
                        estado_jogo = "menu"

                # NAVEGAÇÃO DO TUTORIAL
                if estado_jogo == "tutorial":
                    if tutorial_back.collidepoint(event.pos) and tutorial_pg > 0:
                        tutorial_pg -= 1
                    if tutorial_forward.collidepoint(event.pos) and tutorial_pg < 2:
                        tutorial_pg += 1

            # CONTROLES DE MOVIMENTO DAS RAQUETES
            if estado_jogo in ("singleplayer", "multiplayer"):
                if event.type == pygame.KEYDOWN:
                    # No Singleplayer, o jogador usa as setas ou W/S para mover a raquete do LADO DIREITO
                    if estado_jogo == "singleplayer":
                        if event.key in (pygame.K_UP, pygame.K_w): raq2_vel_y = -velocidade_raquete
                        if event.key in (pygame.K_DOWN, pygame.K_s): raq2_vel_y = velocidade_raquete

                    # No Multiplayer: Player 1 (W/S) e Player 2 (Setas)
                    elif estado_jogo == "multiplayer":
                        if event.key == pygame.K_w: raq1_vel_y = -velocidade_raquete
                        if event.key == pygame.K_s: raq1_vel_y = velocidade_raquete
                        if event.key == pygame.K_UP: raq2_vel_y = -velocidade_raquete
                        if event.key == pygame.K_DOWN: raq2_vel_y = velocidade_raquete

                    if event.key == pygame.K_ESCAPE:
                        estado_jogo = "menu"

                if event.type == pygame.KEYUP:
                    if estado_jogo == "singleplayer":
                        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s): 
                            raq2_vel_y = 0
                    elif estado_jogo == "multiplayer":
                        if event.key in (pygame.K_w, pygame.K_s): raq1_vel_y = 0
                        if event.key in (pygame.K_UP, pygame.K_DOWN): raq2_vel_y = 0

        # TELA: MENU PRINCIPAL
        if estado_jogo == "menu":
            current_tutorial = hovert_img if tutorial_button.collidepoint(mouse_pos) else tutorial_img
            current_custom = hover_img if customize_button.collidepoint(mouse_pos) else customize_img
            current_single = hover_img if singleplayer_button.collidepoint(mouse_pos) else singleplayer_img
            current_multi = hover_img if multiplayer_button.collidepoint(mouse_pos) else multiplayer_img

            for i in range(0, tiles):
                tela.blit(fundo, (i * largura_fundo + scroll, 0))
                rect_fundo.x = i * largura_fundo + scroll

            scroll -= 2
            if abs(scroll) > largura_fundo:
                scroll = 0

            tela.blit(current_single, singleplayer_button)
            tela.blit(current_tutorial, tutorial_button)
            tela.blit(current_custom, customize_button)
            tela.blit(current_multi, multiplayer_button)

        # TELA: TUTORIAL
        elif estado_jogo == "tutorial":
            tutorial_page = pygame.image.load('Pygame/teste/images/tutorial_background.png').convert_alpha() 
            scaled_image = pygame.transform.scale(tutorial_page, (LARGURA, ALTURA)) 
            tela.blit(scaled_image, (0, 0))

            tutorial_main_img = carregar_e_escalar('Pygame/teste/images/tutorial_main.png')
            tutorial_main = tutorial_main_img.get_rect(center=(480, 280))

            tela.blit(tutorial_main_img, tutorial_main)
            tela.blit(tutorial_back_img, tutorial_back) 
            tela.blit(tutorial_forward_img, tutorial_forward) 
            tela.blit(quit_img, quit_btn)
            tela.blit(tutorial_imgs[tutorial_pg], tutorial_coords[tutorial_pg])

        # TELA: CUSTOMIZAÇÃO
        elif estado_jogo == "custom":
            custom_page = pygame.image.load('Pygame/teste/images/shrek.png').convert_alpha() 
            scaled_image = pygame.transform.scale(custom_page, (LARGURA, ALTURA)) 
            tela.blit(scaled_image, (0, 0))
            tela.blit(quit_img, quit_btn)

        # MODO SINGLEPLAYER (JOGADOR NO LADO DIREITO)
        elif estado_jogo == "singleplayer":
            # Movimentação Raquete Jogador (Direita)
            raq2_y = max(raq_raio, min(ALTURA - raq_raio, raq2_y + raq2_vel_y))

            # Movimentação Disco
            disco_x += disco_vel_x
            disco_y += disco_vel_y

            # Colisão Bordas Superior / Inferior
            if disco_y - disco_raio <= 0 or disco_y + disco_raio >= ALTURA:
                disco_vel_y *= -1

            # Colisão com a Parede Esquerda (O disco rebate de volta)
            if disco_x - disco_raio <= 0:
                disco_vel_x = abs(disco_vel_x)
                pontos_p2 += 1  # Pontuação do jogador da direita

            # Colisão Raquete do Jogador (Lado Direito)
            dist_p2 = math.hypot(disco_x - raq2_x, disco_y - raq2_y)
            if dist_p2 <= (disco_raio + raq_raio):
                disco_vel_x = -abs(disco_vel_x)

            # Caso o disco passe do jogador na direita, reinicia
            if disco_x > LARGURA:
                reiniciar_posicoes_single()

            # Desenhar Campo Singleplayer
            tela.fill(PRETO)
            pygame.draw.line(tela, CINZA, (5, 0), (5, ALTURA), 10) # Parede alvo na esquerda

            # Raquete Azul (Direita) e Disco
            pygame.draw.circle(tela, AZUL, (int(raq2_x), int(raq2_y)), raq_raio)
            pygame.draw.circle(tela, BRANCO, (int(disco_x), int(disco_y)), disco_raio)

            # Placar de Pontos
            txt_p = fonte_placar.render(f"Pontos: {pontos_p2}", True, BRANCO)
            tela.blit(txt_p, (LARGURA // 2 - txt_p.get_width() // 2, 15))

            # Botão de Sair no Canto Inferior Esquerdo
            tela.blit(quit_img, quit_btn)

        # MODO MULTIPLAYER
        elif estado_jogo == "multiplayer":
            if vencedor == "":
                raq1_y = max(raq_raio, min(ALTURA - raq_raio, raq1_y + raq1_vel_y))
                raq2_y = max(raq_raio, min(ALTURA - raq_raio, raq2_y + raq2_vel_y))

                disco_x += disco_vel_x
                disco_y += disco_vel_y

                if disco_y - disco_raio <= 0 or disco_y + disco_raio >= ALTURA:
                    disco_vel_y *= -1

                dist_p1 = math.hypot(disco_x - raq1_x, disco_y - raq1_y)
                if dist_p1 <= (disco_raio + raq_raio):
                    disco_vel_x = abs(disco_vel_x)

                dist_p2 = math.hypot(disco_x - raq2_x, disco_y - raq2_y)
                if dist_p2 <= (disco_raio + raq_raio):
                    disco_vel_x = -abs(disco_vel_x)

                if disco_x < 0:
                    pontos_p2 += 1
                    reiniciar_posicoes_multi()
                elif disco_x > LARGURA:
                    pontos_p1 += 1
                    reiniciar_posicoes_multi()

                if pontos_p1 >= limite_pontos:
                    vencedor = "Jogador 1 Venceu!"
                elif pontos_p2 >= limite_pontos:
                    vencedor = "Jogador 2 Venceu!"

            tela.fill(PRETO)
            pygame.draw.line(tela, CINZA, (LARGURA // 2, 0), (LARGURA // 2, ALTURA), 2)
            pygame.draw.circle(tela, CINZA, (LARGURA // 2, ALTURA // 2), 50, 2)

            pygame.draw.circle(tela, VERMELHO, (int(raq1_x), int(raq1_y)), raq_raio)
            pygame.draw.circle(tela, AZUL, (int(raq2_x), int(raq2_y)), raq_raio)
            pygame.draw.circle(tela, BRANCO, (int(disco_x), int(disco_y)), disco_raio)

            txt_p = fonte_placar.render(f"{pontos_p1}   {pontos_p2}", True, BRANCO)
            tela.blit(txt_p, (LARGURA // 2 - txt_p.get_width() // 2, 15))

            # Botão de Sair no Canto Inferior Esquerdo
            tela.blit(quit_img, quit_btn)

            if vencedor != "":
                txt_venc = fonte_titulo.render(vencedor, True, BRANCO)
                tela.blit(txt_venc, (LARGURA // 2 - txt_venc.get_width() // 2, ALTURA // 2 - 30))

        pygame.display.update()

if __name__ == "__main__":
    main()