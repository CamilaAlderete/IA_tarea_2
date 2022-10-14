import pygame
from .constants import BLACK, WHITE, SQUARE_SIZE, GREEN
from .board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}
        self.white_valid_moves = True
        self.black_valid_moves = True
        self.movimientos_sin_captura = 0

    # def winner(self):
    #     return self.board.winner()

    def reset(self):
       self._init()

    def select(self, row, col):
        #Si una pieza es seleccionada
        if self.selected:
            # mover la pieza a la posicion seleccionada
            result = self._move(row, col)
            # Si seleccion es invalida
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        # Si es 0 no hay pieza seleccionada
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            #mover la pieza seleccionada a la fila y columna
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]

            if skipped:
                self.board.remove(skipped)
                self.movimientos_sin_captura = 0
            else:
                self.movimientos_sin_captura += 1

            self.change_turn()
        else:
            return False

        return True
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN , (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
            self.white_valid_moves = self.board.has_valid_moves(WHITE)
            #print("Turno del blanco")
        else:
            self.turn = BLACK
            self.black_valid_moves = self.board.has_valid_moves(BLACK)
            #print("Turno del negro")

    def get_board(self):
        return self.board

    #retorna un nuevo tablero con la jugada de la ia
    def ai_move(self, board):
        self.difference(board)
        self.board = board
        self.change_turn()


    def winner(self):

        """
        Metodo que verifica la cantidad de piezas restantes y si tiene movimientos validos
        para determinar el color ganador
        """

        if self.movimientos_sin_captura == 100:
            return 'Empate'

        remaining_pieces = self.board.remaining_pieces()
        if self.turn == WHITE:

            if remaining_pieces["white"] == 0:
                return BLACK

            if self.white_valid_moves is False:

                self.black_valid_moves = self.board.has_valid_moves(BLACK)

                #blancas sin movimientos validos pero las negras si tienen, ganan las negras
                if self.black_valid_moves is True:
                    return BLACK

                #blanco ni negro con movimientos validos, empate
                else:
                    return 'Empate'

        else:
            if remaining_pieces["black"] == 0:
                return WHITE

            if self.black_valid_moves is False:

                self.white_valid_moves = self.board.has_valid_moves(WHITE)

                # negras sin movimientos validos pero las blancas si tienen, ganan las blancas
                if self.white_valid_moves is True:
                    return WHITE

                # blanco ni negro con movimientos validos, empate
                else:
                    return 'Empate'


    def difference(self, new_board):

        diff_white = new_board.white_left - self.get_board().white_left
        diff_black = new_board.red_left - self.get_board().red_left

        if diff_white < 0 or diff_black < 0:
            self.movimientos_sin_captura = 0
        else:
            self.movimientos_sin_captura += 1
