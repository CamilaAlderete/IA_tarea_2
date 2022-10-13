import pygame
from .constants import CAFE, MARRON, ROWS, SQUARE_SIZE, BLACK, WHITE, COLS, GREEN
from .game import Game
from copy import deepcopy

class Window:
    def __init__(self, win):
        self.game = Game()
        self.win = win
        self.selected = None

    def draw_squares(self, win):
        win.fill(CAFE)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, MARRON, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw(self, win):
        board = self.game.board.board
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece != 0:
                    piece.draw(win)

    def update(self):
        self.draw(self.win)
        self.draw_valid_moves(self.game.valid_moves)
        pygame.display.update()

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN , (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def reset_game(self):
        self.game.reset()
