import random

from minimax.algorithm import simulate_move, get_all_moves, get_opponent, max_, min_
from checkers.game import Game
from checkers.constants import BLACK,WHITE, ROWS, COLS
from checkers.piece import Piece
from checkers.board import Board
import pickle
import json
from minimax.algorithm import get_all_moves, max_
from copy import deepcopy


class RL:

    def __init__(self, game, player_color):
        self.player_color = player_color
        #self.game = game #board actual
        self.last_game_state = None #deepcopy(game) #board y otros datos anteriores del juego
        self.current_game_state = game #board y otros datos actuales del juego
        self.training = False
        self.look_up_table = {}
        self.q_rate = None  #80% elitista, 20% random
        #self.q_rate_list = [0.8]
        self.alpha = 0.5
        self.N = None #training count

    def reset(self):
        self.current_game_state.reset()
        #self.last_game_state.reset()

    def set_N(self, N):
        self.N = N

    def play(self):

        if self.training:

            q = random.random()
            if q <= self.q_rate:
                probability, move = self.play_elitist()
            else:
                probability, move = self.play_random()

            self.update_probability(self.current_game_state, probability)

        else:
            probability, move = self.play_elitist()

        if move is not None:
            self.current_game_state.ai_move(move)
        else:
            self.current_game_state.change_turn()

    def play_elitist(self):

        max_probability = float('-inf') #-1???
        best_move = None
        moves = get_all_moves(self.current_game_state.board, self.player_color, self.current_game_state)
        random.shuffle(moves)

        for move in moves:

            probability = self.reward(move)
            max_probability, best_move = max_(max_probability, probability, best_move, move)

        #no hay movimientos candidatos, perdio o empato
        # if best_move is None:
        #     return 0.0, None

        return max_probability, best_move

    def play_random(self):

        probability = 0.0
        move = None
        moves = get_all_moves(self.current_game_state.board, self.player_color, self.current_game_state)
        random.shuffle(moves)

        if len(moves) > 0:
            move = random.choice(moves)
            probability = self.reward(move)

        # else:
        #     return 0.0, None

        return probability, move


    def reward(self, next_move):

        #Se obtiene la probabilidad del movimiento candidato

        next_game_state = deepcopy(self.current_game_state)
        next_game_state.ai_move(next_move)
        result = next_game_state.winner()

        if result == self.player_color: #gana el jugador
            return 1.0
        elif result == 'Empate': #gana el oponente o empate
            return 0.0
        elif result == self.get_opponent():
            return -1.0
        else:# el juego continua
            return self.get_probability(next_game_state)

    def get_opponent(self):
        if self.player_color == WHITE:
            return BLACK
        else:
            return WHITE

    def get_probability(self, game_status):

        serial = self.serialize_board(game_status.board.board)

        probability = self.look_up_table.get(serial)

        if probability is not None:

            return probability

            #me voy a olvidar del blanco
            # if self.player_color == BLACK:
            #     return probability
            # else:
            #     return 1 - probability
        else:
            #return 0.5
            total = game_status.board.red_left + game_status.board.white_left

            if self.player_color == BLACK:
                return (game_status.board.red_left - game_status.board.white_left)/total
            else:
                return (game_status.board.white_left - game_status.board.red_left)/total



    def get_probability_current_board(self, current_game_state):

        #innecesario el result....
        result = current_game_state.winner()

        if result == self.player_color:
            return 1.0
        elif result == 'Empate':
            return 0.0
        elif result == self.get_opponent():
            return -1.0
        else:
            return self.get_probability(current_game_state)

    def update_probability(self, current_game_state, next_board_prob):

        """
            La tabla de aprendizaje esta estructurada para tener los datos del jugador negro, si el jugador
            es blanco y se desea actualizar la tabla, debe hacerlo pero con el complemento
        """

        probability = self.get_probability_current_board(current_game_state)
        #probability = self.reward(current_board)
        # if self.player_color == WHITE:
        #     next_board_prob = 1 - next_board_prob
        #     probability = 1 - probability #??????????

        probability = probability + self.alpha*(next_board_prob - probability)

        board = self.serialize_board(current_game_state.board.board)
        self.look_up_table.update({board: probability})


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

    # def set_new_board(self, new_board):
    #     # new_board = Board()
    #     # new_board.set_new_board(board)
    #     self.game.difference(new_board)
    #     self.game.board = new_board
    #     #self.game.board.set_new_board(board)

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
            #file = open('learning_table.pkl', 'a')
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

    def finish(self, result):

        if result == self.player_color:
            probability = 1.0
        elif result == self.get_opponent():
            probability = -1.0
        else:
            probability = 0.0

        if self.training:
            board = self.serialize_board(self.current_game_state.board.board)
            self.look_up_table.update({board: probability})

