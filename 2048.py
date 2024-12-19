import pygame
import random
import os

pygame.init()

# Начальная настройка
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)
button_font = pygame.font.Font('freesansbold.ttf', 18)

# Цветовая палитра для игры 2048
colors = {0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200),
          8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95),
          64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 204, 97),
          512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46),
          'light text': (249, 246, 242), 'dark text': (119, 110, 101),
          'other': (0, 0, 0), 'bg': (187, 173, 160)}

# Игровые переменные
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
if os.path.exists('high_score.txt'):
    with open('high_score.txt', 'r') as file:
        init_high = int(file.readline())
else:
    init_high = 0

high_score = init_high
previous_board = None

restart_button = pygame.Rect(WIDTH - 120, HEIGHT - 80, 100, 30)
undo_button = pygame.Rect(WIDTH - 120, HEIGHT - 40, 100, 30)

def draw_buttons():
    pygame.draw.rect(screen, 'lightgray', restart_button)
    pygame.draw.rect(screen, 'lightgray', undo_button)
    restart_text = button_font.render('Рестарт', True, 'black')
    undo_text = button_font.render('Отменить', True, 'black')
    screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 5))
    screen.blit(undo_text, (undo_button.x + 10, undo_button.y + 5))

def draw_over():
    board_size = min(WIDTH, HEIGHT - 100)
    pygame.draw.rect(screen, 'black', [board_size//4, board_size//4, board_size//2, board_size//4], 0, 10)
    game_over_text1 = font.render('Игра окончена!', True, 'white')
    screen.blit(game_over_text1, (board_size//4 + 20, board_size//4 + 20))

def take_turn(direc, board):
    global score, previous_board
    previous_board = [row[:] for row in board]
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True
    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True
    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True
    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board

def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full

def draw_board():
    board_size = min(WIDTH, HEIGHT - 100)
    pygame.draw.rect(screen, colors['bg'], [0, 0, board_size, board_size], 0, 10)
    score_text = font.render(f'Очки: {score}', True, 'black')
    high_score_text = font.render(f'Рекорд: {high_score}', True, 'black')
    screen.blit(score_text, (10, board_size + 10))
    screen.blit(high_score_text, (10, board_size + 50))

def draw_pieces(board):
    board_size = min(WIDTH, HEIGHT - 100)
    cell_size = board_size // 4
    padding = cell_size // 20
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * cell_size + padding, i * cell_size + padding,
                                             cell_size - 2*padding, cell_size - 2*padding], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font_size = cell_size // 2 - (value_len * 2)
                font = pygame.font.Font('freesansbold.ttf', font_size)
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * cell_size + cell_size // 2,
                                                        i * cell_size + cell_size // 2))
                screen.blit(value_text, text_rect)
            pygame.draw.rect(screen, 'black', [j * cell_size + padding, i * cell_size + padding,
                                               cell_size - 2*padding, cell_size - 2*padding], 2, 5)

# Основной игровой цикл
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    draw_buttons()
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    if game_over:
        draw_over()
        if high_score > init_high:
            file = open('high_score.txt', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                board_values = [[0 for _ in range(4)] for _ in range(4)]
                spawn_new = True
                init_count = 0
                score = 0
                direction = ''
                game_over = False
            elif undo_button.collidepoint(event.pos) and previous_board:
                board_values = previous_board
                previous_board = None
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            if score > high_score:
                high_score = score
    pygame.display.flip()
pygame.quit()
