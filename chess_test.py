import tkinter as tk

# Define the initial board state
initial_board = [
    [0, 0, 0, 0, -1, 0, 0, -3],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0]
]

# Create a copy of the initial board for capturing moves
capture_board = [[0 for _ in range(8)] for _ in range(8)]

class ChessBoard(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.selected_piece = None
        self.draw_board()
        self.draw_pieces()
        self.bind("<Button-1>", self.on_click)

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "grey"
                self.create_rectangle(j * 75, i * 75, (j + 1) * 75, (i + 1) * 75, fill=color)

    def draw_pieces(self):
        piece_unicode = {
            1: '\u2654',  # White King
            2: '\u2659',  # White Pawn
            -1: '\u265A',  # Black King
            -3: '\u265C',  # Black Rook
            3: '\u2656',   # White Rook
            -2: '\u265F'   # Black Pawn
        }

        for i in range(8):
            for j in range(8):
                piece = initial_board[i][j]
                if piece != 0:
                    self.create_text((j + 0.5) * 75, (i + 0.5) * 75, text=piece_unicode[piece], font=("Arial", 32), tags="pieces")

    def on_click(self, event):
        col = event.x // 75
        row = event.y // 75

        clicked_piece = initial_board[row][col]

        if self.selected_piece is None and clicked_piece in [2, 3]:  # Allow moving white pawns and white rooks
            self.selected_piece = (row, col)
        elif self.selected_piece is not None:
            if self.is_valid_move(row, col):
                initial_board[row][col] = initial_board[self.selected_piece[0]][self.selected_piece[1]]
                initial_board[self.selected_piece[0]][self.selected_piece[1]] = 0

                # Update capture_board
                self.update_capture_board()

                # Check for pawn promotion
                if initial_board[row][col] == 2 and (row == 0 or row == 7):  # For white pawns reaching the last rank
                    initial_board[row][col] = 3  # Promote to white rook

            self.selected_piece = None

        self.delete("pieces")
        self.draw_pieces()

    def is_valid_move(self, row, col):
        selected_row, selected_col = self.selected_piece
        selected_piece = initial_board[selected_row][selected_col]

        if selected_piece == 2:  # White Pawn
            # Pawn can move one square forward or two squares forward on its first move
            if (row == selected_row - 1 and col == selected_col and initial_board[row][col] == 0) or \
               (row == selected_row - 2 and col == selected_col and selected_row == 6 and initial_board[row][col] == 0):
                return True
            # Pawn can capture diagonally
            elif row == selected_row - 1 and col in (selected_col - 1, selected_col + 1) and initial_board[row][col] == -1:
                return True
            else:
                return False
        elif selected_piece == 3:  # White Rook
            # Rook can move vertically or horizontally any number of squares
            if row == selected_row or col == selected_col:
                # Check if there are no pieces in the way
                if row == selected_row:
                    step = 1 if col > selected_col else -1
                    for j in range(selected_col + step, col, step):
                        if initial_board[row][j] != 0:
                            return False
                elif col == selected_col:
                    step = 1 if row > selected_row else -1
                    for i in range(selected_row + step, row, step):
                        if initial_board[i][col] != 0:
                            return False
                return True
            else:
                return False
        else:
            return False

    def update_capture_board(self):
        for i in range(8):
            for j in range(8):
                # Reset the value in capture_board
                capture_board[i][j] = 0
                # Check if a piece has available moves on the tile
                if initial_board[i][j] != 0:
                    self.selected_piece = (i, j)
                    if self.is_valid_move(i, j):
                        capture_board[i][j] = 1
                        print(capture_board)
                self.selected_piece = None

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess Endgame")

    chess_board = ChessBoard(root, width=600, height=600)
    chess_board.pack()

    root.mainloop()
