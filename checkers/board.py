import pygame
from .constants import CAFE, MARRON, ROWS, SQUARE_SIZE
class Board:
    def __init__(self):
        self.board = []
        self.selected_pice = None
        #Tenemos 12 piezas blancas y 12 piezas rojas
        self.red_left = self.white_left = 12
        #Tenemos 0 reyes blancos y 0 reyes rojos
        self.red_kings = self.white_kings = 0
    
    def draw_squares(self, win):
        win.fill(CAFE)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, MARRON, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        pass