import pygame
from checkers.constants import BLACK,WHITE, WIDTH, HEIGHT, SQUARE_SIZE
from checkers.board import Board
from checkers.game import Game
import pyautogui
from minimax.algorithm import minimax, minimax_alpha_beta_prunning
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

    while run:
        clock.tick(FPS)

        winner = game.winner()

        if winner is None:

            ai_vs_ai(game)

        else:
            if winner == BLACK:
                pyautogui.alert("Gano el jugador: NEGRO")
            elif winner == WHITE:
                pyautogui.alert("Gano el jugador: BLANCO")
            else:
                pyautogui.alert("Empate")

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


def human_vs_human():
    print()

def human_vs_ai(game):

    if game.turn == WHITE:
        # El numero indica que tan profundo buscara en el arbol para tomar una decision
        # value, new_board = minim0ax(game.get_board(), 4, WHITE, game)
        value, new_board = minimax_alpha_beta_prunning(game.get_board(), 4, float('-inf'), float('inf'), True, WHITE, game)
        game.ai_move(new_board)
    else:
        game.update()

def ai_vs_ai(game):

    if game.turn == WHITE:
        value, new_board = minimax_alpha_beta_prunning(game.get_board(), 2, float('-inf'), float('inf'), True, WHITE, game)
        game.ai_move(new_board)
    else:
        value2, new_board2 = minimax_alpha_beta_prunning(game.get_board(), 4, float('-inf'), float('inf'), True, BLACK, game)
        game.ai_move(new_board2)


main()