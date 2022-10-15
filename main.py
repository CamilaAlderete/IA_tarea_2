import pygame
import time
import PySimpleGUI as psg
from checkers.constants import BLACK,WHITE, WIDTH, HEIGHT, SQUARE_SIZE
from checkers.board import Board
from checkers.game import Game
import pyautogui
from minimax.algorithm import minimax, minimax_alpha_beta_prunning
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


    while run:
        clock.tick(FPS)

        winner = game.winner()

        if winner is None:
            if(algoritmo=="Minimax vs Minimax"):
                minimax_vs_minimax(game,profundidadNegro,profundidadBlanco)
            if (algoritmo=="Prunning vs Prunning"):
                prunning_vs_prunning(game,profundidadNegro,profundidadBlanco)
            if(algoritmo=="Minimax vs Prunnig"):
                minimax_vs_prunnig(game,profundidadNegro,profundidadBlanco)
            if game.turn == WHITE:
                # El numero indica que tan profundo buscara en el arbol para tomar una decision
                # value, new_board = minim0ax(game.get_board(), 4, WHITE, game)
                window.update()
            else:
                window.update()

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

        window.update()
    pygame.quit()

    #rl.store_dict()


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

def prunning_vs_prunning(game,profundidadNegro, profundidadBlanco):

    if game.turn == WHITE:
        inicio = time.time()
        value, new_board = minimax_alpha_beta_prunning(game.get_board(), profundidadBlanco, float('-inf'), float('inf'), True, WHITE, WHITE, game)
        game.ai_move(new_board)
        tiempoTurno = time.time() - inicio
        print("Turno del blanco : ",round(tiempoTurno,5), " segundos")
    else:
        inicio = time.time()
        value2, new_board2 = minimax_alpha_beta_prunning(game.get_board(), profundidadNegro, float('-inf'), float('inf'), True, BLACK, BLACK, game)
        game.ai_move(new_board2)
        tiempoTurno = time.time() - inicio
        print("Turno del negro : ", round(tiempoTurno,5), " segundos")


def minimax_vs_prunnig(game,profundidadNegro,profundidadBlanco):

    if game.turn == WHITE:
        inicio = time.time()
        value, new_board = minimax_alpha_beta_prunning(game.get_board(), profundidadBlanco, float('-inf'), float('inf'), True, WHITE, WHITE, game)
        game.ai_move(new_board)
        tiempoTurno= time.time() - inicio
        print("Turno del blanco : ",round(tiempoTurno,5), " segundos")
    else:
        inicio = time.time()
        value2, new_board2 = minimax(game.get_board(), profundidadNegro, True, BLACK, BLACK, game)
        game.ai_move(new_board2)
        tiempoTurno = time.time() - inicio
        print("Turno del negro : ",round(tiempoTurno,5), " segundos")



def minimax_vs_minimax(game,profundidadBlanco,profundidadNegro):

    if game.turn == WHITE:
        inicio = time.time()
        value, new_board = minimax(game.get_board(), profundidadBlanco, True, WHITE, WHITE, game)
        game.ai_move(new_board)
        tiempoTurno = time.time() - inicio
        print("Turno del blanco : ",round(tiempoTurno,5), " segundos")
    else:
        inicio = time.time()
        value2, new_board2 = minimax(game.get_board(), profundidadNegro, True, BLACK, BLACK, game)
        game.ai_move(new_board2)
        tiempoTurno = time.time() - inicio
        print("Turno del negro : ",round(tiempoTurno,5), " segundos")



def Menu():

    # minimax_vs_prunnig(game)
    # set the theme for the screen/window
    psg.theme('SystemDefault')
    # define layout
    layout = [[psg.Text('Elegir Algoritmo', size=(20, 1), font='Lucida', justification='left')],
              [psg.Combo(['Minimax vs Minimax', 'Prunning vs Prunning', 'Minimax vs Prunnig'],default_value='', key='algoritmo')],
              [psg.Text('Elegir Profundidad Negro', size=(30, 1), font='Lucida', justification='left')],
              [psg.Combo( ['2','3','4','5','6'],key='profundidadNegro')],
              [psg.Text('Elegir Profundidad Blanco', size=(30, 1), font='Lucida', justification='left')],
              [psg.Combo(['2', '3', '4', '5', '6'], key='profundidadBlanco')],
              [psg.Button('Ejecutar', font=('Times New Roman', 12)), psg.Button('Finalizar', font=('Times New Roman', 12))]]
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
            main(v['algoritmo'], int(v['profundidadNegro']), int(v['profundidadBlanco']))
            # psg.popup('' + v['algoritmo'] + ' : ' + v['profundidadNegro'] + ' ' + v['profundidadBlanco'])

Menu()