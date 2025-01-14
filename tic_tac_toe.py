import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the drawing window
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe')

# Define the board and players
board = [['', '', ''],
         ['', '', ''],
         ['', '', '']]

w = width // 3
h = height // 3

ai = 'X'
human = 'O'
currentPlayer = human

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def equals3(a, b, c):
    return a == b and b == c and a != ''

def check_winner():
    winner = None

    # Horizontal
    for i in range(3):
        if equals3(board[i][0], board[i][1], board[i][2]):
            winner = board[i][0]

    # Vertical
    for i in range(3):
        if equals3(board[0][i], board[1][i], board[2][i]):
            winner = board[0][i]

    # Diagonal
    if equals3(board[0][0], board[1][1], board[2][2]):
        winner = board[0][0]
    if equals3(board[2][0], board[1][1], board[0][2]):
        winner = board[2][0]

    open_spots = sum(row.count('') for row in board)

    if winner is None and open_spots == 0:
        return 'tie'
    else:
        return winner

def best_move():
    # Call the minimax function and make the AI move
    global currentPlayer
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = ai
                score = minimax(board, 0, False)
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        board[move[0]][move[1]] = ai
        currentPlayer = human

def minimax(board, depth, is_maximizing):
    result = check_winner()
    if result is not None:
        scores = {'X': 10, 'O': -10, 'tie': 0}
        return scores[result]

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = ai
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = human
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    best_score = min(score, best_score)
        return best_score

def draw():
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, (w, 0), (w, height), 4)
    pygame.draw.line(screen, BLACK, (w * 2, 0), (w * 2, height), 4)
    pygame.draw.line(screen, BLACK, (0, h), (width, h), 4)
    pygame.draw.line(screen, BLACK, (0, h * 2), (width, h * 2), 4)

    for j in range(3):
        for i in range(3):
            x = w * i + w // 2
            y = h * j + h // 2
            spot = board[i][j]
            if spot == human:
                pygame.draw.circle(screen, BLACK, (x, y), w // 4, 4)
            elif spot == ai:
                pygame.draw.line(screen, BLACK, (x - w // 4, y - h // 4), (x + w // 4, y + h // 4), 4)
                pygame.draw.line(screen, BLACK, (x + w // 4, y - h // 4), (x - w // 4, y + h // 4), 4)

    result = check_winner()
    if result:
        pygame.time.wait(500)
        font = pygame.font.Font(None, 74)
        if result == 'tie':
            text = font.render('Tie!', True, BLACK)
        else:
            text = font.render(f'{result} wins!', True, BLACK)
        text_rect = text.get_rect(center=(width//2, height//2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

# Run the game loop
running = True
while running:
    draw()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and currentPlayer == human:
            x, y = event.pos
            i = x // w
            j = y // h
            if board[i][j] == '':
                board[i][j] = human
                currentPlayer = ai
                best_move()

# Done! Time to quit.
pygame.quit()
