
import pygame
import sys
import numpy as np

# Initialize pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 64
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
GAME_FONT = pygame.font.SysFont('Arial', 24)
GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Four in a Row')

# Set up the game board and game variables
game_board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
current_player = 1
game_over = False

# Function to draw the game board on the screen
def draw_board():
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            pygame.draw.rect(GAME_WINDOW, (0, 0, 255), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if game_board[row][col] == 1:
                pygame.draw.circle(GAME_WINDOW, (255, 0, 0), (int(col * CELL_SIZE + CELL_SIZE / 2), int(row * CELL_SIZE + CELL_SIZE / 2)), int(CELL_SIZE / 2 - 5))
            elif game_board[row][col] == 2:
                pygame.draw.circle(GAME_WINDOW, (255, 255, 0), (int(col * CELL_SIZE + CELL_SIZE / 2), int(row * CELL_SIZE + CELL_SIZE / 2)), int(CELL_SIZE / 2 - 5))

# Function to handle player input and update the game board accordingly
def handle_input():
    global current_player
    mouse_x, mouse_y = pygame.mouse.get_pos()
    col = int(mouse_x / CELL_SIZE)
    if game_board[0][col] == 0:
        for row in range(BOARD_HEIGHT - 1, -1, -1):
            if game_board[row][col] == 0:
                game_board[row][col] = current_player
                break
        if current_player == 1:
            current_player = 2
        else:
            current_player = 1

# Function to check for a win condition
def check_win():
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if game_board[row][col] == game_board[row][col + 1] == game_board[row][col + 2] == game_board[row][col + 3] != 0:
                return game_board[row][col]
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH):
            if game_board[row][col] == game_board[row + 1][col] == game_board[row + 2][col] == game_board[row + 3][col] != 0:
                return game_board[row][col]
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH - 3):
            if game_board[row][col] == game_board[row + 1][col + 1] == game_board[row + 2][col + 2] == game_board[row + 3][col + 3] != 0:
                return game_board[row][col]
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if game_board[row][col] == game_board[row - 1][col + 1] == game_board[row - 2][col + 2] == game_board[row - 3][col + 3] != 0:
                return game_board[row][col]
    return 0

# Function to display the winner and ask if the players want to play again
def display_winner(winner):
    if winner == 1:
        winner_text = GAME_FONT.render('Player 1 wins!', True, (255, 0, 0))
    elif winner == 2:
        winner_text = GAME_FONT.render('Player 2 wins!', True, (255, 255, 0))
    else:
        winner_text = GAME_FONT.render('Tie game!', True, (255, 255, 255))
    GAME_WINDOW.blit(winner_text, (WINDOW_WIDTH / 2 - winner_text.get_width() / 2, WINDOW_HEIGHT / 2 - winner_text.get_height() / 2))
    pygame.display.update()
    pygame.time.wait(3000)
    play_again_text = GAME_FONT.render('Play again? (Y/N)', True, (255, 255, 255))
    GAME_WINDOW.blit(play_again_text, (WINDOW_WIDTH / 2 - play_again_text.get_width() / 2, WINDOW_HEIGHT / 2 + winner_text.get_height() / 2 + 10))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            handle_input()

    # Draw the game board
    draw_board()

    # Check for a win condition
    winner = check_win()
    if winner != 0:
        game_over = True
        play_again = display_winner(winner)
        if play_again:
            game_board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
            current_player = 1
            game_over = False
        else:
            pygame.quit()
            sys.exit()

    # Update the display
    pygame.display.update()
