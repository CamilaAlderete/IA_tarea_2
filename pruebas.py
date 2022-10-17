import pygame
from checkers.constants import BLACK,WHITE, WIDTH, HEIGHT, SQUARE_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
from checkers.window import Window
pygame.display.set_caption('Prueba Damas')
from reinforcement_learning.RL import RL
import time
from minimax.algorithm import Min, Poda
from main import minimax_vs_minimax, prunning_vs_prunning, minimax_vs_prunnig, prunning_vs_minimax, print_nodos
import json

FPS = 60

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def pruebas():

    window = Window(WIN)
    game = window.game

    algoritmos = ['min_vs_poda']#, 'min_vs_min', 'poda_vs_poda', 'poda_vs_min', 'rl_vs_min']

    for i in algoritmos:

        wins = draws = losses = 0

        total = 10
        for j in range(total):

            result = start_game(window, i)

            if result == BLACK:
                wins += 1
            elif result == WHITE:
                losses += 1
            else:
                draws += 1

            game.reset()

        store_results(i, wins, draws,losses, total)

    print()



def start_game(window, algorithm):

    run = True
    clock = pygame.time.Clock()
    game = window.game
    min_1 = Min()
    min_2 = Min()
    poda_1 = Poda()
    poda_2 = Poda()
    black_player_nodes = 0
    white_player_nodes = 0
    black_time = []
    white_time = []

    while run:

        clock.tick(FPS)
        winner = game.winner()

        if winner is None:

            if algorithm == 'min_vs_min':

                turno, tiempo = minimax_vs_minimax(game, 3, 3, min_1, min_2)
                black_player_nodes = min_1.nodos
                white_player_nodes = min_2.nodos

                if turno == BLACK:
                    black_time.append(tiempo)
                else:
                    white_time.append(tiempo)

            elif algorithm == 'poda_vs_poda':

                turno, tiempo = prunning_vs_prunning(game, 3, 3, poda_1, poda_2)
                black_player_nodes = poda_1.nodos
                white_player_nodes = poda_2.nodos

                if turno == BLACK:
                    black_time.append(tiempo)
                else:
                    white_time.append(tiempo)

            elif algorithm == 'min_vs_poda':

                turno, tiempo = minimax_vs_prunnig(game, 2, 4, min_1, poda_1)
                black_player_nodes = min_1.nodos
                white_player_nodes = poda_1.nodos

                if turno == BLACK:
                    black_time.append(tiempo)
                else:
                    white_time.append(tiempo)


            # elif algorithm == 'poda_vs_min':
            #
            #     prunning_vs_minimax(game, 2, 3, poda_1, min_1)

            #elif algorithm == 'rl_vs_min':

            #elif algorithm == 'rl_vs_poda'



        else:

            if winner == BLACK:
                r = 'Ganador: Negro'
            elif winner == WHITE:
                r = 'Ganador: Blanco'
            else:
                r = 'Empate'

            print(r)
            print_nodos(black_player_nodes, white_player_nodes)
            print('Tiempo negras:')
            print(black_time)
            print('Tiempo blancas')
            print(white_time)

            return winner


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
            #     row, col = get_row_col_from_mouse(pos)
            #     game.select(row, col)

        window.update()

    #pygame.quit()

def store_results(algorithm, wins, draws, losses, total_games):

    wins_ratio_acum = wins / total_games
    draws_ratio_acum = draws / total_games
    losses_ratio_Acum = losses / total_games

    results = {
        'wins': wins,
        'draws': draws,
        'losses': losses,
        'total_games': total_games,
        'wins_ratio_acum': wins_ratio_acum,
        'draws_ratio_acum' : draws_ratio_acum,
        'losses_ratio_Acum': losses_ratio_Acum
    }

    try:
        file_name = algorithm+'.json'
        file = open(file_name, 'w')
        json.dump(results, file, indent=4)
        file.close()

    except:
        print('No se pudo guardar los resultados')




pruebas()