import pygame
from .constants import BLACK, WHITE
from .board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}

    def reset(self):
       self._init()

    def select(self, row, col):
        #Si una pieza es seleccionada
        if self.selected:
            # mover la pieza a la posicion seleccionada
            result = self._move(row, col)
            # Si seleccion es invalida
            if not result:
                self.selected = None
                self.select(row, col)
        # Si no hay pieza seleccionada
        else:
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True

        return False

    def move(self, row, col):
        piece = self.board.get_piece(row, col)
        # Si es 0 no hay pieza seleccionada
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            #mover la pieza seleccionada a la fila y columna
            self.board.move(self.selected, row, col)
            self.change_turn()
        else:
            return False

        return True
    
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK