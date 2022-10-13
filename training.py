import pygame
from checkers.constants import BLACK,WHITE, WIDTH, HEIGHT, SQUARE_SIZE
from checkers.board import Board
from checkers.game import Game
import pyautogui
from minimax.algorithm import minimax, minimax_alpha_beta_prunning
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Entrenamiento Damas')
from reinforcement_learning.RL import RL

# Obtener la fila y columna de la posicion del mouse
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():

    game = Game(WIN)
    rl = RL(BLACK, 1)
    rl.training = True

    for i in range(len(rl.q_rate_list)):

        rl.set_q_rate(rl.q_rate_list[i])

        for j in range(1):

            # entrenamiento adversarial
            rl.set_N(10000)

            for k in range(rl.N):

                #rl.reset()
                rl.game = game
                rl.update_alpha(k)
                start_game(rl)

            # entrenamiento contra humano
            # rl.set_N(1)
            # for i in range(rl.N):
            #     rl.reset()
                # self.update_alpha(i)
                # jugar


        # rl.set_N(1)
        # rl.training = False
        # for j in range(rl.N):
        #     start_game(rl)


def start_game(rl):

    game = Game(WIN)
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    rl.set_game(game)
    rl.load_dict()

    while run:
        clock.tick(FPS)

        winner = game.winner()

        if winner is None:

            if game.turn == BLACK:
                rl.play()
            else:
                value2, new_board2 = minimax_alpha_beta_prunning(game.get_board(), 2, float('-inf'), float('inf'), True, WHITE, WHITE, game)
                game.ai_move(new_board2)
        else:
            # if winner == BLACK:
            #     pyautogui.alert("Gano el jugador: NEGRO")
            # elif winner == WHITE:
            #     pyautogui.alert("Gano el jugador: BLANCO")
            # else:
            #     pyautogui.alert("Empate")

            rl.store_dict()
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    #pygame.quit()


def human_vs_human():
    print()

def human_vs_ai(game):

    if game.turn == WHITE:
        # El numero indica que tan profundo buscara en el arbol para tomar una decision
        # value, new_board = minim0ax(game.get_board(), 4, WHITE, game)
        value, new_board = minimax_alpha_beta_prunning(game.get_board(), 4, float('-inf'), float('inf'), True, WHITE, WHITE, game)
        game.ai_move(new_board)
    else:
        game.update()

def prunning_vs_prunning(game):

    if game.turn == WHITE:
        value, new_board = minimax_alpha_beta_prunning(game.get_board(), 3, float('-inf'), float('inf'), True, WHITE, WHITE, game)
        game.ai_move(new_board)
    else:
        value2, new_board2 = minimax_alpha_beta_prunning(game.get_board(), 2, float('-inf'), float('inf'), True, BLACK, BLACK, game)
        game.ai_move(new_board2)


def minimax_vs_prunnig(game):

    if game.turn == WHITE:
        value, new_board = minimax_alpha_beta_prunning(game.get_board(), 4, float('-inf'), float('inf'), True, WHITE, WHITE, game)
        game.ai_move(new_board)
    else:
        value2, new_board2 = minimax(game.get_board(), 3, True, BLACK, BLACK, game)
        game.ai_move(new_board2)



def minimax_vs_minimax(game):

    if game.turn == WHITE:
        value, new_board = minimax(game.get_board(), 2, True, WHITE, WHITE, game)
        game.ai_move(new_board)


    else:
        value2, new_board2 = minimax(game.get_board(), 3, True, BLACK, BLACK, game)
        game.ai_move(new_board2)





main()