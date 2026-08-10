import pygame
from config import (
    BRANCO, COR_FUNDO, COR_ELEMENTOS, COR_PONTOS,
    fonte_texto, LARGURA, ALTURA
)

quit_img = None
quit_btn = None


def desenhar_raquete(tela, x, y, raio_base, cor_principal):
    # testando 3d
    pygame.draw.circle(tela, (15, 5, 20), (int(x) + 3, int(y) + 3), raio_base)
    pygame.draw.circle(tela, cor_principal, (int(x), int(y)), raio_base)

    cor_borda = (max(0, cor_principal[0] - 60), max(0, cor_principal[1] - 60), max(0, cor_principal[2] - 60))
    pygame.draw.circle(tela, cor_borda, (int(x), int(y)), raio_base, 3)

    raio_corpo = int(raio_base * 0.65)
    pygame.draw.circle(tela, cor_borda, (int(x), int(y)), raio_corpo)

    raio_topo = int(raio_base * 0.35)
    cor_topo = (min(255, cor_principal[0] + 40), min(255, cor_principal[1] + 40), min(255, cor_principal[2] + 40))
    pygame.draw.circle(tela, cor_topo, (int(x) - 1, int(y) - 1), raio_topo)

    pygame.draw.circle(tela, BRANCO, (int(x) - int(raio_base * 0.2), int(y) - int(raio_base * 0.2)), int(raio_base * 0.12))

def desenhar_disco(tela, x, y, raio, cor):
    
    pygame.draw.circle(tela, (10, 2, 15), (int(x) + 2, int(y) + 2), raio)
    pygame.draw.circle(tela, cor, (int(x), int(y)), raio)
    pygame.draw.circle(tela, (80, 40, 100), (int(x), int(y)), raio, 2)
    pygame.draw.circle(tela, BRANCO, (int(x) - 3, int(y) - 3), 4)



def desenhar_campo_personalizado(tela, gol_topo, altura_gol, is_singleplayer=False):
    
    tela.fill(COR_FUNDO)

    espacamento = 24
    for x in range(12, LARGURA, espacamento):
        for y in range(12, ALTURA, espacamento):
            pygame.draw.circle(tela, COR_PONTOS, (x, y), 2)

    pygame.draw.line(tela, COR_ELEMENTOS, (LARGURA // 2, 0), (LARGURA // 2, ALTURA), 3)
    pygame.draw.circle(tela, COR_ELEMENTOS, (LARGURA // 2, ALTURA // 2), 60)

    largura_gol = 80

    if is_singleplayer:
        rect_alvo_esq = pygame.Rect(0, gol_topo, 15, altura_gol)
        pygame.draw.rect(tela, COR_ELEMENTOS, rect_alvo_esq, border_radius=5)
        rect_gol_dir = pygame.Rect(LARGURA - largura_gol + 20, gol_topo, largura_gol, altura_gol)
        pygame.draw.rect(tela, COR_ELEMENTOS, rect_gol_dir, border_radius=25)
    else:
        rect_gol_esq = pygame.Rect(-20, gol_topo, largura_gol, altura_gol)
        pygame.draw.rect(tela, COR_ELEMENTOS, rect_gol_esq, border_radius=25)
        rect_gol_dir = pygame.Rect(LARGURA - largura_gol + 20, gol_topo, largura_gol, altura_gol)
        pygame.draw.rect(tela, COR_ELEMENTOS, rect_gol_dir, border_radius=25)

def criar_botao(tela, texto, x, y, largura, altura, cor_normal, cor_hover, pos_mouse):
    
    retangulo = pygame.Rect(x, y, largura, altura)
    clicado = False

    if retangulo.collidepoint(pos_mouse):
        pygame.draw.rect(tela, cor_hover, retangulo, border_radius=6)
        if pygame.mouse.get_pressed()[0]:
            clicado = True
    else:
        pygame.draw.rect(tela, cor_normal, retangulo, border_radius=6)

    pygame.draw.rect(tela, COR_ELEMENTOS, retangulo, 2, border_radius=6)
    texto_surf = fonte_texto.render(texto, True, BRANCO)
    tela.blit(texto_surf, (x + (largura - texto_surf.get_width()) // 2, 
                           y + (altura - texto_surf.get_height()) // 2))

    return clicado