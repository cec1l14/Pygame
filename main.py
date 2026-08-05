import pygame
import sys
import math

from config import (
    LARGURA, ALTURA, FPS, COR_ELEMENTOS, BRANCO, CINZA_ROXO,
    ROXO_ESCURO, VERDE_LILAS, VERMELHO_ROXO, ROXO_P1, LILAS_P2,
    fonte_titulo, fonte_texto, fonte_placar, carregar_e_escalar
)
from draws import (
    desenhar_raquete, desenhar_disco, desenhar_botao_sair,
    desenhar_campo_personalizado, criar_botao, carregar_assets_draws
)
import draws

def main():
    pygame.init()
    pygame.mixer.init()


    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Air Hockey - Roxo & Lilás")
    relogio = pygame.time.Clock()

    
    carregar_assets_draws()

    # codigo de teteus
    
    tutorial_img = carregar_e_escalar('images/button_tutorial.png')
    hovert_img = carregar_e_escalar('images/button_hover2.png')
    tutorial_button = tutorial_img.get_rect(center=(900, 42))

    singleplayer_img = carregar_e_escalar('images/button_singleplayer.png')
    singleplayer_button = singleplayer_img.get_rect(center=(456, 266))

    multiplayer_img = carregar_e_escalar('images/button_multiplayer.png')
    multiplayer_button = multiplayer_img.get_rect(center=(519, 348))

    customize_img = carregar_e_escalar('images/button_customize.png')
    hover_img = carregar_e_escalar('images/button_hover.png')
    customize_button = customize_img.get_rect(center=(456, 431))

    tutorial_0_img = carregar_e_escalar('images/tutorial0.png')
    tutorial_1_img = carregar_e_escalar('images/tutorial1.png')
    tutorial_2_img = carregar_e_escalar('images/tutorial2.png')

    tutorial_imgs = {0: tutorial_0_img, 1: tutorial_1_img, 2: tutorial_2_img}
    tutorial_coords = {
        0: tutorial_0_img.get_rect(center=(480, 300)),
        1: tutorial_1_img.get_rect(center=(480, 300)),
        2: tutorial_2_img.get_rect(center=(480, 300))
    }

    tutorial_back_img = carregar_e_escalar('images/tutorial_back.png')
    tutorial_back = tutorial_back_img.get_rect(center=(252, 275))

    tutorial_forward_img = carregar_e_escalar('images/tutorial_forward.png')
    tutorial_forward = tutorial_forward_img.get_rect(center=(702, 275))

    fundo = pygame.image.load("images/main4.png").convert()
    fundo = pygame.transform.scale(fundo, (int(fundo.get_width() * 0.5), ALTURA))
    largura_fundo = fundo.get_width()
    scroll = 0
    tiles = math.ceil(LARGURA / largura_fundo) + 1

    
    musica_ativa = True
    sfx_ativo = True
    cores_bola = [COR_ELEMENTOS, BRANCO, (240, 190, 255), (190, 90, 240)]
    nomes_cores_bola = ["LILÁS", "BRANCO", "ORQUÍDEA", "ROXO NEON"]
    indice_cor_bola = 0
    cor_disco_atual = cores_bola[indice_cor_bola]
    limite_pontos = 5

    
    velocidade_disco_base = 7.0
    disco_x, disco_y = LARGURA // 2, ALTURA // 2
    disco_raio = 20
    disco_vel_x, disco_vel_y = -velocidade_disco_base, velocidade_disco_base

    raq1_x, raq1_y = 60, ALTURA // 2
    raq2_x, raq2_y = LARGURA - 60, ALTURA // 2
    raq_raio = 35
    raq1_vel_y, raq2_vel_y = 0, 0
    velocidade_raquete = 8

    altura_gol = 220
    gol_topo = (ALTURA // 2) - (altura_gol // 2)
    gol_fundo = (ALTURA // 2) + (altura_gol // 2)

    pontos_p1, pontos_p2 = 0, 0
    vencedor = ""
    estado_jogo = "menu"
    tutorial_pg = 0

    def reiniciar_posicoes_single():
        nonlocal disco_x, disco_y, disco_vel_x, disco_vel_y, raq2_y
        disco_x, disco_y = (LARGURA // 4) * 3, ALTURA // 2
        raq2_y = ALTURA // 2
        disco_vel_x, disco_vel_y = -velocidade_disco_base, velocidade_disco_base

    def reiniciar_posicoes_multi():
        nonlocal disco_x, disco_y, disco_vel_x, disco_vel_y, raq1_y, raq2_y
        disco_x, disco_y = LARGURA // 2, ALTURA // 2
        raq1_y, raq2_y = ALTURA // 2, ALTURA // 2
        disco_vel_x, disco_vel_y = velocidade_disco_base, velocidade_disco_base

    def reiniciar_jogo_completo():
        nonlocal pontos_p1, pontos_p2, vencedor
        pontos_p1, pontos_p2 = 0, 0
        vencedor = ""
        if estado_jogo == "singleplayer":
            reiniciar_posicoes_single()
        else:
            reiniciar_posicoes_multi()

    # CORAÇÃO DO JOGO
    while True:
        relogio.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if estado_jogo == "menu":
                    if tutorial_button.collidepoint(event.pos): estado_jogo = "tutorial"
                    elif customize_button.collidepoint(event.pos): estado_jogo = "custom"
                    elif singleplayer_button.collidepoint(event.pos):
                        estado_jogo = "singleplayer"
                        reiniciar_jogo_completo()
                    elif multiplayer_button.collidepoint(event.pos):
                        estado_jogo = "multiplayer"
                        reiniciar_jogo_completo()

                elif estado_jogo in ("tutorial", "custom", "singleplayer", "multiplayer"):
                    if draws.quit_btn.collidepoint(event.pos):
                        estado_jogo = "menu"

                if estado_jogo == "tutorial":
                    if tutorial_back.collidepoint(event.pos) and tutorial_pg > 0: tutorial_pg -= 1
                    if tutorial_forward.collidepoint(event.pos) and tutorial_pg < 2: tutorial_pg += 1

            if estado_jogo in ("singleplayer", "multiplayer"):
                if event.type == pygame.KEYDOWN:
                    if estado_jogo == "singleplayer":
                        if event.key in (pygame.K_UP, pygame.K_w): raq2_vel_y = -velocidade_raquete
                        if event.key in (pygame.K_DOWN, pygame.K_s): raq2_vel_y = velocidade_raquete
                    elif estado_jogo == "multiplayer":
                        if event.key == pygame.K_w: raq1_vel_y = -velocidade_raquete
                        if event.key == pygame.K_s: raq1_vel_y = velocidade_raquete
                        if event.key == pygame.K_UP: raq2_vel_y = -velocidade_raquete
                        if event.key == pygame.K_DOWN: raq2_vel_y = velocidade_raquete
                    if event.key == pygame.K_ESCAPE: estado_jogo = "menu"

                if event.type == pygame.KEYUP:
                    if estado_jogo == "singleplayer":
                        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s): raq2_vel_y = 0
                    elif estado_jogo == "multiplayer":
                        if event.key in (pygame.K_w, pygame.K_s): raq1_vel_y = 0
                        if event.key in (pygame.K_UP, pygame.K_DOWN): raq2_vel_y = 0

        # TELAS
        if estado_jogo == "menu":
            current_tutorial = hovert_img if tutorial_button.collidepoint(mouse_pos) else tutorial_img
            current_custom = hover_img if customize_button.collidepoint(mouse_pos) else customize_img
            current_single = hover_img if singleplayer_button.collidepoint(mouse_pos) else singleplayer_img
            current_multi = hover_img if multiplayer_button.collidepoint(mouse_pos) else multiplayer_img

            for i in range(0, tiles):
                tela.blit(fundo, (i * largura_fundo + scroll, 0))

            scroll -= 2
            if abs(scroll) > largura_fundo: scroll = 0

            tela.blit(current_single, singleplayer_button)
            tela.blit(current_tutorial, tutorial_button)
            tela.blit(current_custom, customize_button)
            tela.blit(current_multi, multiplayer_button)

        elif estado_jogo == "tutorial":
            tutorial_page = carregar_e_escalar('images/tutorial_background.png', 1.0)
            tela.blit(pygame.transform.scale(tutorial_page, (LARGURA, ALTURA)), (0, 0))

            tutorial_main_img = carregar_e_escalar('images/tutorial_main.png')
            tela.blit(tutorial_main_img, tutorial_main_img.get_rect(center=(480, 280)))
            tela.blit(tutorial_back_img, tutorial_back) 
            tela.blit(tutorial_forward_img, tutorial_forward) 
            desenhar_botao_sair(tela)
            tela.blit(tutorial_imgs[tutorial_pg], tutorial_coords[tutorial_pg])

        elif estado_jogo == "custom":
            for i in range(0, tiles): tela.blit(fundo, (i * largura_fundo + scroll, 0))

            painel = pygame.Surface((600, 380), pygame.SRCALPHA)
            painel.fill((25, 10, 35, 230))
            tela.blit(painel, (LARGURA // 2 - 300, 60))
            pygame.draw.rect(tela, COR_ELEMENTOS, (LARGURA // 2 - 300, 60, 600, 380), 2, border_radius=12)

            txt_titulo = fonte_titulo.render("CONFIGURAÇÕES", True, COR_ELEMENTOS)
            tela.blit(txt_titulo, (LARGURA // 2 - txt_titulo.get_width() // 2, 80))

            
            tela.blit(fonte_texto.render("Música de Fundo", True, CINZA_ROXO), (LARGURA // 2 - 240, 150))
            st_m = "LIGADO" if musica_ativa else "DESLIGADO"
            if criar_botao(tela, st_m, LARGURA // 2 + 100, 142, 130, 32, VERDE_LILAS if musica_ativa else VERMELHO_ROXO, CINZA_ROXO, mouse_pos):
                musica_ativa = not musica_ativa
                if not musica_ativa: pygame.mixer.music.stop()
                pygame.time.delay(150)

            tela.blit(fonte_texto.render("Efeitos Sonoros", True, CINZA_ROXO), (LARGURA // 2 - 240, 210))
            st_s = "LIGADO" if sfx_ativo else "DESLIGADO"
            if criar_botao(tela, st_s, LARGURA // 2 + 100, 202, 130, 32, VERDE_LILAS if sfx_ativo else VERMELHO_ROXO, CINZA_ROXO, mouse_pos):
                sfx_ativo = not sfx_ativo
                pygame.time.delay(150)

            tela.blit(fonte_texto.render("Cor do Disco", True, CINZA_ROXO), (LARGURA // 2 - 240, 270))
            desenhar_disco(tela, LARGURA // 2 + 70, 278, 12, cor_disco_atual)
            if criar_botao(tela, nomes_cores_bola[indice_cor_bola], LARGURA // 2 + 100, 262, 130, 32, ROXO_ESCURO, CINZA_ROXO, mouse_pos):
                indice_cor_bola = (indice_cor_bola + 1) % len(cores_bola)
                cor_disco_atual = cores_bola[indice_cor_bola]
                pygame.time.delay(150)

            tela.blit(fonte_texto.render("Limite de Pontos", True, CINZA_ROXO), (LARGURA // 2 - 240, 330))
            if criar_botao(tela, "-", LARGURA // 2 + 100, 322, 35, 32, ROXO_ESCURO, CINZA_ROXO, mouse_pos):
                if limite_pontos > 1: limite_pontos -= 1; pygame.time.delay(150)
            
            txt_pts = fonte_texto.render(str(limite_pontos), True, BRANCO)
            tela.blit(txt_pts, (LARGURA // 2 + 152 - txt_pts.get_width() // 2, 330))

            if criar_botao(tela, "+", LARGURA // 2 + 170, 322, 35, 32, ROXO_ESCURO, CINZA_ROXO, mouse_pos):
                limite_pontos += 1; pygame.time.delay(150)

            desenhar_botao_sair(tela)

        elif estado_jogo == "singleplayer":
            raq2_y = max(raq_raio, min(ALTURA - raq_raio, raq2_y + raq2_vel_y))
            disco_x += disco_vel_x
            disco_y += disco_vel_y

            if disco_y - disco_raio <= 0 or disco_y + disco_raio >= ALTURA: disco_vel_y *= -1

            if disco_x - disco_raio <= 15:
                if gol_topo <= disco_y <= gol_fundo:
                    pontos_p2 += 1
                disco_vel_x = abs(disco_vel_x)

            if math.hypot(disco_x - raq2_x, disco_y - raq2_y) <= (disco_raio + raq_raio):
                disco_vel_x = -abs(disco_vel_x)

            if disco_x > LARGURA + disco_raio: reiniciar_posicoes_single()

            desenhar_campo_personalizado(tela, gol_topo, altura_gol, is_singleplayer=True)
            desenhar_raquete(tela, raq2_x, raq2_y, raq_raio, LILAS_P2)
            desenhar_disco(tela, disco_x, disco_y, disco_raio, cor_disco_atual)

            txt_p = fonte_placar.render(f"Pontos: {pontos_p2}", True, COR_ELEMENTOS)
            tela.blit(txt_p, (LARGURA // 2 - txt_p.get_width() // 2, 15))
            desenhar_botao_sair(tela)

        elif estado_jogo == "multiplayer":
            if vencedor == "":
                raq1_y = max(raq_raio, min(ALTURA - raq_raio, raq1_y + raq1_vel_y))
                raq2_y = max(raq_raio, min(ALTURA - raq_raio, raq2_y + raq2_vel_y))

                disco_x += disco_vel_x
                disco_y += disco_vel_y

                if disco_y - disco_raio <= 0 or disco_y + disco_raio >= ALTURA: disco_vel_y *= -1

                if math.hypot(disco_x - raq1_x, disco_y - raq1_y) <= (disco_raio + raq_raio): disco_vel_x = abs(disco_vel_x)
                if math.hypot(disco_x - raq2_x, disco_y - raq2_y) <= (disco_raio + raq_raio): disco_vel_x = -abs(disco_vel_x)

                if disco_x - disco_raio <= 0:
                    if gol_topo <= disco_y <= gol_fundo: pontos_p2 += 1; reiniciar_posicoes_multi()
                    else: disco_vel_x = abs(disco_vel_x)

                if disco_x + disco_raio >= LARGURA:
                    if gol_topo <= disco_y <= gol_fundo: pontos_p1 += 1; reiniciar_posicoes_multi()
                    else: disco_vel_x = -abs(disco_vel_x)

                if pontos_p1 >= limite_pontos: vencedor = "Jogador 1 Venceu!"
                elif pontos_p2 >= limite_pontos: vencedor = "Jogador 2 Venceu!"

            desenhar_campo_personalizado(tela, gol_topo, altura_gol, is_singleplayer=False)
            desenhar_raquete(tela, raq1_x, raq1_y, raq_raio, ROXO_P1)
            desenhar_raquete(tela, raq2_x, raq2_y, raq_raio, LILAS_P2)
            desenhar_disco(tela, disco_x, disco_y, disco_raio, cor_disco_atual)

            txt_p = fonte_placar.render(f"{pontos_p1}   {pontos_p2}", True, COR_ELEMENTOS)
            tela.blit(txt_p, (LARGURA // 2 - txt_p.get_width() // 2, 15))
            desenhar_botao_sair(tela)

            if vencedor != "":
                txt_venc = fonte_titulo.render(vencedor, True, COR_ELEMENTOS)
                tela.blit(txt_venc, (LARGURA // 2 - txt_venc.get_width() // 2, ALTURA // 2 - 30))

        pygame.display.update()

if __name__ == "__main__":
    main()