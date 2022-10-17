import pygame
import time
import PySimpleGUI as psg
from checkers.constants import BLACK,WHITE, WIDTH, HEIGHT, SQUARE_SIZE
from checkers.board import Board
from checkers.game import Game
import pyautogui
from minimax.algorithm import Min, Poda
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
from checkers.window import Window

pygame.display.set_caption('Damas')

from reinforcement_learning.RL import RL

# Obtener la fila y columna de la posicion del mouse
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main(algoritmo, profundidadNegro,profundidadBlanco):
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption('Damas')

    run = True
    FPS = 60
    clock = pygame.time.Clock()
    window = Window(WIN)
    game = window.game
    min_1 = Min()
    poda_1 = Poda()
    min_2 = Min()
    poda_2 = Poda()
    black_player_nodes = 0
    white_player_nodes = 0
    black_time = []
    white_time = []
    while run:

        clock.tick(FPS)
        winner = game.winner()

        if winner is None:
            if algoritmo == "Minimax vs Minimax":
                minimax_vs_minimax(game, profundidadNegro, profundidadBlanco, min_1, min_2)
                black_player_nodes = min_1.nodos
                white_player_nodes = min_2.nodos
            elif algoritmo == "Poda vs Poda":
                prunning_vs_prunning(game,profundidadNegro, profundidadBlanco, poda_1, poda_2)
                black_player_nodes = poda_1.nodos
                white_player_nodes = poda_2.nodos
            elif algoritmo == "Minimax vs Poda":
                minimax_vs_prunnig(game,profundidadNegro, profundidadBlanco, min_1, poda_1)
                black_player_nodes = min_1.nodos
                white_player_nodes = poda_1.nodos
            elif algoritmo == "Humano vs Poda":
                human_vs_ai(game, profundidadBlanco, poda_1)
                white_player_nodes = poda_1.nodos

            window.update()

        else:
            if winner == BLACK:
                pyautogui.alert("Gano el jugador: NEGRO")
            elif winner == WHITE:
                pyautogui.alert("Gano el jugador: BLANCO")
            else:
                pyautogui.alert("Empate")

            print_nodos(black_player_nodes, white_player_nodes)

            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
            #     row, col = get_row_col_from_mouse(pos)
            #     game.select(row, col)

        window.update()
    pygame.quit()

    #rl.store_dict()


def human_vs_human():
    print()

def human_vs_ai( game, profundidadBlanco,poda):

    if game.turn == WHITE:
        value, new_board = poda.minimax_alpha_beta_prunning(game.get_board(), profundidadBlanco, float('-inf'), float('inf'), True, WHITE, WHITE, game)
        game.ai_move(new_board)
    else:

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

def prunning_vs_prunning(game,profundidadNegro, profundidadBlanco, poda_1, poda_2):

    #s = 'Poda('+ str(profundidadNegro)+') vs Poda('+str(profundidadBlanco)+')'
    #print(s)

    if game.turn == BLACK:
        inicio = time.time()

        value2, new_board2 = poda_1.minimax_alpha_beta_prunning(game.get_board(), profundidadNegro, float('-inf'), float('inf'), True, BLACK, BLACK, game)
        game.ai_move(new_board2)

        tiempoTurno = time.time() - inicio
        #print("Turno del negro : ", round(tiempoTurno, 5), " segundos")
        return BLACK, tiempoTurno

    else:

        inicio = time.time()

        value, new_board = poda_2.minimax_alpha_beta_prunning(game.get_board(), profundidadBlanco, float('-inf'),
                                                              float('inf'), True, WHITE, WHITE, game)
        game.ai_move(new_board)
        tiempoTurno = time.time() - inicio
        #print("Turno del blanco : ", round(tiempoTurno, 5), " segundos")
        return WHITE, tiempoTurno




def prunning_vs_minimax(game,profundidadNegro,profundidadBlanco, poda, min):

    #s = 'Poda(' + str(profundidadNegro) + ') vs Min(' + str(profundidadBlanco) + ')'
    #print(s)

    if game.turn == BLACK:

        inicio = time.time()

        value2, new_board2 = poda.minimax_alpha_beta_prunning(game.get_board(), profundidadNegro, float('-inf'), float('inf'), True, BLACK, BLACK, game)
        game.ai_move(new_board2)

        tiempoTurno = time.time() - inicio
        #print("Turno del negro : ", round(tiempoTurno, 5), " segundos")
        return BLACK, tiempoTurno


    else:

        inicio = time.time()

        value, new_board = min.minimax(game.get_board(), profundidadBlanco, True, WHITE, WHITE, game)
        game.ai_move(new_board)

        tiempoTurno = time.time() - inicio
        #print("Turno del blanco : ", round(tiempoTurno, 5), " segundos")
        return WHITE, tiempoTurno


def minimax_vs_prunnig(game, profundidadNegro, profundidadBlanco, min, poda):
    #s = 'Min(' + str(profundidadNegro) + ') vs Poda(' + str(profundidadBlanco) + ')'
    #print(s)

    if game.turn == BLACK:

        inicio = time.time()

        value2, new_board2 = min.minimax(game.get_board(), profundidadNegro, True, BLACK, BLACK, game)
        game.ai_move(new_board2)

        tiempoTurno = time.time() - inicio
        #print("Turno del blanco : ", round(tiempoTurno, 5), " segundos")
        return BLACK, tiempoTurno

    else:

        inicio = time.time()

        value, new_board = poda.minimax_alpha_beta_prunning(game.get_board(), profundidadBlanco, float('-inf'), float('inf'), True, WHITE, WHITE, game)
        game.ai_move(new_board)

        tiempoTurno = time.time() - inicio
        #print("Turno del negro : ", round(tiempoTurno, 5), " segundos")
        return WHITE, tiempoTurno


def minimax_vs_minimax(game,profundidadNegro, profundidadBlanco, min_1, min_2):

    #s = 'Min(' + str(profundidadNegro) + ') vs Min(' + str(profundidadBlanco) + ')'
    #print(s)

    if game.turn == BLACK:

        inicio = time.time()

        value2, new_board2 = min_1.minimax(game.get_board(), profundidadNegro, True, BLACK, BLACK, game)
        game.ai_move(new_board2)

        tiempoTurno = time.time() - inicio
        #print("Turno del negro : ", round(tiempoTurno, 5), " segundos")
        return BLACK, tiempoTurno


    else:

        inicio = time.time()

        value, new_board = min_2.minimax(game.get_board(), profundidadBlanco, True, WHITE, WHITE, game)
        game.ai_move(new_board)

        tiempoTurno = time.time() - inicio
        #print("Turno del blanco : ", round(tiempoTurno, 5), " segundos")
        return WHITE, tiempoTurno




def print_nodos(black_player_nodes, white_player_nodes):

    negro = "Nodos expandidos por el jugador negro: " + str(black_player_nodes)
    blanco = "Nodos expandidos por el jugador blanco: " + str(white_player_nodes)

    if black_player_nodes != 0:
        print(negro)

    if white_player_nodes != 0:
        print(blanco)



def Menu():

    # minimax_vs_prunnig(game)
    # set the theme for the screen/window
    psg.theme('SystemDefault')
    # define layout
    layout = [[psg.Text('Elegir Algoritmo', size=(20, 1), font='Lucida', justification='left')],
              [psg.Combo(['Minimax vs Minimax', 'Poda vs Poda', 'Minimax vs Poda', 'Humano vs Poda'],default_value='', key='algoritmo')],
              [psg.Text('Elegir Profundidad Negro', size=(30, 1), font='Lucida', justification='left')],
              [psg.Combo( ['2','3','4','5','6'],key='profundidadNegro')],
              [psg.Text('Elegir Profundidad Blanco', size=(30, 1), font='Lucida', justification='left')],
              [psg.Combo(['2', '3', '4', '5', '6'], key='profundidadBlanco')],
              [psg.Button('Ejecutar', font=('Lucida', 10)), psg.Button('Finalizar', font=('Lucida', 10))]]
    # Define Window
    win = psg.Window('Damas', layout)
    while(True):
        # Read  values entered by user
        e, v = win.read()
        # close first window
        if( e == "Finalizar"):
            win.close()
            break
        else:
            if v['algoritmo'] == 'Humano vs Poda':
                main(v['algoritmo'], 0, int(v['profundidadBlanco']))
            else:
                main(v['algoritmo'], int(v['profundidadNegro']), int(v['profundidadBlanco']))
            # psg.popup('' + v['algoritmo'] + ' : ' + v['profundidadNegro'] + ' ' + v['profundidadBlanco'])
