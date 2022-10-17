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
class Min:

    def __init__(self):
        self.nodos = 0

    def minimax(self, position, depth, max_player, player_color, color, game):

        if depth == 0 or game.winner() is not None:
            return position.evaluate(color), position

        opponent_color = get_opponent(player_color)

        if max_player:
            max_eval = float('-inf')
            best_move = None

            # Recorrer todas las jugadas posibles
            moves = get_all_moves(position, player_color, game)
            for move in moves:
                # Hacer la jugada
                evaluation = self.minimax(move, depth - 1, False, opponent_color, color, game)[0]
                max_eval, best_move = max_(max_eval, evaluation, best_move, move)
                self.nodos +=1

            #evita bug que surge cuando ya no se tienen movimientos disponibles
            if len(moves) > 0:
                return max_eval, best_move
            else:
                return position.evaluate(color), position

        else:
            min_eval = float('inf')
            best_move = None

            moves = get_all_moves(position, player_color, game)
            for move in moves:
                evaluation = self.minimax(move, depth - 1, True, opponent_color, color, game)[0]
                min_eval, best_move = min_(min_eval, evaluation, best_move, move)
                self.nodos += 1

            # evita bug que surge cuando ya no se tienen movimientos disponibles
            if len(moves) > 0:
                return min_eval, best_move
            else:
                return position.evaluate(color), position

# alpha beta pruning
class Poda:
    def __init__(self):
        self.nodos = 0
    def minimax_alpha_beta_prunning(self,position, depth, alpha, beta, max_player, player_color, color, game):

        if depth == 0 or game.winner() is not None:
            return position.evaluate(color), position

        opponent_color = get_opponent(player_color)

        if max_player:

            max_eval = float('-inf')
            best_move = None
            moves = get_all_moves(position, player_color, game)

            # Recorrer todas las jugadas posibles
            for move in moves:
                # Hacer la jugada
                evaluation = self.minimax_alpha_beta_prunning(move, depth - 1, alpha, beta, False, opponent_color, color, game)[0]
                max_eval, best_move = max_(max_eval, evaluation, best_move, move)
                alpha = max(alpha, max_eval)
                self.nodos +=1

                if max_eval >= beta:
                    break

            # evita bug que surge cuando ya no se tienen movimientos disponibles
            if len(moves) > 0:
                return max_eval, best_move
            else:
                return position.evaluate(color), position

        else:

            min_eval = float('inf')
            best_move = None
            moves = get_all_moves(position, player_color, game)

            for move in moves:

                evaluation = self.minimax_alpha_beta_prunning(move, depth - 1, alpha, beta, True, opponent_color, color, game)[0]
                min_eval, best_move = min_(min_eval, evaluation, best_move, move)
                beta = min(beta, min_eval)
                self.nodos +=1

                if min_eval <= alpha:
                    break

            # evita bug que surge cuando ya no se tienen movimientos disponibles
            if len(moves) > 0:
                return min_eval, best_move
            else:
                return position.evaluate(color), position

def get_opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def max_(max_eval, eval, best_move, move):
    if eval > max_eval:
        return eval, move
    else:
        return max_eval, best_move

def min_(min_eval, eval, best_move, move):
    if eval < min_eval:
        return eval, move
    else:
        return min_eval, best_move

