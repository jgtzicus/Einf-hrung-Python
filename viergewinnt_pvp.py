import pygame
import sys
import random
import numpy as np

# Initialize pygame
pygame.init()

# Set up the game window
CELL_SIZE = 100
RADIUS = int(CELL_SIZE / 2 - 5)
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
WINDOW_WIDTH = CELL_SIZE * BOARD_WIDTH
WINDOW_HEIGHT = CELL_SIZE * (BOARD_HEIGHT + 1)
FONT = pygame.font.SysFont('Arial', 24)
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Four in a Row')

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Set up the game board and game variables
game_board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
PLAYER1 = 1
PLAYER2 = 2 # Can be a real player or AI
current_player = PLAYER1
game_over = False
game_mode = 1 # 1 for PvP and 2 for PvAI

# Function to draw the game board on the pygame screen
def draw_board():
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            pygame.draw.rect(SCREEN, BLUE, (col * CELL_SIZE, (row + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(SCREEN, BLACK, (int(col * CELL_SIZE + CELL_SIZE / 2), int((row + 1) * CELL_SIZE + CELL_SIZE / 2)), RADIUS)
            if game_board[row][col] == 1:
                pygame.draw.circle(SCREEN, RED, (int(col * CELL_SIZE + CELL_SIZE / 2), int((row + 1) * CELL_SIZE + CELL_SIZE / 2)), RADIUS)
            elif game_board[row][col] == 2:
                pygame.draw.circle(SCREEN, YELLOW, (int(col * CELL_SIZE + CELL_SIZE / 2), int((row + 1) * CELL_SIZE + CELL_SIZE / 2)), RADIUS)

# Function to select the game mode
def select_gamemode():
    global game_mode
    game_mode_text = FONT.render('Select game mode', True, WHITE)
    game_mode_options = FONT.render('1 - PvP | 2 - PvAI', True, WHITE)
    SCREEN.blit(game_mode_text, (WINDOW_WIDTH / 2 - game_mode_text.get_width() / 2, CELL_SIZE / 2 - game_mode_text.get_height() / 2 - CELL_SIZE / 8))
    SCREEN.blit(game_mode_options, (WINDOW_WIDTH / 2 - game_mode_options.get_width() / 2, CELL_SIZE / 2 - game_mode_text.get_height() / 2 + CELL_SIZE / 8))
    pygame.display.update()
    while game_mode != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                if event.key == pygame.K_1 or event.key == pygame.K_LEFT:
                    game_mode = 1
                    pygame.draw.rect(SCREEN, BLACK, (0,0, WINDOW_WIDTH, CELL_SIZE))
                    return
                elif event.key == pygame.K_2 or event.key == pygame.K_RIGHT:
                    game_mode = 2
                    pygame.draw.rect(SCREEN, BLACK, (0,0, WINDOW_WIDTH, CELL_SIZE))
                    return

# Function to handle player input and update the game board accordingly
def handle_input():
    global current_player
    global game_mode
    if game_mode == 2 and current_player == PLAYER2:
        col = decide_for_col()
    else:
        mouse_x, _ = pygame.mouse.get_pos()
        col = int(mouse_x / CELL_SIZE)
    print(f'Selected Column: {col}')
    if game_board[0][col] == 0: # If top row of selected col isn't filled
        for row in range(BOARD_HEIGHT - 1, -1, -1): # From down to top (step = -1)
            if game_board[row][col] == 0:
                game_board[row][col] = current_player
                break
        if current_player == 1:
            current_player = 2
        elif current_player == 2:
            current_player = 1
    else:
        handle_input() # Only for the first time of choosing a full row!

# Function to check for a win condition
def check_win():
    for row in range(BOARD_HEIGHT): # horizontal
        for col in range(BOARD_WIDTH - 3):
            if game_board[row][col] == game_board[row][col + 1] == game_board[row][col + 2] == game_board[row][col + 3] != 0:
                return game_board[row][col]
    for row in range(BOARD_HEIGHT - 3): # vertical
        for col in range(BOARD_WIDTH):
            if game_board[row][col] == game_board[row + 1][col] == game_board[row + 2][col] == game_board[row + 3][col] != 0:
                return game_board[row][col]
    for row in range(BOARD_HEIGHT - 3): # top left (bottom right)
        for col in range(BOARD_WIDTH - 3):
            if game_board[row][col] == game_board[row + 1][col + 1] == game_board[row + 2][col + 2] == game_board[row + 3][col + 3] != 0:
                return game_board[row][col]
    for row in range(3, BOARD_HEIGHT): # top right
        for col in range(BOARD_WIDTH - 3):
            if game_board[row][col] == game_board[row - 1][col + 1] == game_board[row - 2][col + 2] == game_board[row - 3][col + 3] != 0:
                return game_board[row][col]
    return 0

# Function to display the winner and ask if the players want to play again
def display_winner(winner):
    if winner == 1:
        winner_text = FONT.render('Player 1 wins!', True, RED)
    elif winner == 2:
        winner_text = FONT.render('Player 2 wins!', True, YELLOW)
    else:
        winner_text = FONT.render('Tie game!', True, WHITE)
    play_again_text = FONT.render('Play again?', True, WHITE)
    SCREEN.blit(winner_text, (WINDOW_WIDTH / 2 - winner_text.get_width() / 2, CELL_SIZE / 2 - winner_text.get_height() / 2 - CELL_SIZE / 8))
    SCREEN.blit(play_again_text, (WINDOW_WIDTH / 2 - play_again_text.get_width() / 2, CELL_SIZE / 2 - play_again_text.get_height() / 2 + CELL_SIZE / 8))
    pygame.display.update()

    # Player input for a new game
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y or event.key == pygame.K_j or event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    return False

# AI should decide for one out of all columns
def decide_for_col():
    return random.randint(0, BOARD_WIDTH - 1) # AI is temporarily random!

# Function to quit the game
def quit_game():
    pygame.quit()
    sys.exit()

def main():
    global game_board
    global current_player
    global game_over
    global game_mode
    # Draw the game board once
    draw_board()
    print(game_board)

    select_gamemode()

    # Main game loop
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(SCREEN, BLACK, (0,0, WINDOW_WIDTH, CELL_SIZE))
                posx = event.pos[0]
                if current_player == PLAYER1:
                    pygame.draw.circle(SCREEN, RED, (posx, int(CELL_SIZE/2)), RADIUS)
                elif current_player == PLAYER2 and game_mode == 1:
                    pygame.draw.circle(SCREEN, YELLOW, (posx, int(CELL_SIZE/2)), RADIUS)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(SCREEN, BLACK, (0,0, WINDOW_WIDTH, CELL_SIZE))
                handle_input()
                print(game_board) # Only for debugging with Terminal

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
                pygame.draw.rect(SCREEN, BLACK, (0,0, WINDOW_WIDTH, CELL_SIZE))
                draw_board()
                select_gamemode()
            else:
                quit_game()

        # Update the display
        pygame.display.update()

if __name__ == '__main__':
    main()