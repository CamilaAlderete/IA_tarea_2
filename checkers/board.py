import pygame
from .constants import CAFE, MARRON, ROWS, SQUARE_SIZE, BLACK, WHITE, COLS
from .piece import Piece
class Board:
    def __init__(self):
        self.board = []
        #Tenemos 12 piezas blancas y 12 piezas rojas
        self.red_left = self.white_left = 12
        #Tenemos 0 reyes blancos y 0 reyes rojos(NEGROS)
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(CAFE)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, MARRON, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        # La pieza en la posicion actual se invierten (swap)
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        # Si la pieza llega al final del tablero se convierte en rey
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    #Pasamos una fila y columna y retorna una pieza
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(ROWS):
                if col % 2 == ((row + 1) % 2):
                    # Arriba los blancos
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    # Abajo los negros
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)