import tkinter as tk
from tkinter import *
from tkinter.messagebox import showwarning, showinfo
import json

# Изначальная доска
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

# Копия доски для проверки на возможность взятия и шаха
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
            1: '\u2654',  # Словарь фигур
            2: '\u2659',
            -1: '\u265A',
            -3: '\u265C',
            3: '\u2656',
            -2: '\u265F'
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

        if self.selected_piece is None and clicked_piece in [-1, 1, -2, 2, -3, 3]:  # Ходы
            self.selected_piece = (row, col)
        elif self.selected_piece is not None:
            if self.is_valid_move(row, col):
                initial_board[row][col] = initial_board[self.selected_piece[0]][self.selected_piece[1]]
                initial_board[self.selected_piece[0]][self.selected_piece[1]] = 0

                # Обновление доски захвата
                self.update_capture_board()

                # Превращение пешки
                if initial_board[row][col] == 2 and row == 0:  # Достижение пешкой нужного для превращения ряда
                    initial_board[row][col] = 3  # Превращение белой пешки
                elif initial_board[row][col] == -2 and row == 7:
                    initial_board[row][col] = -3

            self.selected_piece = None

        self.delete("pieces")
        self.draw_pieces()

    def is_valid_move(self, row, col):
        selected_row, selected_col = self.selected_piece
        selected_piece = initial_board[selected_row][selected_col]

        if selected_piece == 2:  # Белая пешка
            # Первый ход пешкой совершается на одну или две клетки, последующие на одну
            if (row == selected_row - 1 and col == selected_col and initial_board[row][col] == 0) or \
               (row == selected_row - 2 and col == selected_col and selected_row == 6 and initial_board[row][col] == 0):
                return True
            # Захват пешкой
            elif row == selected_row - 1 and col in (selected_col - 1, selected_col + 1) and initial_board[row][col] == -1:
                return True
            else:
                return False
        elif selected_piece == 3:  # Белая ладья
            # Ладья может двигаться вертикально и горизонтально на любое количество клеток
            if row == selected_row or col == selected_col:
                # Проверка на фигуры на пути
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
        elif selected_piece == 1: # Белый король
            # Король может двигаться на одну клетку вокруг себя
            if (row in (selected_row - 1, selected_row + 1) and (col in (selected_col + 1, selected_col - 1)) and
                    initial_board[row][col] == 0) and (()):
                return True
            # TODO: Добить короля, выбор цвета игрока, шаховые ситуации и т.д.

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


try:
    file = open("db_test.json", "x+")
except FileExistsError:
    file = open("db_test.json", "a+")
    flag = True


def register():
    user_login = entry_register_name.get()
    user_password = entry_register_password.get()

    with open("db_test.json", "r") as read_file:
        try:
            database_test = list(json.load(read_file))
        except json.JSONDecodeError:
            database_test = None
        print(database_test)
    with open("db_test.json", "w") as file:
        user_exists = False

        if database_test is not None:
            for user in database_test:
                if user_login == user['login']:
                    user_exists = True
                    showwarning('Ошибка', "Такое имя пользователя уже существует!")

        else:
            database_test = []
        if not user_exists:
            database_test.append({'login': user_login, 'password': user_password})
            json.dump(database_test, file)
            showinfo("Успех!", "Регистрация успешна, вы вернётесь к основному экрану.")
            register_window.destroy()


def login():
    user_login = entry_login_name.get()
    user_password = entry_login_password.get()

    with open("db_test.json", "r") as read_file:
        try:
            database_test = list(json.load(read_file))
        except json.JSONDecodeError:
            database_test = None

    with open("db_test.json", "w") as file:  # Проверка на наличие пользователя в базе
        user_exists = False
        if database_test is not None:
            for user in database_test:
                if user['login'] == user_login and user['password'] == user_password:
                    user_exists = True
                    showinfo('Вход прошел успешно', 'Вход совершен')
                    login_success(user_login)

        if not user_exists:
            if database_test is None:
                database_test = []
            showwarning('Ошибка', 'Неверное имя пользователя или пароль')
        json.dump(database_test, file)


def game():
    game_window = tk.Tk()
    game_window.title("Эндшпиль")

    board = ChessBoard(game_window, width=600, height=600)
    board.pack()
    game_window.mainloop()

def login_success(login):
    font = "Calibri 16"

    global welcome_window
    welcome_window = Tk()
    welcome_window.geometry("500x500")
    welcome_window.title("Добро пожаловать!")
    welcome_window.resizable(False, False)

    global color_var
    color_var = IntVar(master=welcome_window, value=0)

    welcome_label = Label(welcome_window, text=f"Добро пожаловать, {login} !", font=font)
    welcome_label.pack()

    color_label = Label(welcome_window, text="Выберите цвет фигур:", font=font)
    color_label.pack()

    radio_button_white = Radiobutton(welcome_window, text="Белые", variable=color_var, value=0, font=font)
    radio_button_black = Radiobutton(welcome_window, text='Чёрные', variable=color_var, value=1, font=font)
    radio_button_white.pack()
    radio_button_black.pack()

    button_start = Button(welcome_window, text="Начать", command=game, bg='brown', fg='white')
    button_start.pack(anchor='center')

    login_window.destroy()


def open_register_window():
    global register_window
    register_window = Toplevel()
    register_window.config(width=500, height=500)
    register_window.title("Регистрация")
    register_window.resizable(False, False)

    global entry_register_name
    entry_register_name = Label(register_window, text="Имя", width=20, font=("bold", 10))
    entry_register_name.place(x=80, y=130)

    entry_register_name = Entry(register_window)
    entry_register_name.place(x=240, y=130)

    global entry_register_password
    entry_register_password = Label(register_window, text="Пароль", width=20, font=("bold", 10))
    entry_register_password.place(x=68, y=180)

    entry_register_password = Entry(register_window)
    entry_register_password.place(x=240, y=180)

    button_done = Button(register_window, text="Регистрация", width=20, command=register, bg='brown', fg='white')
    button_done.place(x=180, y=380)

    label_register = Label(register_window, text="Регистрация", width=20, font=("bold", 20))
    label_register.place(x=90, y=53)


login_window = Tk()
login_window.config(width=500, height=500)
login_window.title("Войти или зарегистрироваться")
login_window.resizable(False, False)

entry_login_name = Label(login_window, text="Имя", width=20, font=("bold", 10))
entry_login_name.place(x=80, y=130)

entry_login_name = Entry(login_window)
entry_login_name.place(x=240, y=130)

entry_login_password = Label(login_window, text="Пароль", width=20, font=("bold", 10))
entry_login_password.place(x=68, y=180)

entry_login_password = Entry(login_window)
entry_login_password.place(x=240, y=180)

button_login = Button(login_window, text="Вход", command=login, width=20, bg='brown',
                      fg='white')  # command=existing_checker()
button_login.place(x=180, y=280)

label_login = Label(login_window, text="Вход", width=20, font=("bold", 20))
label_login.place(x=90, y=53)

button_open_register_window = Button(login_window, text="Регистрация", command=open_register_window, width=20,
                                     bg='brown', fg='white')  # command=existing_checker()
button_open_register_window.place(x=180, y=320)

login_window.mainloop()
