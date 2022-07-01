'''
Wenbo Pan
CS 5001, Fall 2021

This program is for the final project checker.

I referenced this Youtube channel https://www.youtube.com/watch?v=vnd3RfeG3NM
from its tutorial on the design of classes and get avaliable moves
'''

from board import Board
from constants import *
from piece import Piece
import pickle


def test_create_board():
    board = Board()
    board.create_board()
    for row in range(NUM_SQUARES):
        for col in range(NUM_SQUARES):
            if col % 2 != row % 2 and row in BLACK_ROW:
                assert(board.board[row][col] != 0)
                assert(board.board[row][col].color == PIECES_COLOR[1])
            elif col % 2 != row % 2 and row in RED_ROW:
                assert(board.board[row][col] != 0)
                assert(board.board[row][col].color == PIECES_COLOR[0])
            else:
                assert(board.board[row][col] == 0)


def test_get_pieces():
    board = Board()
    x1, y1 = 1, 0   # positon has a piece
    x2, y2 = 0, 0   # positon doesn't have a piece
    assert(isinstance(board.get_pieces(x1, y1), Piece))
    assert(board.get_pieces(x2, y2) == 0)
