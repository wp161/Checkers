'''
Wenbo Pan
CS 5001, Fall 2021

This program is for the final project checker.

I referenced this Youtube channel https://www.youtube.com/watch?v=vnd3RfeG3NM
from its tutorial on the design of classes and get avaliable moves
'''

from piece import Piece
from constants import *


def test_calc_pos():
    row, col = 1, 0
    piece = Piece(row, col, PIECES_COLOR[1])
    piece.calc_pos()
    assert(piece.x == 25)
    assert(piece.y == 75)


def test_make_king():
    piece = Piece(1, 0, PIECES_COLOR[1])
    piece.make_king()
    assert(piece.king is True)


def test_move():
    row, col = 1, 0
    new_row, new_col = 2, 1
    piece = Piece(row, col, PIECES_COLOR[1])

    # Testing normal move
    piece.move(new_row, new_col)
    assert(piece.row == new_row)
    assert(piece.col == new_col)
    assert(piece.king is not True)
    assert(piece.black_kings == 0)
    assert(piece.x == 75)
    assert(piece.y == 125)

    # Move which makes a black piece into a king
    king_row, king_col = 7, 2
    piece.move(king_row, king_col)
    assert(piece.row == king_row)
    assert(piece.col == king_col)
    assert(piece.king is True)
    assert(piece.black_kings == 1)
    assert(piece.x == 125)
    assert(piece.y == 375)

    # Move which makes a red piece into a king
    red_piece = Piece(row, col, PIECES_COLOR[0])
    king_row, king_col = 0, 1
    red_piece.move(king_row, king_col)
    assert(red_piece.row == king_row)
    assert(red_piece.col == king_col)
    assert(red_piece.king is True)
    assert(red_piece.red_kings == 1)
    assert(red_piece.x == 75)
    assert(red_piece.y == 25)
