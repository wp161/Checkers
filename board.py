'''
Wenbo Pan
CS 5001, Fall 2021

This program is for the final project checker.

I referenced this Youtube channel https://www.youtube.com/watch?v=vnd3RfeG3NM
from its tutorial on the design of classes and get avaliable moves
'''


import turtle
from constants import *
from piece import Piece


class Board:
    '''
    Class: Board
        A board state and logic.
    Attributes:
        board -- The state of the board, a list
        pen --  Create a turtle object
        red_left -- Number of remaining red pieces on the board
        black_left -- Number of remaining black pieces on the board
        red_pieces -- All red pieces objects on the board, a list
        black_pieces -- All black pieces objects on the board, a list

    Methods:
        draw_square -- Draw a square of a given size
        draw_squares -- Draw squares for the board
        create_board -- Create the state of the board
        draw -- Draw the board with pieces
        get_pieces -- Get the piece object at a given square
    '''
    def __init__(self):
        self.board = []
        self.pen = turtle.Turtle()
        self.red_left = self.black_left = INITIAL_PIECES
        self.red_pieces = []
        self.black_pieces = []
        self.create_board()

    def draw_square(self, size):
        '''
        Method -- draw_square
            Draw a square of a given size.
        Parameters:
            self -- The Board object
            size -- the length of each side of the square
        Returns:
            Nothing. Draws a square in the graphics window.
        '''
        RIGHT_ANGLE = 90
        self.pen.pendown()
        for i in range(4):
            self.pen.forward(size)
            self.pen.left(RIGHT_ANGLE)
        self.pen.penup()

    def draw_squares(self):
        '''
        Method -- draw_squares
            Draw squares for the board
        Parameter:
            self -- The Board object
        Returns:
            None
        '''
        board_size = NUM_SQUARES * SQUARE
        corner = -board_size / 2 - 1
        self.pen.penup()
        self.pen.setposition(corner, corner)
        self.draw_square(board_size)
        for col in range(NUM_SQUARES):
            for row in range(NUM_SQUARES):
                self.pen.setposition(corner + SQUARE * col,
                                     corner + SQUARE * row)
                if col % 2 != row % 2:
                    color = SQUARE_COLORS[0]
                else:
                    color = SQUARE_COLORS[1]
                self.pen.fillcolor(color)
                self.pen.begin_fill()
                self.draw_square(SQUARE)
                self.pen.end_fill()

    def create_board(self):
        '''
        Method -- create_board
            Create the state of the board
        Parameters:
            self -- The Board object
        Returns:
            None
        '''
        for row in range(NUM_SQUARES):
            self.board.append([])
            for col in range(NUM_SQUARES):
                if col % 2 != row % 2:
                    if row in BLACK_ROW:
                        piece = Piece(row, col, PIECES_COLOR[1])
                        self.board[row].append(piece)
                        self.black_pieces.append(piece)
                    elif row in RED_ROW:
                        piece = Piece(row, col, PIECES_COLOR[0])
                        self.board[row].append(piece)
                        self.red_pieces.append(piece)
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self):
        '''
        Method -- draw
            Draw the board with pieces
        Parameters:
            self -- The Board object
        Returns:
            None
        '''
        self.draw_squares()
        for row in range(NUM_SQUARES):
            for col in range(NUM_SQUARES):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw()

    def get_pieces(self, row, col):
        '''
        Method -- get_pieces
            Get the piece object at given square
        Parameters:
            self -- The Board object
            row -- The row of the square
            col -- The col of the square
        Returns:
            A piece object
        '''
        return self.board[row][col]
