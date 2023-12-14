import operator
from itertools import product


class ChessPiece:

    # история нужна для правильной работы board.unmake_move().
    eaten_pieces_history = []
    has_moved_history = []
    position_history = []

    def __init__(self, color, x, y, unicode):
        self.moved = False
        self.color = color
        self.x = x
        self.y = y
        self.type = self.__class__.__name__
        self.unicode = unicode

    def filter_moves(self, moves, board):
        final_moves = moves[:]

        for move in moves:
            board.make_move(self, move[0], move[1], keep_history=True)

            if board.king_is_threatened(self.color, move):
                final_moves.remove(move)

            board.unmake_move(self)

        return final_moves

    def get_moves(self, board):
        pass

    def get_last_eaten(self):
        return self.eaten_pieces_history.pop()

    def set_last_eaten(self, piece):
        self.eaten_pieces_history.append(piece)

    def set_position(self, x, y, keep_history):
        if keep_history:
            self.position_history.append(self.x)
            self.position_history.append(self.y)
            self.has_moved_history.append(self.moved)

        self.x = x
        self.y = y
        self.moved = True

    def set_old_position(self):
        position_y = self.position_history.pop()
        position_x = self.position_history.pop()
        self.y = position_y
        self.x = position_x
        self.moved = self.has_moved_history.pop()

    def get_score(self):
        return 0

    def __repr__(self):
        return '{}: {}|{},{}'.format(self.type, self.color, self.x, self.y)


class Pawn(ChessPiece):

    def get_moves(self, board):
        moves = []

        if board.game_mode == 0 and self.color == 'white' or board.game_mode == 1 and self.color == 'black':
            direction = 1
        else:
            direction = -1

        x = self.x + direction

        if board.has_empty_block(x, self.y):
            moves.append((x, self.y))
            if self.moved is False and board.has_empty_block(x + direction, self.y):
                moves.append((x + direction, self.y))

        if board.is_valid_move(x, self.y - 1):
            if board.has_opponent(self, x, self.y - 1):
                moves.append((x, self.y - 1))

        if board.is_valid_move(self.x + direction, self.y + 1):
            if board.has_opponent(self, x, self.y + 1):
                moves.append((x, self.y + 1))

        return moves

    def promote(self, board):
        if board.game_mode == 0 and self.y == 0:
            self.type = Rook(self.color, self.x, self.y, '\u2656')

    def get_score(self):
        return 10


class Rook(ChessPiece):

    def get_moves(self, board):
        moves = []
        moves += self.get_vertical_moves(board)
        moves += self.get_horizontal_moves(board)
        return moves

    def get_vertical_moves(self, board):
        moves = []
        for op in [operator.add, operator.sub]:
            for i in range(1, 9):
                x = op(self.x, i)
                if not board.is_valid_move(x, self.y) or board.has_friend(self, x, self.y):
                    break
                if board.has_empty_block(x, self.y):
                    moves.append((x, self.y))
                if board.has_opponent(self, x, self.y):
                    moves.append((x, self.y))
                    break
        return moves

    def get_horizontal_moves(self, board):
        moves = []
        for op in [operator.add, operator.sub]:
            for i in range(1, 9):
                y = op(self.y, i)
                if not board.is_valid_move(self.x, y) or board.has_friend(self, self.x, y):
                    break
                if board.has_empty_block(self.x, y):
                    moves.append((self.x, y))
                if board.has_opponent(self, self.x, y):
                    moves.append((self.x, y))
                    break
        return moves

    def get_score(self):
        return 30


class King(ChessPiece):

    def get_moves(self, board):
        moves = []
        moves += self.get_horizontal_moves(board)
        moves += self.get_vertical_moves(board)
        return moves

    def get_vertical_moves(self, board):
        moves = []
        for op in [operator.add, operator.sub]:
            x = op(self.x, 1)
            if board.has_empty_block(x, self.y) or board.has_opponent(self, x, self.y):
                moves.append((x, self.y))
            if board.has_empty_block(x, self.y + 1) or board.has_opponent(self, x, self.y + 1):
                moves.append((x, self.y+1))
            if board.has_empty_block(x, self.y - 1) or board.has_opponent(self, x, self.y - 1):
                moves.append((x, self.y - 1))
        return moves

    def get_horizontal_moves(self, board):
        moves = []
        for op in [operator.add, operator.sub]:
            y = op(self.y, 1)
            if board.has_empty_block(self.x, y) or board.has_opponent(self, self.x, y):
                moves.append((self.x, y))
        return moves

    def get_score(self):
        return 1000
