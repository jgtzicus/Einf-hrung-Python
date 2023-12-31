import pygame
import sys
import random
import math

# Globale Konstanten
ROW_COUNT = 6 # oben = 6, unten = 1
COLUMN_COUNT = 7 # links = 7, rechts = 1
SQUARE_SIZE = 100 # in Pixel als Maßstab
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)
ROT = (255, 0, 0)
GELB = (255, 255, 0)

# Funktionen
def create_board(): # Erstellt das Spielfeld als Array
    board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
    return board

def drop_piece(board, row, col, piece): # Schreibt AI_PIECE also 2 oder PLAYER_PIECE also 1 in ein vorgegebenes Feld
    board[row][col] = piece

def is_valid_location(board, col): # Überprüft, ob die oberste Reihe einer Spalte noch frei ist 
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col): # Sucht innerhalb einer Spalte die nächste freie Reihe
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece): # Überprüft in alle Richtungen, ob ein Gewinnen vorliegt
    # Überprüfen auf horizontale Gewinnmöglichkeiten
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Überprüfen auf vertikale Gewinnmöglichkeiten
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Überprüfen auf diagonale Gewinnmöglichkeiten (nach oben rechts)
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

    # Überprüfen auf diagonale Gewinnmöglichkeiten (nach oben links)
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Score Diagonal (nach oben rechts)
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score Diagonal (nach oben links)
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer): # Minimax-Algorithmus
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -float("inf")
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = float("inf")
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, (0,0,255), (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, (0,0,0), (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), int(SQUARE_SIZE/2 - 5))

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, (255,0,0), (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), int(SQUARE_SIZE/2 - 5))
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, (255,255,0), (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), int(SQUARE_SIZE/2 - 5))
    pygame.display.update()

def print_board(board):
    for row in board:
        print(row)

board = create_board()
print_board(board)
game_over = False

pygame.init()

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE

size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("monospace", 75)

turn = PLAYER

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, SCHWARZ, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, ROT, (posx, int(SQUARE_SIZE / 2)), int(SQUARE_SIZE / 2 - 5))

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, SCHWARZ, (0, 0, width, SQUARE_SIZE))
            # Spieler Eingabe
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = font.render("Spieler gewinnt!!", 1, ROT)
                        screen.blit(label, (40, 10))
                        game_over = True

                    if len(get_valid_locations(board)) == 0:  # Überprüfen auf Unentschieden
                        label = font.render("Unentschieden!", 1, WEISS)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)

    # KI Eingabe
    if turn == AI and not game_over: # doppelte Abfrage nach game_over (trotz while-Schleife), da sich der Wert bereits geändert haben kann!
        col, _ = minimax(board, 4, -float("inf"), float("inf"), True)  # Reduziere die Suchtiefe, um die Spielzeit zu begrenzen

        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = font.render("KI gewinnt!!", 1, GELB)
                screen.blit(label, (40, 10))
                game_over = True

            if len(get_valid_locations(board)) == 0:  # Überprüfen auf Unentschieden
                label = font.render("Unentschieden!", 1, WEISS)
                screen.blit(label, (40, 10))
                game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)