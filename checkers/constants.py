import pygame

#Tamanho del tablero
WIDTH, HEIGHT = 680, 680

#Tamaño de las casillas
ROWS, COLS = 8, 8

#Tamaño de las piezas
SQUARE_SIZE = WIDTH // COLS

#Colores
MARRON = (94,56,18)   # RGB
CAFE = (241, 190, 72)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (44, 25))
GREEN = (0, 255, 0)