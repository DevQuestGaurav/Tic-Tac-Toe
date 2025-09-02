import pygame, sys, random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 900, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Levels")

# Colors
WHITE = (245, 245, 245)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
GRAY = (180, 180, 180)

# Fonts
font = pygame.font.SysFont(None, 100)
button_font = pygame.font.SysFont(None, 50)
result_font = pygame.font.SysFont(None, 60)

# Board
board = [["" for _ in range(3)] for _ in range(3)]
SQUARE_SIZE = WIDTH // 3
LINE_WIDTH = 8

# Difficulty (default None until chosen)
difficulty = None

# Draw grid
def draw_lines():
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, i*SQUARE_SIZE), (WIDTH, i*SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i*SQUARE_SIZE, 0), (i*SQUARE_SIZE, WIDTH), LINE_WIDTH)

# Draw marks
def draw_marks():
    for row in range(3):
        for col in range(3):
            mark = board[row][col]
            if mark != "":
                text = font.render(mark, True, BLUE if mark == "X" else RED)
                screen.blit(text, (col*SQUARE_SIZE + 70, row*SQUARE_SIZE + 30))

# Check winner
def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None

# Check draw
def check_draw():
    for row in board:
        if "" in row:
            return False
    return True

# Computer move based on difficulty
def computer_move(level):
    empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]

    if level == "Easy":
        return random.choice(empty)

    if level == "Medium":
        # Try to win
        for r, c in empty:
            board[r][c] = "O"
            if check_winner() == "O":
                return (r, c)
            board[r][c] = ""
        # Try to block
        for r, c in empty:
            board[r][c] = "X"
            if check_winner() == "X":
                board[r][c] = ""
                return (r, c)
            board[r][c] = ""
        return random.choice(empty)

    if level == "Hard":
        return minimax_move()

# Minimax algorithm for unbeatable AI
def minimax(board, is_maximizing):
    winner = check_winner()
    if winner == "O": return 1
    if winner == "X": return -1
    if check_draw(): return 0

    if is_maximizing:
        best = -2
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = "O"
                    score = minimax(board, False)
                    board[r][c] = ""
                    best = max(score, best)
        return best
    else:
        best = 2
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = "X"
                    score = minimax(board, True)
                    board[r][c] = ""
                    best = min(score, best)
        return best

def minimax_move():
    best_score = -2
    move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = "O"
                score = minimax(board, False)
                board[r][c] = ""
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move

# Draw difficulty menu
def draw_menu():
    screen.fill(WHITE)
    title = result_font.render("Choose Difficulty", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

    easy_btn = pygame.Rect(200, 250, 200, 60)
    med_btn = pygame.Rect(200, 350, 200, 60)
    hard_btn = pygame.Rect(200, 450, 200, 60)

    pygame.draw.rect(screen, GREEN, easy_btn)
    pygame.draw.rect(screen, BLUE, med_btn)
    pygame.draw.rect(screen, RED, hard_btn)

    screen.blit(button_font.render("Easy", True, WHITE), (260, 260))
    screen.blit(button_font.render("Medium", True, WHITE), (235, 360))
    screen.blit(button_font.render("Hard", True, WHITE), (260, 460))

    return easy_btn, med_btn, hard_btn

# Draw restart button
def draw_restart():
    restart_btn = pygame.Rect(200, HEIGHT-70, 200, 50)
    pygame.draw.rect(screen, GRAY, restart_btn)
    screen.blit(button_font.render("Play Again", True, BLACK), (225, HEIGHT-65))
    return restart_btn

# Reset game
def reset_game():
    global board, difficulty, menu
    board = [["" for _ in range(3)] for _ in range(3)]
    difficulty = None
    menu = True

# Game loop
running = True
menu = True

while running:
    screen.fill(WHITE)

    if menu:
        easy_btn, med_btn, hard_btn = draw_menu()
    else:
        draw_lines()
        draw_marks()
        winner = check_winner()
        if winner:
            text = result_font.render(f"{winner} Wins!", True, BLACK)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT-120))
            restart_btn = draw_restart()
        elif check_draw():
            text = result_font.render("Draw!", True, BLACK)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT-120))
            restart_btn = draw_restart()
        else:
            restart_btn = None

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if menu and event.type == pygame.MOUSEBUTTONDOWN:
            if easy_btn.collidepoint(event.pos): difficulty, menu = "Easy", False
            if med_btn.collidepoint(event.pos): difficulty, menu = "Medium", False
            if hard_btn.collidepoint(event.pos): difficulty, menu = "Hard", False

        elif not menu and event.type == pygame.MOUSEBUTTONDOWN:
            winner = check_winner()
            if winner or check_draw():
                if restart_btn and restart_btn.collidepoint(event.pos):
                    reset_game()
                continue

            x, y = event.pos
            row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
            if row < 3 and board[row][col] == "":
                board[row][col] = "X"

                if not check_winner() and not check_draw():
                    r, c = computer_move(difficulty)
                    board[r][c] = "O"
