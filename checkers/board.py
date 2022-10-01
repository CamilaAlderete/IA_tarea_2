import pygame
from .constants import CAFE, MARRON, ROWS, SQUARE_SIZE, BLACK, WHITE, COLS
from .piece import Piece
class Board:
    def __init__(self):
        self.board = []
        #Tenemos 12 piezas blancas y 12 piezas rojas
        self.red_left = self.white_left = 12
        #Tenemos 0 reyes blancos y 0 reyes rojos(NEGROS)
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(CAFE)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, MARRON, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # funcion de evaluacion
    # Incentiva a obtener reyes
    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    # Dado el color 
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    

    def move(self, piece, row, col):
        # La pieza en la posicion actual se invierten (swap)
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        # Si la pieza llega al final del tablero se convierte en rey
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    #Pasamos una fila y columna y retorna una pieza
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(ROWS):
                if col % 2 == ((row + 1) % 2):
                    # Arriba los blancos
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    # Abajo los negros
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.white_left -= 1
                else:
                    self.red_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK
        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    
    # traverse_left y traverse_right son funciones recursivas
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        # r es row
        for r in range(start, stop, step):
            #fuera del tablero
            if left < 0:
                break
            current = self.board[r][left]
            # empty square
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                        # evitar bug en piezas negras
                        if row == 0:
                            row = - 1

                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last + skipped))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last + skipped))
                break
            # si tiene el mismo color no se puede avanzar
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                        # evitar bug en piezas negras
                        if row == 0:
                            row = - 1

                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last + skipped))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last + skipped))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves


    def has_valid_moves(self, color):

        #Verifica si tiene movimientos validos que puede realizar un color.

        valid_moves = False

        for row in range(ROWS):
            for col in range(COLS):

                piece = self.board[row][col]
                if piece != 0:

                    if piece.color == color:

                        moves = len(self.get_valid_moves(piece))

                        if moves != 0:
                            valid_moves = True
                            break

        return valid_moves

    def remaining_pieces(self):
        return { "black": self.red_left, "white": self.white_left}