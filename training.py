import pygame
from checkers.constants import BLACK,WHITE, WIDTH, HEIGHT, SQUARE_SIZE
from checkers.board import Board
from checkers.game import Game
import pyautogui
from minimax.algorithm import minimax, minimax_alpha_beta_prunning
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
from checkers.window import Window
pygame.display.set_caption('Entrenamiento Damas')
from reinforcement_learning.RL import RL
import pickle
import time


FPS = 60


# Obtener la fila y columna de la posicion del mouse
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def train():

    window = Window(WIN)
    game = window.game
    q_rate_list = [0.8]


    for i in range(len(q_rate_list)):

        agente = RL(game, BLACK)
        agente.set_q_rate(q_rate_list[i])
        agente.training = True
        agente.load_dict()

        for j in range(1):

            # entrenamiento adversarial
            agente.set_N(10000)

            for k in range(agente.N):
                agente.update_alpha(k)
                start_game(agente, window)
                agente.reset()

        if agente.training:
            agente.store_dict()


def validate():

    window = Window(WIN)
    game = window.game
    q_rate_list = [0.8]
    agente = RL(game, BLACK)
    agente.training = False
    agente.load_dict()
    wins = draws = losses = 0

    for i in range(len(q_rate_list)):

        agente.set_q_rate(q_rate_list[i])

        for j in range(1):

            agente.set_N(100)

            for k in range(agente.N):

                result = start_game(agente, window)

                if result == BLACK:
                    wins += 1
                elif result == WHITE:
                    losses += 1
                else:
                    draws += 1

                agente.reset()

    agente.store_validation_results(wins,draws, losses, agente.N)


def start_game(agente, window):

    run = True
    clock = pygame.time.Clock()
    game = window.game

    while run:

        clock.tick(FPS)
        winner = game.winner()

        if winner is None:

            if game.turn == BLACK:
                agente.play()
            else:
                value2, new_board2 = minimax_alpha_beta_prunning(game.get_board(), 2, float('-inf'), float('inf'), True, WHITE, WHITE, game)
                game.ai_move(new_board2)
        else:

            agente.finish(winner)#preguntar condicion de entrenando
            if not agente.training:
                return winner

            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        window.update()

    #pygame.quit()




train()
#validate()