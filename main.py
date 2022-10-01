import pygame
from checkers.constants import BLACK, WIDTH, HEIGHT, SQUARE_SIZE, WHITE
from checkers.board import Board
from checkers.game import Game
import pyautogui
from minimax.algorithm import minimax, minimax_alpha_beta_poda
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Damas')

# Obtener la fila y columna de la posicion del mouse
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    game = Game(WIN)
    
    #Seleccionar una pieza y mover por el tablero
    #piece = board.get_piece(0, 1)
    #board.move(piece,7,3)
    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            # El numero indica que tan profundo buscara en el arbol para tomar una decision
            #value, new_board = minimax(game.get_board(), 4, WHITE, game)
            value, new_board = minimax_alpha_beta_poda(game.get_board(), 4, float('-inf'), float('inf'), WHITE, game)
            game.ai_move(new_board)
        else:
            game.update()
        if game.winner() != None:
            if game.winner() == BLACK:
                pyautogui.alert("Gano el jugador: NEGRO")
            else:
                pyautogui.alert("Gano el jugador: BLANCO")
            run = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    pygame.quit()

main()