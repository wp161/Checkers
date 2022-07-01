'''
Wenbo Pan
CS 5001, Fall 2021

This program is for the final project checker.

I referenced this Youtube channel https://www.youtube.com/watch?v=vnd3RfeG3NM
from its tutorial on the design of classes and get avaliable moves
'''

import turtle
from constants import *
from board import Board
from game import Game


def get_position_click(x, y):
    row = int((y + 200) // SQUARE)
    col = int((x + 200) // SQUARE)
    print(row, col)


def main():
    board_size = NUM_SQUARES * SQUARE
    window_size = board_size + SQUARE
    turtle.setup(window_size, window_size)
    turtle.screensize(board_size, board_size)
    turtle.bgcolor(SQUARE_COLORS[1])
    turtle.tracer(0, 0)

    screen = turtle.Screen()

    board = Board()
    game = Game()
    board.draw()

    screen.onscreenclick(game.update)

    screen.listen()
    turtle.done()


if __name__ == "__main__":
    main()
