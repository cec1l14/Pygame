"""
O presente código consiste na implementação do jogo de tabuleiro Campo Minado.
Algumas partes do código, rotuladas como TODO, foram omitidas para que sejam 
preenchidas durante a aula prática sobre a biblioteca PyGame.
"""

import pygame
import random

def main():
   pygame.init()

   preto = (0,0,0)
   # vermelho = (255,0,0)
   branco = (255,255,255)
   fonte = pygame.font.SysFont("Comic Sams MS", 30)

   lado_celula = 50
   num_linhas = 4

   # Resolucao = coluna x linha (200 x 250)
   tela = pygame.display.set_mode( (num_linhas * lado_celula, (num_linhas+1) * lado_celula) )
   pygame.display.set_caption( "Campo minado" )

   # Tela inicial
   tela.fill(branco)

   # TODO Desenhar um o tabuleiro de 16 celulas (4 x 4)
   tabuleiro_celulas = [[None]*num_linhas for i in range(num_linhas)]
   

   # Criando o tabuleiro virtual cujos elementos correspondem a um marcador de bomba ('X')
   # ou o numero de bombas ao redor
   conteudo_celula = [[None for j in range(num_linhas)] for i in range(num_linhas)]

   # Marca com 'X' 10% das celulas
   num_bombas = 0
   while (num_bombas < 0.1 * (num_linhas ** 2)):
      i = random.randint(0, num_linhas - 1)
      j = random.randint(0, num_linhas - 1)       
      
      if (conteudo_celula[i][j] == None):
         conteudo_celula[i][j] = "X"
         num_bombas += 1       
            
   # TODO Calcular o numero de bombas ao redor das celulas que nao sao bombas
  
   for i in range(num_linhas):
         for j in range(num_linhas):
            conteudo_celula2 = conteudo_celula
            if conteudo_celula2[i][j] == None:
                  conteudo_celula2[i][j] = 0
            if conteudo_celula [i][j] != 'X':
               if i == 0 and j == 0:
                  if conteudo_celula2 [i+1][j] == "X":
                     conteudo_celula2 [i][j] += 1
                  if conteudo_celula2 [i][j+1] == "X":
                     conteudo_celula2 [i][j] += 1
               if i == 0 and j != 0:
                  if conteudo_celula2 [i+1][j] == "X":
                     conteudo_celula2 [i][j] += 1
                  if conteudo_celula2 [i][j-1] == "X":
                     conteudo_celula2 [i][j] += 1
                  if j !=3:
                     if conteudo_celula2 [i][j+1] == "X":
                        conteudo_celula2 [i][j] += 1
               if (i == 1 or i == 2) and j == 0:
                  if conteudo_celula2 [i-1][j] == "X":
                     conteudo_celula2 [i][j] += 1
                  if conteudo_celula2 [i+1][j] == "X":
                     conteudo_celula2 [i][j] += 1
                  if conteudo_celula2 [i][j+1] == "X":
                     conteudo_celula2 [i][j] += 1
               if (i == 1 or i == 2) and j != 0:
                  if conteudo_celula2 [i-1][j] == "X":
                     conteudo_celula2 [i][j] += 1
                  if conteudo_celula2 [i+1][j] == "X":
                     conteudo_celula2 [i][j] += 1
                  if conteudo_celula2 [i][j-1] == "X":
                     conteudo_celula2 [i][j] += 1
                  if j !=3:
                     if conteudo_celula2 [i][j+1] == "X":
                        conteudo_celula2 [i][j] += 1
               if i == 3 and j == 0:
                  if conteudo_celula2 [i-1][j] == "X":
                     conteudo_celula2 [i][j] += 1
                  if conteudo_celula2 [i][j+1] == "X":
                     conteudo_celula2 [i][j] += 1
               if i == 3 and j != 0:
                  if conteudo_celula2 [i-1][j] == "X":
                     conteudo_celula2 [i][j] += 1
                  if conteudo_celula2 [i][j-1] == "X":
                     conteudo_celula2 [i][j] += 1
                  if j !=3:
                     if conteudo_celula2 [i][j+1] == "X":
                        conteudo_celula2 [i][j] += 1
   for i in conteudo_celula2:
      print(i)

                    
   # Cria uma matriz para controlar a visualizacao do conteudo das celulas
   celula_revelada = [[False for i in range(num_linhas)] for j in range(num_linhas)]

   jogo_cancelado = False
   perdeu = False
   ganhou = False
   num_celulas_abertas = 0

   # Laco do jogo
   while not jogo_cancelado:

      for evento in pygame.event.get(): 
         
         if (evento.type == pygame.QUIT): 
            jogo_cancelado = True
            break
         
         # Se o jogo terminou, as instrucoes abaixo nao sao mais executadas  
         if (perdeu or ganhou):
            continue

         # Tela so' sera' atualizada quando tela_mudou for igual a True 
         tela_mudou = False

         if (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1):
            # Pega as coordenadas do ponto de clique e calcula a celula
            mouse_x, mouse_y = evento.pos
            
            print(f"x = {mouse_x}, y = {mouse_y}")
            
            celula_x = mouse_x // lado_celula
            celula_y = mouse_y // lado_celula

                   # Clicou fora do tabuleiro
            if (celula_y > num_linhas-1):
               continue # segue para o proximo evento

            # Entra no if se a celula foi clicada pela primeira vez
            if (not celula_revelada[celula_x][celula_y]):
               tela_mudou = True
               num_celulas_abertas += 1
               celula_revelada[celula_x][celula_y] = True
               
               # Verifica se perdeu
               if (conteudo_celula[celula_x][celula_y] == "X"):
                  pygame.mixer.music.load('explosion.ogg')
                  pygame.mixer.music.play(1)
                  perdeu = True                             
               # Verifica se ganhou   
               elif (num_celulas_abertas + num_bombas == num_linhas**2):                  
                  pygame.mixer.music.load('applause.ogg')
                  pygame.mixer.music.play(1)
                  ganhou = True

         # Atualiza a tela
         if (tela_mudou):
            i, j = celula_x, celula_y
            
            if (conteudo_celula[i][j] == "X"):
               bomba = pygame.image.load('bomba.jpeg')
               
               # Redimensiona a imagem
               bomba = pygame.transform.scale(bomba, (lado_celula - 2, lado_celula - 2))            
               
               # Rotaciona a imagem
               bomba = pygame.transform.rotate(bomba, 90)
               
               # Posiciona a imagem em uma superficie
               tela.blit(bomba, (lado_celula*i + 1, lado_celula*j + 1))
            else:
               texto = fonte.render(conteudo_celula[i][j], True, preto)            
               tela.blit(texto, (lado_celula*i + 0.4*lado_celula, lado_celula*j + 0.4*lado_celula) )

            if (ganhou):            
               texto = fonte.render("Ganhou!", True, preto)
               
               tela.blit(texto, (0, lado_celula*num_linhas))            
            elif (perdeu):             
               texto = fonte.render("Perdeu!", True, preto)
               
               tela.blit(texto, (0, lado_celula*num_linhas))

            pygame.display.update()
   pygame.quit()

if __name__ == "__main__":
    main()
