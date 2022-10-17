import pygame
from checkers.constants import BLACK,WHITE, WIDTH, HEIGHT, SQUARE_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
from checkers.window import Window
pygame.display.set_caption('Entrenamiento Damas')
from reinforcement_learning.RL import RL
import pickle
import time
FPS = 60
import PySimpleGUI as psg


def watch_learning_table(resultado, cantidad):

    window = Window(WIN)
    game = window.game
    clock = pygame.time.Clock()
    agente = RL(game, BLACK)

    try:

        file = open('learning_table.pkl', 'rb')
        dict = pickle.load(file)
        suma = 0

        if resultado == 'Gana':
            r = 1.0
        elif resultado == 'Empata':
            r = 0.0
        else:
            r = -1.0

        for key in dict:

            if dict[key] == r:

                clock.tick(FPS)
                game.board.board = agente.deserialize_board(key)
                # black, white = number_of_pieces(key)
                #
                # if black == white and black == 12:
                #     continue

                window.update()
                time.sleep(3)
                suma += 1
                if suma == cantidad:
                    break

        file.close()
    except:
        print('No se pudo cargar la tabla de aprendizaje')

    pygame.quit()



def number_of_pieces(serialized_board):

    white = 0
    black = 0

    for i in range(len(serialized_board)):

        char = serialized_board[i]
        if char == '1' or char == '3':
            black += 1
        elif char == '2' or char == '4':
            white += 1

    return black, white


def Menu():

    # minimax_vs_prunnig(game)
    # set the theme for the screen/window
    psg.theme('SystemDefault')
    # define layout
    layout = [[psg.Text('Resultado en fichas negras', size=(20, 1), font='Lucida', justification='left')],
              [psg.Combo(['Gana', 'Empata o Pierde'],default_value='', key='resultado')],
              [psg.Text('Cantidad', size=(30, 1), font='Lucida', justification='left')],
              [psg.Combo( ['10','20','30','50','100'],key='Cantidad')],
              [psg.Button('Aceptar', font=('Lucida', 10)), psg.Button('Finalizar', font=('Lucida', 10))]]
    # Define Window
    win = psg.Window('Learning Table', layout)
    while(True):
        # Read  values entered by user
        e, v = win.read()
        # close first window
        if( e == "Finalizar"):
            win.close()
            break
        else:
            watch_learning_table(v['resultado'], int(v['Cantidad']))

Menu()