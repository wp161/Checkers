'''
Wenbo Pan
CS 5001, Fall 2021

This program is for the final project checker.

I referenced this Youtube channel https://www.youtube.com/watch?v=vnd3RfeG3NM
from its tutorial on the design of classes and get avaliable moves
'''

from game import Game
from board import Board
from piece import Piece
from constants import *
import turtle

turtle.tracer(0, 0)


def translate_to_xy(row, col):
    x = col * SQUARE - SQUARE * NUM_SQUARES / 2
    y = row * SQUARE - SQUARE * NUM_SQUARES / 2
    return x, y


def sort_items(items):
    return sorted(items, key=lambda x: (x[0][0], x[0][1]))


def test_select():
    game = Game()
    game.board.board = [[0] * NUM_SQUARES for _ in range(NUM_SQUARES)]
    # The board has a black piece at positon (2,5)
    game.board.board[2][5] = Piece(2, 5, PIECES_COLOR[1])
    game.turn = PIECES_COLOR[1]

    row = 2
    col = 5

    # User clicks at image coordinate (x,y)
    x, y = translate_to_xy(row, col)
    result = game.select(x, y)
    assert(game.selected.row == row)
    assert(game.selected.col == col)
    assert(result is True)
    assert(len(game.valid_moves) > 0)  # The piece has valid moves
    assert(game.turn == PIECES_COLOR[1])

    # Test move after the user has selected a piece
    # This also tested the _move() and move() method
    new_row, new_col = list(game.valid_moves.items())[0][0]
    x, y = translate_to_xy(new_row, new_col)
    result = game.select(x, y)
    assert(game.selected.row == new_row)
    assert(game.selected.col == new_col)
    assert(result is False)
    assert(len(game.valid_moves) == 0)
    assert(game.turn == PIECES_COLOR[0])

    # Reintialize the game board again
    game = Game()
    game.board.board = [[0] * NUM_SQUARES for _ in range(NUM_SQUARES)]
    game.board.board[2][5] = Piece(2, 5, PIECES_COLOR[1])
    game.turn = PIECES_COLOR[1]

    # Test if user select an empty square
    row, col = 0, 0
    x, y = translate_to_xy(row, col)
    result = game.select(x, y)
    assert(game.selected is None)
    assert(result is False)
    assert(len(game.valid_moves) == 0)
    assert(game.turn == PIECES_COLOR[1])

    # Test if user select an invalid move
    # select valid piece
    game = Game()
    game.board.board = [[0] * NUM_SQUARES for _ in range(NUM_SQUARES)]
    game.board.board[2][7] = Piece(2, 7, PIECES_COLOR[1])
    game.turn = PIECES_COLOR[1]

    row, col = 2, 7
    x, y = translate_to_xy(row, col)
    game.select(x, y)
    assert(game.selected is not None)

    # Make an illegal move
    new_row, new_col = 1, 7
    x, y = translate_to_xy(new_row, new_col)
    result = game.select(x, y)
    assert(game.selected is None)
    assert(result is False)
    # Turn doesn't change since there's no move made
    assert(game.turn == PIECES_COLOR[1])


def test_remaining_valid_moves():
    game = Game()
    game.turn = PIECES_COLOR[1]

    assert(game.remaining_valid_moves(PIECES_COLOR[1]) is True)
    assert(game.remaining_valid_moves(PIECES_COLOR[0]) is True)

    # Make a board with just one red piece and two black pieces
    # The red piece is at the bottom left and doesn't have avaliable moves
    game.board.board = [[0] * NUM_SQUARES for _ in range(NUM_SQUARES)]
    game.board.board[7][0] = Piece(7, 0, PIECES_COLOR[0])
    game.board.board[6][1] = Piece(6, 1, PIECES_COLOR[1])
    game.board.board[5][2] = Piece(5, 2, PIECES_COLOR[1])
    assert(game.remaining_valid_moves(PIECES_COLOR[0]) is False)


def test_change_turn():
    game = Game()
    game.turn = PIECES_COLOR[1]
    assert(game.change_turn() == PIECES_COLOR[0])
    game.turn = PIECES_COLOR[0]
    assert(game.change_turn() == PIECES_COLOR[1])


def test_winner():
    game = Game()
    game.board.black_left = 0
    game.board.red_left = 8
    assert(game.winner() == "Red")

    game.board.black_left = 8
    game.board.red_left = 0
    assert(game.winner() == "Black")

    game.board.board = [[0] * NUM_SQUARES for _ in range(NUM_SQUARES)]
    game.board.board[7][0] = Piece(7, 0, PIECES_COLOR[0])
    game.board.board[6][1] = Piece(6, 1, PIECES_COLOR[1])
    game.board.board[5][2] = Piece(5, 2, PIECES_COLOR[1])
    assert(game.winner() == "Black")


def test_get_computer_pieces():
    game = Game()
    pieces = game.get_computer_pieces()
    for piece in pieces:
        assert(piece.color == PIECES_COLOR[0])
    assert(len(pieces) == game.board.red_left)


def test_computer_select_move():
    game = Game()
    game.board.board = [[0] * NUM_SQUARES for _ in range(NUM_SQUARES)]
    game.board.board[7][0] = Piece(7, 0, PIECES_COLOR[0])
    game.board.board[6][1] = Piece(6, 1, PIECES_COLOR[1])
    move, skip = game.computer_select_move()
    new_pos, computer_piece = move
    captured_piece = skip[0]

    assert(game.board.board[6][1] == captured_piece)
    assert(game.board.board[7][0] == computer_piece)
    assert(new_pos[0] == 5 and new_pos[1] == 2)


def test_remove():
    game = Game()
    game.board.board = [[0] * NUM_SQUARES for _ in range(NUM_SQUARES)]
    game.board.board[7][0] = Piece(7, 0, PIECES_COLOR[0])
    game.board.red_left = 1
    game.remove([game.board.board[7][0]])
    assert(game.board.board[7][0] == 0)
    assert(game.board.red_left == 0)


def test__computer_move():
    game = Game()
    game.board.board = [[0] * NUM_SQUARES for _ in range(NUM_SQUARES)]
    game.board.board[7][0] = Piece(7, 0, PIECES_COLOR[0])
    game.board.board[6][1] = Piece(6, 1, PIECES_COLOR[1])
    game.turn = PIECES_COLOR[0]
    move, skip = game.computer_select_move()
    new_pos, computer_piece = move
    game._computer_move(move, skip)
    #  New position of the computer piece
    assert(game.board.board[5][2] == computer_piece)
    assert(game.board.board[6][1] == 0)
    assert(game.turn == PIECES_COLOR[1])


def test_get_valid_move():
    game = Game()
    game.board.board = [[0] * NUM_SQUARES for _ in range(NUM_SQUARES)]

    #  Testing non-capture moves for non-king pieces
    game.board.board[0][1] = Piece(0, 1, PIECES_COLOR[1])
    moves = game.get_valid_move(game.board.board[0][1])
    moves = list(moves.items())
    moves = sort_items(moves)
    move1 = moves[0][0]
    move2 = moves[1][0]
    assert(move1[0] == 1 and move1[1] == 0)
    assert(move2[0] == 1 and move2[1] == 2)
    assert(len(moves) == 2)  # This piece has two valid moves avaliable

    game.board.board[0][7] = Piece(0, 7, PIECES_COLOR[1])
    moves = game.get_valid_move(game.board.board[0][7])
    moves = list(moves.items())
    moves = sort_items(moves)
    move1 = moves[0][0]
    assert(move1[0] == 1 and move1[1] == 6)
    assert(len(moves) == 1)  # This conor piece has one valid move avaliable

    #  Testing non-capture moves for king piece
    game.board.board = [[0] * NUM_SQUARES for _ in range(NUM_SQUARES)]
    game.board.board[4][4] = Piece(4, 4, PIECES_COLOR[1])
    game.board.board[4][4].make_king()

    moves = game.get_valid_move(game.board.board[4][4])
    moves = list(moves.items())
    moves = sort_items(moves)
    move1 = moves[0][0]
    move2 = moves[1][0]
    move3 = moves[2][0]
    move4 = moves[3][0]
    assert(move1[0] == 3 and move1[1] == 3)
    assert(move2[0] == 3 and move2[1] == 5)
    assert(move3[0] == 5 and move3[1] == 3)
    assert(move4[0] == 5 and move4[1] == 5)
    assert(len(moves) == 4)  # This king piece has four valid moves avaliable

    # Testing single-capture moves (capture is the same for king/regular piece)
    game.board.board = [[0] * NUM_SQUARES for _ in range(NUM_SQUARES)]
    game.board.board[0][3] = Piece(0, 3, PIECES_COLOR[1])
    game.board.board[1][4] = Piece(1, 4, PIECES_COLOR[0])
    moves = game.get_valid_move(game.board.board[0][3])
    moves = list(moves.items())
    moves = sort_items(moves)
    move1 = moves[0][0]
    move2 = moves[1][0]
    captured_piece = moves[1][1][0]
    assert(move1[0] == 1 and move1[1] == 2)
    assert(move2[0] == 2 and move2[1] == 5)
    assert(captured_piece == game.board.board[1][4])
    assert(len(moves) == 2)

    # Testing multi-capture moves
    game.board.board[3][4] = Piece(3, 4, PIECES_COLOR[0])
    moves = game.get_valid_move(game.board.board[0][3])
    moves = list(moves.items())
    moves = sort_items(moves)
    move1 = moves[0][0]
    move2 = moves[1][0]
    move3 = moves[2][0]
    captured_piece_1 = moves[2][1][0]
    captured_piece_2 = moves[2][1][1]
    print(moves)
    assert(move1[0] == 1 and move1[1] == 2)
    assert(move2[0] == 2 and move2[1] == 5)
    assert(move3[0] == 4 and move3[1] == 3)
    # The first captured piece
    assert(captured_piece_1 == game.board.board[3][4])
    # The second captured piece
    assert(captured_piece_2 == game.board.board[1][4])
    assert(len(moves) == 3)

    # Since get_valid_moves() calls search_left() and search_right()
    # We can skip the testing for these two methods
    # since get_valid_moves() passes all the tests

    # Some of the test may fail due to the randomness of returned variables
    # If this occures I can execute this code and provide a screenshot
    # to verify the test should work
