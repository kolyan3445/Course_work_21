import pygame
from tkinter import messagebox
from ChessPiece import *
from Computer import get_random_move, get_ai_move

dark_block = pygame.Surface((75, 75))
light_block = pygame.Surface((75, 75))

light_block.fill((255, 255, 255))
dark_block.fill((100, 100, 100))

whitePawn = pygame.image.load('assets/pieces/white_pawn.png')
whitePawn = pygame.transform.scale(whitePawn, (75, 75))
whiteRook = pygame.image.load('assets/pieces/white_rook.png')
whiteRook = pygame.transform.scale(whiteRook, (75, 75))
whiteKing = pygame.image.load('assets/pieces/white_king.png')
whiteKing = pygame.transform.scale(whiteKing, (75, 75))

blackPawn = pygame.image.load('assets/pieces/black_pawn.png')
blackPawn = pygame.transform.scale(blackPawn, (75, 75))
blackRook = pygame.image.load('assets/pieces/black_rook.png')
blackRook = pygame.transform.scale(blackRook, (75, 75))
blackKing = pygame.image.load('assets/pieces/black_king.png')
blackKing = pygame.transform.scale(blackKing, (75, 75))

highlight_block = pygame.image.load('assets/squares/highlight.png')
highlight_block = pygame.transform.scale(highlight_block, (75, 75))

screen = None
pygame.font.init()
font_pg = pygame.font.SysFont('Comic Sans MS', 25)
font_tk = "Colibri 15"


def initialize():
    global screen
    pygame.init()
    pygame.display.set_caption('Эндшпиль')
    icon = pygame.image.load('assets/icon.png')
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((600, 650))
    screen.fill((0, 0, 0))


def draw_background(board):
    
    block_x = 0
    for i in range(4):
        block_y = 0
        for j in range(4):
            screen.blit(light_block, (block_x, block_y))
            screen.blit(dark_block, (block_x + 75, block_y))
            screen.blit(light_block, (block_x + 75, block_y + 75))
            screen.blit(dark_block, (block_x, block_y + 75))
            block_y += 150
        block_x += 150
    step_x = 0
    step_y = pygame.display.get_surface().get_size()[0] - 75
    for i in range(8):
        for j in range(8):
            if isinstance(board[i][j], ChessPiece):
                obj = globals()[f'{board[i][j].color}{board[i][j].type}']
                screen.blit(obj, (step_x, step_y))
            step_x += 75
        step_x = 0
        step_y -= 75
    pygame.display.update()


def draw_text(text):
    s = pygame.Surface((400, 50))
    s.fill((0, 0, 0))
    screen.blit(s, (100, 600))
    text_surface = font_pg.render(text, False, (237, 237, 237))
    x = 230
    text_surface_restart = font_pg.render('Нажмите пробел для перезапуска', False, (237, 237, 237))
    screen.blit(text_surface, (x, 600))
    screen.blit(text_surface_restart, (150, 620))
    pygame.display.update()


def start(board):
    global screen
    possible_piece_moves = []
    running = True
    visible_moves = False
    dimensions = pygame.display.get_surface().get_size()
    game_over = False
    piece = None
    if board.game_mode == 1 and board.ai:
        get_ai_move(board)
        draw_background(board)
    while running:
        if game_over:
            draw_text(game_over_txt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x = 7 - pygame.mouse.get_pos()[1] // 75
                y = pygame.mouse.get_pos()[0] // 75
                if isinstance(board[x][y], ChessPiece) and (board.get_player_color() == board[x][y].color or not board.ai) and (x, y) not in possible_piece_moves:
                    piece = board[x][y]
                    moves = piece.filter_moves(piece.get_moves(board), board)
                    move_positions = []
                    possible_piece_moves = []
                    for move in moves:
                        move_positions.append((dimensions[0] - (8 - move[1]) * 75, dimensions[1] - move[0] * 75 - 125))
                        move_x = 7 - move_positions[-1][1] // 75
                        move_y = move_positions[-1][0] // 75
                        possible_piece_moves.append((move_x, move_y))
                    if visible_moves:
                        draw_background(board)
                        visible_moves = False
                    for move in move_positions:
                        visible_moves = True
                        screen.blit(highlight_block, (move[0], move[1]))
                        pygame.display.update()
                else:
                    clicked_move = (x, y)
                    try:
                        if clicked_move in possible_piece_moves:
                            board.make_move(piece, x, y)
                            possible_piece_moves.clear()
                            draw_background(board)
                            if board.ai:
                                get_ai_move(board)
                                draw_background(board)
                                    
                        if board.white_won():
                            game_over = True
                            game_over_txt = 'Победа белых!'
                        elif board.black_won():
                            game_over = True
                            game_over_txt = 'Победа чёрных!'
                        elif board.draw():
                            game_over = True
                            game_over_txt = 'Ничья!'
                    except UnboundLocalError:
                        pass
