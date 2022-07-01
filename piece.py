'''
Wenbo Pan
CS 5001, Fall 2021

This program is for the final project checker.

I referenced this Youtube channel https://www.youtube.com/watch?v=vnd3RfeG3NM
from its tutorial on the design of classes and get avaliable moves
'''

import turtle
from constants import *


class Piece:
    '''
    Class: Piece
    Attributes:
        row -- The row coordinate of the piece
        col -- The col coordinate of the piece
        color -- The color of the piece
        king -- If the piece is a king piece, default to False
        red_kings -- Counter of king pieces for red
        black_kings -- Counter of king pieces for black
        pen -- Create a turtle object
        x -- x coordinate of the piece
        y -- y coordinate of the piece
        direction -- The moving direction of the piece
    Methods:
        calc_pos -- Get the position of the piece
        make_king -- Make the piece a king piece
        draw -- Draw pieces
        draw_circle -- Draw a circle with given radius
        move -- Update the position and king state of the piece with a move
    '''
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.red_kings = self.black_kings = 0
        self.pen = turtle.Turtle()

        self.x = 0
        self.y = 0
        self.calc_pos()

        if self.color == PIECES_COLOR[0]:
            self.direction = RED_DIRECTION
        elif self.color == PIECES_COLOR[1]:
            self.direction = BLK_DIRECTION

    def calc_pos(self):
        '''
        Method -- calc_pos
            Get the position of the piece
        Parameters:
            self -- The Piece object
        Returns:
            self.x -- The x coordinate of the piece
            self.y -- The y coordinate of the piece
        '''
        self.x = SQUARE * self.col + SQUARE // 2
        self.y = SQUARE * self.row + SQUARE // 2
        return self.x, self.y

    def make_king(self):
        '''
        Method -- make_king
            Make the piece a king piece
        Parameters:
            self -- The Piece object
        Returns:
            None
        '''
        self.king = True

    def draw(self):
        '''
        Method -- draw
            Draw pieces
        Parameters:
            self -- The Piece object
        Returns:
            None
        '''
        self.pen.penup()
        self.pen.setposition(- SQUARE * NUM_SQUARES // 2 + self.x - CUSHION,
                             - SQUARE * NUM_SQUARES // 2 + self.y
                             - CIRCLE_RADIUS - CUSHION)
        self.pen.color(self.color)
        self.pen.fillcolor(self.color)
        self.pen.begin_fill()
        self.draw_circle(CIRCLE_RADIUS, self.color)
        self.pen.end_fill()
        if self.king:
            self.pen.setposition(- SQUARE * NUM_SQUARES / 2 + self.x - CUSHION,
                                 - SQUARE * NUM_SQUARES / 2 + self.y
                                 - KING_RADIUS - CUSHION)
            self.pen.pendown()
            self.pen.color(SQUARE_COLORS[1])
            self.pen.circle(KING_RADIUS)
            self.pen.penup()

    def draw_circle(self, size, color):
        '''
        Method -- draw_circle
            Draw a circle with a given radius.
        Parameters:
            self -- The Piece object
            size -- The radius of the circle
            color -- The color of the circle
        Returns:
            Nothing. Draws a circle in the graphics window.
        '''
        self.pen.pendown()
        self.pen.color(color)
        self.pen.begin_fill()
        self.pen.circle(size)
        self.pen.end_fill()
        self.pen.penup()

    def move(self, row, col):
        '''
        Method -- move
            Update the position and king state of the piece with a move
        Parameters:
            self -- The Piece object
            row -- The new/destination row coordinate
            col -- The new/destination col coordinate
        Returns:
            None
        '''
        self.row = row
        self.col = col
        if self.row == FST_ROW and self.color == PIECES_COLOR[0]:
            self.make_king()
            self.red_kings += 1
        if self.row == LST_ROW and self.color == PIECES_COLOR[1]:
            self.make_king()
            self.black_kings += 1
        self.x, self.y = self.calc_pos()
