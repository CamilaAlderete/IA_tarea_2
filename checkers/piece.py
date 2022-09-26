import pygame
from .constants import SQUARE_SIZE, GREY, CROWN, BLACK

class Piece:
    #Para el tamanho de las piezas 
    PADDING = 10
    OUTLINE = 3

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        #Si es el rey puede pasar sobre las piezas enemigas e ir mas lejos
        self.king = False

        if self.color == BLACK:
            self.direction = -1
        else:
            self.direction = 1

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE//2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE//2

    def make_king(self):
        self.king = True
    
    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING         
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)

        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            # Poner imagen encima de la pieza
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))
    
    # Recalcular posicion
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)