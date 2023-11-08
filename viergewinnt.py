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

pygame.init()