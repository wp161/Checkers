'''
Sample Code
CS 5001, Fall 2021
This code will get you started with the final project, milestone 1.
'''
import turtle


NUM_SQUARES = 8  # The number of squares on each row.
SQUARE = 50  # The size of each square in the checkerboard.
SQUARE_COLORS = ("light gray", "white")
BOARD_COLOR = "black"
PIECES_COLOR = ("dark red", "black")


def click_handler(x, y):
    '''
        Function -- click_handler
            Called when a click occurs.
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        Returns:
            Does not and should not return. Click handlers are a special type
            of function automatically called by Turtle. You will not have
            access to anything returned by this function.
    '''
    print("Clicked at ", x, y)


def draw_square(pen, size):
    '''
        Function -- draw_square
            Draw a square of a given size.
        Parameters:
            pen -- an instance of pen
            size -- the length of each side of the square
        Returns:
            Nothing. Draws a square in the graphics window.
    '''
    RIGHT_ANGLE = 90
    pen.pendown()
    for i in range(4):
        pen.forward(size)
        pen.left(RIGHT_ANGLE)
    pen.penup()


def draw_circle(pen, size):
    '''
        Function -- draw_circle
            Draw a circle with a given radius.
        Parameters:
            a_turtle -- an instance of Turtle
            size -- the radius of the circle
        Returns:
            Nothing. Draws a circle in the graphics windo.
    '''
    pen.pendown()
    pen.circle(size)
    pen.penup()


def main():
    board_size = NUM_SQUARES * SQUARE
    # Create the UI window. This should be the width of the board plus a
    # little margin
    window_size = board_size + SQUARE  # The extra + SQUARE is the margin
    turtle.setup(window_size, window_size)

    # Set the drawing canvas size. The should be actual board size
    turtle.screensize(board_size, board_size)
    turtle.bgcolor(SQUARE_COLORS[1])  # The window's background color
    turtle.tracer(0, 0)  # makes the drawing appear immediately

    pen = turtle.Turtle()  # This variable does the drawing.
    pen.penup()  # This allows the pen to be moved.
    pen.hideturtle()  # This gets rid of the triangle cursor.

    # The first parameter is the outline color, the second is the filler
    pen.color(BOARD_COLOR, SQUARE_COLORS[1])
    # pen.color(PIECES_COLOR[0], SQUARE_COLORS[1])

    # YOUR CODE HERE

    # Step 1 - the board outline
    corner = -board_size / 2 - 1
    pen.setposition(corner, corner)
    draw_square(pen, board_size)

    # Step 2 & 3 - the checkboard squares
    # pen.color(BOARD_COLOR, SQUARE_COLORS[0])
    for col in range(NUM_SQUARES):
        for row in range(NUM_SQUARES):
            pen.setposition(corner + SQUARE * col, corner + SQUARE * row)
            if col % 2 != row % 2:
                color = SQUARE_COLORS[0]
                pen.fillcolor(color)
                pen.begin_fill()
                draw_square(pen, SQUARE)
                pen.end_fill()

    # Step 4 - the pieces
    CIRCLE_RADIUS = SQUARE / 2
    CIRCLE_POSITION = 0.5
    BLACK_ROW = (0, 1, 2)
    RED_ROW = (5, 6, 7)
    for col in range(NUM_SQUARES):
        for row in range(NUM_SQUARES):
            pen.setposition((corner + SQUARE * (col + CIRCLE_POSITION)),
                            corner + SQUARE * row)
            if col % 2 != row % 2:
                if row in BLACK_ROW:
                    color = PIECES_COLOR[1]
                    pen.color(color)
                    pen.fillcolor(color)
                    pen.begin_fill()
                    draw_circle(pen, CIRCLE_RADIUS)
                    pen.end_fill()
                elif row in RED_ROW:
                    color = PIECES_COLOR[0]
                    pen.color(color)
                    pen.fillcolor(color)
                    pen.begin_fill()
                    draw_circle(pen, CIRCLE_RADIUS)
                    pen.end_fill()

    # Click handling
    screen = turtle.Screen()

    # This will call call the click_handler function when a click occurs
    screen.onclick(click_handler)

    turtle.done()  # Stops the window from closing.


if __name__ == "__main__":
    main()
