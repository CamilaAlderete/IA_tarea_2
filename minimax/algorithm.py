from sre_parse import WHITESPACE
import pygame
from copy import deepcopy
# deepcopy copia el objeto en vez de la referencia, 
# para no modificar el original

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# nuestra posicion en el tablero, la profundidad del arbol y el jugador
# Si max es true, es el turno de la maquina
def minimax(position, depth, max_player, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    # Si es el turno de la maquina
    if max_player:
        max_eval = float('-inf')
        best_move = None
        # Recorrer todas las jugadas posibles
        for move in get_all_moves(position, WHITE, game):
            # Hacer la jugada
            evaluation = minimax(move, depth - 1, False, game)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
        return min_eval, best_move