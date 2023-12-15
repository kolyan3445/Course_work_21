import BoardDraw
from BoardLogic import *

from tkinter import *
from tkinter.messagebox import showwarning, showinfo
import json

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
    keep_playing = True
    
    board = Board(game_mode=color_var.get(), ai=True, depth=1, log=True)  # game_mode == 0: белые снизу / 1: чёрные снизу

    welcome_window.destroy()

    while keep_playing:
        BoardDraw.initialize()
        board.place_pieces()
        BoardDraw.draw_background(board)
        keep_playing = BoardDraw.start(board)


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
    radio_button_black = Radiobutton(welcome_window, text='Чёрные', variable=color_var,  value=1, font=font)
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

button_login = Button(login_window, text="Вход", command=login, width=20, bg='brown', fg='white') #command=existing_checker()
button_login.place(x=180, y=280)

label_login = Label(login_window, text="Вход", width=20, font=("bold", 20))
label_login.place(x=90, y=53)

button_open_register_window = Button(login_window, text="Регистрация", command=open_register_window, width=20, bg='brown', fg='white') #command=existing_checker()
button_open_register_window.place(x=180, y=320)

login_window.mainloop()
        
