'''
Wenbo Pan
CS 5001, Fall 2021

This program is for the final project checker.

I referenced this Youtube channel https://www.youtube.com/watch?v=vnd3RfeG3NM
from its tutorial on the design of classes and get avaliable moves
'''

NUM_SQUARES = 8  # The number of squares on each row.
SQUARE = 50  # The size of each square in the checkerboard.
SQUARE_COLORS = ("light gray", "white")
VALID_SQUARE = "red"
BOARD_COLOR = "black"
PIECES_COLOR = ("dark red", "black")
CUSHION = PADDING = 1
KING_RADIUS = 20


CIRCLE_RADIUS = (SQUARE / 2) - 1
CIRCLE_POSITION = 0.5
BLACK_ROW = (0, 1, 2)
RED_ROW = (5, 6, 7)

RED = "Red"
BLACK = "Black"

INITIAL_PIECES = 12

RED_DIRECTION = -1
BLK_DIRECTION = 1

FST_ROW = FST_COL = 0
LST_ROW = LST_COL = 7
