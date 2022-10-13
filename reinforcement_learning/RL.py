import random

from minimax.algorithm import simulate_move, get_all_moves, get_opponent, max_, min_
from checkers.game import Game
from checkers.constants import BLACK,WHITE, ROWS, COLS
from checkers.piece import Piece
from checkers.board import Board
import pickle
import json
from minimax.algorithm import minimax, minimax_alpha_beta_prunning, get_all_moves, max_
from copy import deepcopy


class RL:

    def __init__(self, player_color, N):
        self.player_color = player_color
        #self.game = game #board actual
        self.last_board = [] #board anterior
        self.training = False
        self.look_up_table = {}
        self.q_rate = 0.8  #80% elitista, 20% random
        self.q_rate_list = [0.8]
        self.alpha = 0.5
        self.N = N #training count

    def reset(self):
        self.game = self.game.reset()

    def set_N(self, N):
        self.N = N

    def set_game(self, game):
        self.game = game

    #def set_training_var(self, option):
    #    self.training = option

    #def get_training_var(self):
    #    return self.training

    def train(self, training_count, human_training_count, total_experiments):

        self.training = True

        for q in range(self.q_rate_list):

            self.set_q_rate(q)

            for j in range(total_experiments):

                #entrenamiento adversarial
                self.set_N(training_count)
                for i in range(self.N):
                    self.reset()
                    self.update_alpha(i)

                    #jugar

                # entrenamiento contra humano
                self.set_N(human_training_count)
                for i in range(self.N):
                    self.reset()
                    #self.update_alpha(i)
                    # jugar

        #guardar resultados de entrenamiento

    def play(self):

        if self.training:

            q = random.random()
            if q <= self.q_rate:
                probability, move = self.play_elitist()
            else:
                probability, move = self.play_random()

            self.update_probability(self.game.get_board(), probability)

        else:
            probability, move = self.play_elitist()

        self.last_board = self.game.get_board().board
        if move is not None:
            #self.set_new_board(move.board)
            #self.set_new_board(move)
            self.game.ai_move(move)
        else:
            self.game.change_turn()





    def play_elitist(self):

        max_probability = 0.0 #float('-inf')
        best_move = None
        moves = get_all_moves(self.game.get_board(), self.player_color, self.game)
        random.shuffle(moves)

        for move in moves:
            # probability = self.get_probability(move)
            #probability = self.reward(move.board)
            probability = self.reward(move)
            max_probability, best_move = max_(max_probability, probability, best_move, move)

        return max_probability, best_move

    def play_random(self):

        probability = 0.0
        move = None
        moves = get_all_moves(self.game.get_board(), self.player_color, self.game)
        random.shuffle(moves)

        if len(moves) > 0:
            move = random.choice(moves)
            #probability = self.reward(move.board)
            probability = self.reward(move)

        return probability, move

    def validate(self, total_games):

        wins = losses = draws = 0

        self.training = False
        self.reset()

        for i in range(total_games):
            self.reset()
            #jugar
            #result = self.get_game_result()
            ################
            result = True
            if result == 'Win':
                wins += 1
            elif result == 'Draw':
                draws += 1
            else:
                losses += 1

    def reward(self, move):

        prev_move = self.game.get_board()

        #result = self.get_game_result()

        result = self.get_game_result(move)

        if result == self.player_color: #gana el jugador
            return 1.0
        elif result == self.get_opponent() or result == 'Empate': #gana el oponente o empate
            return 0.0
        else: # el juego continua
            return self.get_probability(move.board)

    def get_opponent(self):
        if self.player_color == WHITE:
            return BLACK
        else:
            return WHITE

    def get_probability(self, board):

        move = self.serialize_board(board)

        probability = self.look_up_table.get(move)

        if probability is not None:

            return probability

            #me voy a olvidar del blanco
            # if self.player_color == BLACK:
            #     return probability
            # else:
            #     return 1 - probability
        else:
            return 0.5

    def update_probability(self, current_board, next_board_prob):

        """
            La tabla de aprendizaje esta estructurada para tener los datos del jugador negro, si el jugador
            es blanco y se desea actualizar la tabla, debe hacerlo pero con el complemento
        """

        #probability = self.get_probability(current_board)
        probability = self.reward(current_board)

        # if self.player_color == WHITE:
        #     next_board_prob = 1 - next_board_prob
        #     probability = 1 - probability #??????????

        probability = probability + self.alpha*(next_board_prob - probability)

        board = self.serialize_board(current_board.board)
        self.look_up_table.update({board: probability})



    def get_game_result(self, new_board):

        prev_board = self.game.get_board()
        movimientos_sin_captura = self.game.movimientos_sin_captura

        diff_white = new_board.white_left - prev_board.white_left
        diff_black = new_board.red_left - prev_board.red_left

        if diff_white < 0 or diff_black < 0:
            movimientos_sin_captura = 0
        else:
            movimientos_sin_captura += 1

        if movimientos_sin_captura == 100:
            return 'Empate'

        turn = get_opponent(self.game.turn)
        white_valid_moves = new_board.has_valid_moves(WHITE)
        black_valid_moves = new_board.has_valid_moves(BLACK)
        remaining_pieces = new_board.remaining_pieces()

        if turn == WHITE:

            if remaining_pieces["white"] == 0:
                return BLACK

            if white_valid_moves is False:

                #blancas sin movimientos validos pero las negras si tienen, ganan las negras
                if black_valid_moves is True:
                    return BLACK

                #blanco ni negro con movimientos validos, empate
                else:
                    return 'Empate'

        else:
            if remaining_pieces["black"] == 0:
                return WHITE

            if black_valid_moves is False:

                # negras sin movimientos validos pero las blancas si tienen, ganan las blancas
                if white_valid_moves is True:
                    return WHITE

                # blanco ni negro con movimientos validos, empate
                else:
                    return 'Empate'




    def set_q_rate(self, q_rate):
        self.q_rate = q_rate

    def update_alpha(self, current_game):
        self.alpha = 0.5 - 0.49 * current_game / self.N

    def serialize_board(self, board):

        serialized_board = ''

        for row in board:
            for piece in row:
                if piece == 0:
                    serialized_board += '0'
                elif piece.color == BLACK:
                    if piece.king == False:
                        serialized_board += '1'
                    else:
                        serialized_board += '3'
                else:
                    if piece.king == False:
                        serialized_board += '2'
                    else:
                        serialized_board += '4'

            serialized_board += '5'

        return serialized_board

    def deserialize_board(self, serialized_board):

        board = self.create_empty_board()
        row = 0
        col = 0

        for i in range(len(serialized_board)):

            char = serialized_board[i]
            if char == '0':
                col += 1
            elif char == '1':
                board[row][col] = Piece(row, col, BLACK)
                col += 1
            elif char == '2':
                board[row][col] = Piece(row, col, WHITE)
                col += 1
            elif char == '3':
                piece = Piece(row, col, BLACK)
                piece.make_king()
                board[row][col] = piece
                col += 1
            elif char == '4':
                piece = Piece(row, col, WHITE)
                piece.make_king()
                board[row][col] = piece
                col += 1
            else:
                col = 0
                row += 1

        return board


    def create_empty_board(self):
        board = []
        for row in range(ROWS):
            board.append([])
            for col in range(ROWS):
                board[row].append(0)
        return board

    def set_new_board(self, new_board):
        # new_board = Board()
        # new_board.set_new_board(board)
        self.game.difference(new_board)
        self.game.board = new_board
        #self.game.board.set_new_board(board)

    def store_dict(self):

        try:

            # if self.player_color == WHITE:
            #     file = open('white_table.pkl', 'wb')
            # else:
            #     file = open('black_table.pkl', 'wb')

            file = open('learning_table.pkl', 'wb')
            pickle.dump(self.look_up_table, file)
            file.close()

        except:
            print('No se pudo guardar la tabla de aprendizaje')

    def load_dict(self):

        try:
            # if self.player_color == WHITE:
            #     file = open('white_table.pkl', 'rb')
            # else:
            #     file = open('black_table.pkl', 'rb')
            file = open('learning_table.pkl', 'rb')
            self.look_up_table = pickle.load(file)
            file.close()
        except:
            print('No se pudo cargar la tabla de aprendizaje')


    def store_validation_results(self, wins, draws, losses, total_games):

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

            # if self.player_color == WHITE:
            #     file = open('white_validation_results.json', 'w')
            # else:
            #     file = open('black_validation_results.json', 'w')

            file = open('validation_results.json', 'w')
            json.dump(results, file, indent=4)
            file.close()

        except:
            print('No se pudo guardar los resultados')
