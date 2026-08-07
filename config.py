import pygame
import sys

pygame.init()


LARGURA = 960
ALTURA = 540
FPS = 60

COR_FUNDO = (25, 10, 30)
COR_ELEMENTOS = (210, 160, 240)
COR_PONTOS = (65, 30, 80)

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

ROXO_P1 = (220, 100, 255)
LILAS_P2 = (170, 130, 255)
CINZA_ROXO = (140, 120, 160)
ROXO_ESCURO = (45, 20, 60)
VERDE_LILAS = (180, 120, 255)
VERMELHO_ROXO = (150, 40, 90)

fonte_titulo = pygame.font.SysFont(None, 45)
fonte_texto = pygame.font.SysFont(None, 24)
fonte_placar = pygame.font.SysFont(None, 40)

# 4. FUNÇÃO DE CARREGAMENTO DE IMAGEM (gemini)
def carregar_e_escalar(caminho, proporcao=0.5):
    img = pygame.image.load(caminho).convert_alpha()
    novo_tam = (int(img.get_width() * proporcao), int(img.get_height() * proporcao))
    return pygame.transform.scale(img, novo_tam)