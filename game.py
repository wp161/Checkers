'''
Wenbo Pan
CS 5001, Fall 2021

This program is for the final project checker.

I referenced this Youtube channel https://www.youtube.com/watch?v=vnd3RfeG3NM
from its tutorial on the design of classes and get avaliable moves
'''

import turtle
import random
import _pickle as pickle
from constants import *
from board import Board
from piece import Piece


class Game:
    '''
    Class: Game
        A game state and logic.
    Attributes:
        board -- A Board object of the gmae
        pen --  Create a turtle object
        turn -- The turn of the game (red/ black)
        selected -- Any piece is selected or not, boolean
        valid_moves -- A dictionary to include valid moves and skipped pieces
                        for the player
        computer_valid_moves -- A dictionary to include valid moves and skipped
                                pieces for the computer
    Methods:
        # update -- Update display every turn
        # select -- Select a piece and move to destination
        # _computer_move -- Take a validated move for the computer
        # _move -- Take a validated move for the player
        # move -- Move a piece on the board and update coordinates
        # change_turn -- Change game turn
        # draw_square -- Draw a square using given size
        # draw_valid_move -- Draw red squares on board to indicate valid moves
        # remove -- Remove pieces that are skipped
        # winner -- Check if there is winner and who wins
        #  remaining_valid_moves -- Check if there's any valid moves avaliable
        # get_computer_pieces -- Get all red pieces objects
        # computer_select_move -- Find the move for the computer and skipped
                                pieces
        # get_valid_move -- create a dictionary indicating valid moves and
                            skipped pieces.
        search_left -- search valid cells and skipped cells in the left
                             direction.
        search_right -- search valid cells and skipped cells in the right
                              direction.
    '''
    def __init__(self):
        self.board = Board()
        self.pen = turtle.Turtle()
        self.turn = PIECES_COLOR[1]
        self.board.draw()
        self.selected = None
        self.valid_moves = {}
        self.computer_valid_moves = {}

    def update(self, x, y):
        '''
        Method -- update
            Update display every turn
        Parameters:
            self -- The Game object
            x -- x coordinate that come from onclick function
            y -- y ccoordinate that come from onclick function
        Returns:
            None
        '''
        self.board.draw()
        self.select(x, y)
        self.draw_valid_move(self.valid_moves)
        if self.turn == PIECES_COLOR[0]:
            move, skip = self.computer_select_move()
            if move is not None:
                self._computer_move(move, skip)
            self.board.draw()
        if self.winner() is not None:
            print(self.winner() + " wins!")

    def select(self, x, y):
        '''
        Method -- select
            Select a piece or moving destination cell
        Parameters:
            self -- The Game object.
            x -- x coordinate that come from onclick function
            y -- y ccoordinate that come from onclick function
        Returns:
            True if a piece is selected. Otherwise False
        '''
        row = int((y + NUM_SQUARES * SQUARE / 2) // SQUARE)
        col = int((x + NUM_SQUARES * SQUARE / 2) // SQUARE)
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
            self.board.draw()

        piece = self.board.get_pieces(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.get_valid_move(piece)
            return True
        return False

    def _computer_move(self, move, skip):
        '''
        Method -- _computer_move
            Take a validated move for the computer
        Parameters:
            self -- The Game object
            move -- A tuple with the selected piece and destination
                    cooridinates
            skip -- A list for all skipped/captured pieces
        Returns:
            No
        '''
        piece = move[1]
        row = move[0][0]
        col = move[0][1]
        self.move(piece, row, col)
        if skip is not None:
            self.remove(skip)
        self.turn = self.change_turn()

    def _move(self, row, col):
        '''
        Method -- _move
            Take a validate move
        Parameters:
            self -- The Game object
            row -- The destination row that the piece is about to move to
            col -- The destination col that the piece is about to move to
        Returns:
            True if the move really occurs, otherwise False
        '''
        piece = self.board.get_pieces(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.remove(skipped)
            self.turn = self.change_turn()
            return True
        else:
            return False

    def move(self, piece, row, col):
        '''
        Method -- move
            Move a piece on a board. Change corresponding coordinates
        Parameters:
            self -- The Game object
            piece -- A Piece object that is going to move
            row -- The row that the piece is about to move to
            col -- The col that the piece is about to move to
        Returns:
            None
        '''
        if piece != 0 and piece.color == self.turn:
            self.board.board[piece.row][piece.col], \
                self.board.board[row][col] \
                = self.board.board[row][col], \
                self.board.board[piece.row][piece.col]
            piece.move(row, col)

    def change_turn(self):
        '''
        Method -- change_turn
            Change game turn
        Parameters:
            self -- The Game object
        Returns:
            The next turn for the game (red/black)
        '''
        self.valid_moves = {}
        if self.turn == PIECES_COLOR[0]:
            return PIECES_COLOR[1]
        else:
            return PIECES_COLOR[0]

    def draw_square(self, size):
        '''
        Method -- draw_square
            Draw a square of a given size.
        Parameters:
            self -- The Game object
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

    def draw_valid_move(self, moves):
        '''
        Method -- draw_valid_move
            Draw red squares indicating valid moves
        Parameters:
            self -- The Game object
            moves -- A dictionary indicating valid moves; (row, col) of valid
                     move as key while a list of captured pieces as value
        Returns:
            None
        '''
        board_size = NUM_SQUARES * SQUARE
        for move in moves:
            col, row = move
            self.pen.setposition(row * SQUARE - board_size // 2,
                                 col * SQUARE - board_size // 2)
            color = VALID_SQUARE
            self.pen.fillcolor(color)
            self.pen.begin_fill()
            self.draw_square(SQUARE)
            self.pen.end_fill()

    def remove(self, skipped):
        '''
        Method -- remove
            Remove pieces that are skipped
        Parameters:
            self -- The Game object
            skipped -- Pieces that are captured, a list of Piece object
        Returns:
            None
        '''
        for item in skipped:
            if item != 0:
                if item.color == PIECES_COLOR[0]:
                    self.board.red_left -= 1
                elif item.color == PIECES_COLOR[1]:
                    self.board.black_left -= 1
                self.board.board[item.row][item.col] = 0

    def winner(self):
        '''
        Method -- isWinner
            Check if there is a winner. If so, print the winter
        Parameters:
            self -- The Game object
        Returns:
            A string indicate the winner (red/black)
        '''
        if (self.board.black_left <= 0 or not
                self.remaining_valid_moves(PIECES_COLOR[1])):
            return RED
        elif (self.board.red_left <= 0 or not
              self.remaining_valid_moves(PIECES_COLOR[0])):
            return BLACK

    def remaining_valid_moves(self, turn):
        '''
        Method -- remaining_valid_moves
            Check if there's any valid moves avaliable
        Parameters:
            self -- The Game object
            turn -- The current game turn (red/black)
        Returns:
            True if there's any valid moves avaliable, otherwise False
        '''
        pieces = []
        condition = []
        for row in self.board.board:
            for piece in row:
                if piece != 0 and piece.color == turn:
                    pieces.append(piece)
        for piece in pieces:
            remaining_valid_moves = self.get_valid_move(piece)
            condition.append(len(remaining_valid_moves) > 0)
        return any(condition)

    def get_computer_pieces(self):
        '''
        Method -- get_computer_pieces
            Get all red pieces objects
        Parameters:
            self -- The Game object
        Returns:
            A list with all red pieces objects
        '''
        pieces = []
        for row in self.board.board:
            for piece in row:
                if piece != 0 and piece.color == PIECES_COLOR[0]:
                    pieces.append(piece)
        return pieces

    def computer_select_move(self):
        '''
        Method -- computer_select_move
            Find the move for the computer and skipped pieces
        Parameters:
            self -- The Game object
        Returns:
            move -- A tuple (new_pos, piece) where new_pos is the available
                    move and piece is associated with this move
            skip -- A list with all captured pieces
        '''
        cap_moves = {}
        noncap_moves = {}
        skip_dic = {}
        for piece in self.get_computer_pieces():
            self.computer_valid_moves = self.get_valid_move(piece)
            for move, skip in self.computer_valid_moves.items():
                if len(skip) != 0:
                    cap_moves.update({move: piece})
                    skip_dic.update({move: skip})
                else:
                    noncap_moves.update({move: piece})
        move = None
        skip = None
        if len(cap_moves) != 0:
            move = key, value = random.choice(list(cap_moves.items()))
            index = move[0]
            skip = skip_dic.get(index)
        elif len(noncap_moves) != 0:
            move = key, value = random.choice(list(noncap_moves.items()))
        return move, skip

    def get_valid_move(self, piece):
        '''
        Method -- get_valid_move
            Create a dictionary indicating valid moves and skipped pieces
        Parameters:
            self -- The Game object
            piece -- the piece that clicked on/selected
        Return:
            moves -- A dictionary with valid moves as key, and a list of
                    skipped pieces as value
        '''
        if isinstance(piece, Piece):
            moves = {}
            left = piece.col - 1
            right = piece.col + 1
            row = piece.row
            if piece.color == PIECES_COLOR[0] or piece.king:
                moves.update(self.search_left(row - 1, max(row - 3, -1),
                                              RED_DIRECTION, piece.color,
                                              left))
                moves.update(self.search_right(row - 1, max(row - 3, -1),
                                               RED_DIRECTION, piece.color,
                                               right))
            if piece.color == PIECES_COLOR[1] or piece.king:
                moves.update(self.search_left(row + 1, min(row + 3,
                                              NUM_SQUARES), BLK_DIRECTION,
                                              piece.color, left))
                moves.update(self.search_right(row + 1, min(row + 3,
                                               NUM_SQUARES), BLK_DIRECTION,
                                               piece.color, right))
            return moves

    def search_left(self, start, end, step, color, left, skipped=[]):
        '''
        Method -- search_left
            Search valid cells and skipped cells in the left side
        Parameters:
            self -- The Game object
            start -- The begining row of a search
            end --  The ending row of a search
            step -- -1 for upward search direction and 1 for downward search
                    direction
            color -- Piece color
            skipped - A list of pieces skipped. Initiated is a empty list
        Return:
            moves -- A dictionary with valid moves as key, and a list of
                    skipped pieces as value
        '''
        moves = {}
        last = []
        for c in range(start, end, step):
            if left < 0:
                break
            current = self.board.board[c][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(c, left)] = last + skipped
                else:
                    moves[(c, left)] = last
                if last:
                    if step == -1:
                        row = max(c - 3, 0)
                    else:
                        row = min(c + 3, NUM_SQUARES)
                    moves.update(self.search_left(c + step, row, step, color,
                                                  left - 1, skipped=last))
                    moves.update(self.search_right(c + step, row, step, color,
                                                   left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves

    def search_right(self, start, end, step, color, right, skipped=[]):
        '''
        Method -- search_right
            Search valid cells and skipped cells in the right side
        Parameters:
            self -- The Game object
            start -- The begining row of a search
            end --  The ending row of a search
            step -- -1 for upward search direction and 1 for downward search
                    direction
            color -- Piece color
            skipped -- A list of pieces skipped. Initiated is a empty list
        Return:
            moves -- A dictionary with valid moves as key, and a list of
                    skipped pieces as value
        '''
        moves = {}
        last = []
        for c in range(start, end, step):
            if right >= NUM_SQUARES:
                break
            current = self.board.board[c][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(c, right)] = last + skipped
                else:
                    moves[(c, right)] = last
                if last:
                    if step == -1:
                        row = max(c - 3, 0)
                    else:
                        row = min(c + 3, NUM_SQUARES)
                    moves.update(self.search_left(c + step, row, step, color,
                                                  right - 1, skipped=last))
                    moves.update(self.search_right(c + step, row, step, color,
                                                   right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves
