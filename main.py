import pygame

pygame.init()
BRANCO = (255,255,255)

janela = pygame.display.set_mode((1024, 600))
janela.fill(BRANCO)
pygame.display.set_caption('Air Hockey')

# button configuration



continuar = True

while continuar:
 for event in pygame.event.get():
    if event.type == pygame.QUIT:
        continuar = False

    pygame.display.update()

pygame.quit()
