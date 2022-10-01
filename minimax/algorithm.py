from sre_parse import WHITESPACE
import pygame
from copy import deepcopy
# deepcopy copia el objeto en vez de la referencia, 
# para no modificar el original

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def simulate_move(piece, move, board,skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
                # Hacer una copia del tablero
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = simulate_move(temp_piece, move, temp_board, skip)
                # Agregar la jugada al arreglo de jugadas
                moves.append(new_board)
    return moves

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

# alpha beta pruning
def minimax_alpha_beta_poda(position, depth, alpha, beta, max_player, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    # Si es el turno de la maquina
    if max_player:
        max_eval = float('-inf')
        best_move = None
        # Recorrer todas las jugadas posibles
        for move in get_all_moves(position, WHITE, game):
            # Hacer la jugada
            evaluation = minimax_alpha_beta_poda(move, depth - 1, alpha, beta, False, game)[0]
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if max_eval == evaluation:
                best_move = move
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax_alpha_beta_poda(move, depth - 1, alpha, beta, True, game)[0]
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if min_eval == evaluation:
                best_move = move
            if beta <= alpha:
                break
        return min_eval, best_move