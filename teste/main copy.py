import pygame
import sys
import math
def main():
  
  pygame.init()


  altura_tela = 1080
  largura_tela = 1920
  tela = pygame.display.set_mode((largura_tela,altura_tela))
  clock = pygame.time.Clock()
  FPS = 50

  
  tutorial_img = pygame.image.load('Menu/images/button_tutorial.png').convert_alpha()
  hovert_img = pygame.image.load('Menu/images/button_hover2.png').convert_alpha()
  tutorial_button = tutorial_img.get_rect(center=(1588,85))

  singleplayer_img = pygame.image.load('Menu/images/button_singleplayer.png').convert_alpha()
  singleplayer_button = singleplayer_img.get_rect(center=(912,532))

  multiplayer_img = pygame.image.load('Menu/images/button_multiplayer.png').convert_alpha()
  multiplayer_button = multiplayer_img.get_rect(center=(1038,696))

  customize_img = pygame.image.load('Menu/images/button_customize.png').convert_alpha()
  hover_img = pygame.image.load('Menu/images/button_hover.png').convert_alpha()
  customize_button = customize_img.get_rect(center=(912,863))


  tutorial_0_img = pygame.image.load('Menu/images/tutorial0.png').convert_alpha() 
  tutorial_1_img = pygame.image.load('Menu/images/tutorial1.png').convert_alpha() 
  tutorial_2_img = pygame.image.load('Menu/images/tutorial2.png').convert_alpha() 

  tutorial_0 = tutorial_0_img.get_rect(center=(960,600)) 
  tutorial_1 = tutorial_1_img.get_rect(center=(960,600)) 
  tutorial_2 = tutorial_2_img.get_rect(center=(960,600)) 

  tutorial_imgs = {0: tutorial_0_img, 1: tutorial_1_img, 2: tutorial_2_img} 
  tutorial_coords = {0: tutorial_0, 1: tutorial_1, 2: tutorial_2} 

  tutorial_back_img = pygame.image.load('Menu/images/tutorial_back.png').convert_alpha() 
  tutorial_back = tutorial_back_img.get_rect(center=(505,551)) 

  tutorial_forward_img = pygame.image.load('Menu/images/tutorial_forward.png').convert_alpha() 
  tutorial_forward = tutorial_forward_img.get_rect(center=(1405,551)) 

  quit_img = pygame.image.load('Menu/images/button_quit.png').convert_alpha() 
  quit = quit_img.get_rect(center=(200,1000)) 

  estado_jogo = "menu"
  musica_tocando = False
  tutorial_pg = 0

  fundo = pygame.image.load("Menu/images/main4.png").convert()
  largura_fundo = fundo.get_width()
  rect_fundo = fundo.get_rect()
  scroll = 0
  tiles = math.ceil(largura_tela  / largura_fundo) + 1

  current_tutorial = tutorial_img
  current_custom = customize_img
  current_single = singleplayer_img
  current_multi = multiplayer_img

  jogo = True

  while jogo:

    clock.tick(FPS)

    if estado_jogo == "menu":

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


      if not musica_tocando:
          pygame.mixer.music.load("Menu/k.mp3")
          pygame.mixer.music.play(loops=0)
          musica_tocando = True
    
    if estado_jogo == "tutorial":
      tutorial_page = pygame.image.load('Menu/images/tutorial_background.png').convert_alpha() 
      screen_size = tela.get_size() 
      scaled_image = pygame.transform.scale(tutorial_page, screen_size) 
      tela.blit(scaled_image, (0, 0))

      tutorial_main_img = pygame.image.load('Menu/images/tutorial_main.png').convert_alpha()
      tutorial_main = tutorial_main_img.get_rect(center=(960,560))

      tela.blit(tutorial_main_img, tutorial_main)
      tela.blit(tutorial_back_img, tutorial_back) 
      tela.blit(tutorial_forward_img, tutorial_forward) 
      tela.blit(quit_img, quit)
      tela.blit(tutorial_imgs[tutorial_pg], tutorial_coords[tutorial_pg]) 

      if not musica_tocando:
        pygame.mixer.music.load("Menu/roll.mp3")
        pygame.mixer.music.play(loops=0)
        musica_tocando = True
      
    if estado_jogo == "custom":
        custom_page = pygame.image.load('Menu/images/shrek.png').convert_alpha() 
        screen_size = tela.get_size() 
        scaled_image = pygame.transform.scale(custom_page, screen_size) 
        tela.blit(scaled_image, (0, 0))
        tela.blit(quit_img, quit)
        if not musica_tocando:
          pygame.mixer.music.load("Menu/pain.mp3")
          pygame.mixer.music.play(loops=0)
          musica_tocando = True

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if event.type == pygame.MOUSEBUTTONDOWN: 
        if event.button == 1:
          if tutorial_button.collidepoint(event.pos):
            estado_jogo = "tutorial"
          if customize_button.collidepoint(mouse_pos):
            estado_jogo = "custom"
          if quit.collidepoint(event.pos):
             estado_jogo = "menu"
          if tutorial_back.collidepoint(event.pos): 
            if tutorial_pg > 0: 
              tutorial_pg -= 1 
          if tutorial_forward.collidepoint(event.pos): 
            if tutorial_pg < 2: 
              tutorial_pg += 1 

      if tutorial_button.collidepoint(mouse_pos):
        current_tutorial = hovert_img
      else:
        current_tutorial = tutorial_img
      if customize_button.collidepoint(mouse_pos):
        current_custom = hover_img
      else:
        current_custom = customize_img
    if singleplayer_button.collidepoint(mouse_pos):
        current_single = hover_img
    else:
        current_single = singleplayer_img
    if multiplayer_button.collidepoint(mouse_pos):
        current_multi = hover_img
    else:
        current_multi = multiplayer_img
    

      
    pygame.display.update()

  pygame.quit()

if __name__ == "__main__":
  main()