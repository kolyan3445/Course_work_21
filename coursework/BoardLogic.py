from ChessPiece import *
from copy import deepcopy
import random


class Board:
    whites = []
    blacks = []

    def __init__(self, game_mode, ai=False, depth=2, log=False):  # game_mode == 0 : белые снизу / чёрные сверху
        self.board = []
        self.game_mode = game_mode
        self.depth = depth
        self.ai = ai
        self.log = log

        global Bking_xPos, Bking_yPos, Wking_xPos, Wking_yPos, Wpawn1_xPos, Wpawn1_yPos, Wpawn2_xPos, Wpawn2_yPos, Brook_xPos, Brook_yPos
        Bking_xPos = random.randint(0, 4)
        Bking_yPos = random.randint(0, 2)
        Wking_xPos = random.randint(2, 7)
        Wking_yPos = random.randint(4, 7)
        Wpawn1_xPos = random.randint(0, 2)
        Wpawn1_yPos = random.randint(3, 7)
        Wpawn2_xPos = random.randint(3, 7)
        Wpawn2_yPos = random.randint(3, 4)
        Brook_xPos = random.randint(5, 7)
        Brook_yPos = random.randint(0, 2)


    def initialize_board(self):
        for i in range(8):
            self.board.append(['empty-block' for _ in range(8)])

    def place_pieces(self):
        self.board.clear()
        self.whites.clear()
        self.blacks.clear()
        self.initialize_board()
        self.whiteKing = King('white', Wking_xPos, Wking_yPos, '\u265A')
        self.blackKing = King('black', Bking_xPos, Bking_yPos, '\u2654')
        self[Wking_xPos][Wking_yPos] = self.whiteKing
        self[Bking_xPos][Bking_yPos] = self.blackKing
        self[Wpawn1_xPos][Wpawn1_yPos] = Pawn('white', Wpawn1_xPos, Wpawn1_yPos, '\u265F')
        self[Wpawn2_xPos][Wpawn2_yPos] = Pawn('white', Wpawn2_xPos, Wpawn2_yPos, '\u265F')
        self[Brook_xPos][Brook_yPos] = Rook('black', Brook_xPos, Brook_yPos, '\u265C')

        self.save_pieces()

        if self.game_mode != 0:
            self.reverse()

    def save_pieces(self):
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], ChessPiece):
                    if self[i][j].color == 'white':
                        self.whites.append(self[i][j])
                    else:
                        self.blacks.append(self[i][j])

    def make_move(self, piece, x, y, keep_history=False):  # история отслеживается при поиске компьютером ходов
        old_x = piece.x
        old_y = piece.y
        if keep_history:
            self.board[old_x][old_y].set_last_eaten(self.board[x][y])
        else:
            if isinstance(self.board[x][y], ChessPiece):
                if self.board[x][y].color == 'white':
                    self.whites.remove(self.board[x][y])
                else:
                    self.blacks.remove(self.board[x][y])
        self.board[x][y] = self.board[old_x][old_y]
        self.board[old_x][old_y] = 'empty-block'
        self.board[x][y].set_position(x, y, keep_history)

    def unmake_move(self, piece):
        x = piece.x
        y = piece.y
        self.board[x][y].set_old_position()
        old_x = piece.x
        old_y = piece.y
        self.board[old_x][old_y] = self.board[x][y]
        self.board[x][y] = piece.get_last_eaten()

    def reverse(self):
        self.board = self.board[::-1]
        for i in range(8):
            for j in range(8):
                if isinstance(self.board[i][j], ChessPiece):
                    piece = self.board[i][j]
                    piece.x = i
                    piece.y = j

    def __getitem__(self, item):
        return self.board[item]

    def has_opponent(self, piece, x, y):
        if not self.is_valid_move(x, y):
            return False
        if isinstance(self.board[x][y], ChessPiece):
            return piece.color != self[x][y].color
        return False

    def has_friend(self, piece, x, y):
        if not self.is_valid_move(x, y):
            return False
        if isinstance(self[x][y], ChessPiece):
            return piece.color == self[x][y].color
        return False

    @staticmethod
    def is_valid_move(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def has_empty_block(self, x, y):
        if not self.is_valid_move(x, y):
            return False
        return not isinstance(self[x][y], ChessPiece)

    def get_player_color(self):
        if self.game_mode == 0:
            return 'white'
        return 'black'

    def king_is_threatened(self, color, move=None):
        if color == 'white':
            enemies = self.blacks
            king = self.whiteKing
        else:
            enemies = self.whites
            king = self.blackKing
        threats = []
        for enemy in enemies:
            moves = enemy.get_moves(self)
            if (king.x, king.y) in moves:
                threats.append(enemy)
        if move and len(threats) == 1 and threats[0].x == move[0] and threats[0].y == move[1]:
            return False
        return True if len(threats) > 0 else False

    def is_terminal(self):
        terminal1 = self.white_won()
        terminal2 = self.black_won()
        terminal3 = self.draw()
        return terminal1 or terminal2 or terminal3

    def draw(self):
        if not self.king_is_threatened('white') and not self.has_moves('white'):
            return True
        if not self.king_is_threatened('black') and not self.has_moves('black'):
            return True
        if self.insufficient_material():
            return True
        return False

    def white_won(self):
        if self.king_is_threatened('black') and not self.has_moves('black'):
            return True
        return False

    def black_won(self):
        if self.king_is_threatened('white') and not self.has_moves('white'):
            return True
        return False

    def has_moves(self, color):
        total_moves = 0
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], ChessPiece) and self[i][j].color == color:
                    piece = self[i][j]
                    total_moves += len(piece.filter_moves(piece.get_moves(self), self))
                    if total_moves > 0:
                        return True
        return False

    def insufficient_material(self):
        total_white_pieces = 0
        total_black_pieces = 0

        for piece in self.whites:
            if piece.type != 'King':
                total_white_pieces += 1

        for piece in self.blacks:
            if piece.type != 'King':
                total_black_pieces += 1

        if self.whiteKing and self.blackKing:
            if total_white_pieces + total_black_pieces == 0:
                return True
            if len(self.whites) == 1 and len(self.blacks) == 1:
                return True

    def evaluate(self):
        white_points = 0
        black_points = 0
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], ChessPiece):
                    piece = self[i][j]
                    if piece.color == 'white':
                        white_points += piece.get_score()
                    else:
                        black_points += piece.get_score()
        if self.game_mode == 0:
            return black_points - white_points
        return white_points - black_points

    def __str__(self):
        return str(self[::-1]).replace('], ', ']\n')

    def __repr__(self):
        return 'Board'

    def unicode_array_repr(self):
        data = deepcopy(self.board)
        for idx, row in enumerate(self.board):
            for i, p in enumerate(row):
                if isinstance(p, ChessPiece):
                    un = p.unicode
                else:
                    un = '\u25AF'
                data[idx][i] = un
        return data[::-1]

    def get_king(self, piece):
        if piece.color == 'white':
            return self.whiteKing
        return self.blackKing
