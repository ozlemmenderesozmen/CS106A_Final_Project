"""
Brick Breaker Game
The player must crush a wall of bricks by deflecting a bouncing ball with a paddle.
The paddle may move horizontally and is controlled with the computer's mouse.
The player gets 3 lives to start with; a life is lost if the ball hits the bottom of the screen.
When all the bricks have been destroyed, the player wins the game.
There is only 1 level in the game.
"""

import tkinter
import time
import keyboard

# How big is the playing area?
CANVAS_WIDTH = 600  # Width of drawing canvas in pixels
CANVAS_HEIGHT = 800  # Height of drawing canvas in pixels

# Constants for the bricks
N_ROWS = 8  # How many rows of bricks are there?
N_COLS = 10  # How many columns of bricks are there?
SPACING = 5  # How much space is there between each brick?
BRICK_START_Y = 50  # The y coordinate of the top-most brick
BRICK_HEIGHT = 20  # How many pixels high is each brick
BRICK_WIDTH = (CANVAS_WIDTH - (N_COLS + 1) * SPACING) / N_COLS

# Constants for the ball and paddle
BALL_SIZE = 40
PADDLE_Y = CANVAS_HEIGHT - 40
PADDLE_WIDTH = 120

CHANGE_X = 10
CHANGE_Y = 10


def main():
    count = 0
    # playing area is created
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Brick Breaker')
    for i in range(3):
        count += 1
        # playing elements are created
        bricks = building_bricks(canvas)
        ball = create_a_ball(canvas)
        paddle = create_paddle(canvas)
        canvas.update()
        # with pressing space from keyboard, the game starts
        wait_until_player_press_space()
        play_brick_breaker_game(canvas, ball, paddle, bricks, count)
        canvas.update()
        wait_until_player_press_space()
        canvas.delete(tkinter.ALL)


def wait_until_player_press_space():
    # game stops until player press space
    while not press_space():
        time.sleep(1 / 10)


def building_bricks(canvas):
    # returns and creates bricks
    bricks = []
    for row in range(N_ROWS):
        for col in range(N_COLS):
            a_brick = create_a_brick(canvas, row, col)
            bricks.append(a_brick)

    return bricks


def create_a_brick(canvas, row, col):
    # creates and returns a brick
    left_x = col * (SPACING + BRICK_WIDTH)
    top_y = BRICK_START_Y + row * (BRICK_HEIGHT + SPACING)
    end_x = left_x + (CANVAS_WIDTH - (N_COLS + 1) * SPACING) / N_COLS
    end_y = top_y + BRICK_HEIGHT
    colour = get_colour(row)
    brick = canvas.create_rectangle(left_x, top_y, end_x, end_y, fill=colour, outline='white')

    return brick


def get_colour(row):
    # returns the colour for bricks
    if row == 0 or row == 1 or row == 2:
        return 'red'
    if row == 3 or row == 4 or row == 5:
        return 'yellow'
    else:
        return 'blue'


def create_a_ball(canvas):
    # creates and returns the ball
    start_y = CANVAS_HEIGHT / 2 - BALL_SIZE / 2
    end_y = start_y + BALL_SIZE
    start_x = CANVAS_WIDTH / 2 - BALL_SIZE / 2
    end_x = start_x + BALL_SIZE
    ball = canvas.create_oval(start_x, start_y, end_x, end_y, fill='black')

    return ball


def create_paddle(canvas):
    # creates and returns the paddle
    paddle = canvas.create_rectangle(0, PADDLE_Y, PADDLE_WIDTH, CANVAS_HEIGHT - 20, fill='black')
    return paddle


def play_brick_breaker_game(canvas, ball, paddle, bricks, count):
    # starts the game and designs the conditions of how it ends
    dx = CHANGE_X
    dy = CHANGE_Y
    while True:
        move_paddle(canvas, paddle)  # move paddle

        canvas.move(ball, dx, dy)  # move ball
        if hit_left_wall(canvas, ball) or hit_right_wall(canvas, ball):  # if ball hits left or right wall
            dx *= -1
        elif hit_top_wall(canvas, ball):  # if ball hits top wall
            dy *= -1
        elif hit_paddle(canvas, paddle):  # if ball hits paddle
            dx, dy = bounce_ball_when_hits_paddle(canvas, ball, paddle, dx, dy)
        elif is_ball_lower_than_paddle(canvas, ball, paddle):  # if ball is in lower level than paddle
            if count == 1:
                two_more_play(canvas)
                break
            elif count == 2:
                one_more_play(canvas)
                break
            elif count == 3:
                game_over(canvas)
                break
        elif hit_bricks(canvas, bricks):  # if ball hits bricks
            dy *= -1
        elif len(bricks) == 0:  # if ball hits all bricks and there are no more bricks
            win_the_game(canvas)
            break

        canvas.update()         # redraw canvas
        time.sleep(1 / 50.)       # pause


def move_paddle(canvas, paddle):
    # moves paddle according to mouse movement
    mouse_x = canvas.winfo_pointerx()
    paddle_left_x = min(mouse_x, CANVAS_WIDTH - PADDLE_WIDTH)
    canvas.moveto(paddle, paddle_left_x, PADDLE_Y)


def two_more_play(canvas):
    # first try
    canvas.create_text(300, 500, fill="black", font="Times 30 bold",
                       text="2 MORE")


def one_more_play(canvas):
    # second try
    canvas.create_text(300, 500, fill="black", font="Times 30 bold",
                       text="1 MORE")


def game_over(canvas):
    # third try
    canvas.create_text(300, 500, fill="red", font="Times 30 bold",
                       text="GAME OVER")


def win_the_game(canvas):
    # writes to the screen that player win the game
    canvas.create_text(300, 500, fill="black", font="Times 30 bold",
                       text="YOU WIN")


def is_ball_lower_than_paddle(canvas, ball, paddle):
    # returns the condition - ball is lower than paddle
    return get_bottom_y(canvas, ball) > get_top_y(canvas, paddle)


def hit_paddle(canvas, paddle):
    # this graphics method gets the location of the paddle as a list
    paddle_coords = canvas.coords(paddle)

    # the list has four elements:
    x1 = paddle_coords[0]
    y1 = paddle_coords[1]
    x2 = paddle_coords[2]
    y2 = paddle_coords[3]

    # we can then get a list of all objects in that area
    results = canvas.find_overlapping(x1, y1, x2, y2)

    return len(results) > 1


def bounce_ball_when_hits_paddle(canvas, ball, paddle, dx, dy):
    # bounces the ball when the ball hits the paddle
    if get_right_x(canvas, ball) <= (get_left_x(canvas, paddle) + BALL_SIZE / 2) and dx > 0:
        dx *= -1
    elif get_left_x(canvas, ball) >= (get_right_x(canvas, paddle) - BALL_SIZE / 2) and dx < 0:
        dx *= -1
    dy *= -1
    return dx, dy


def hit_bricks(canvas, bricks):
    for brick in bricks:
        # this graphics method gets the location of the bricks as a list
        brick_coords = canvas.coords(brick)

        # the list has four elements:
        x1 = brick_coords[0]
        y1 = brick_coords[1]
        x2 = brick_coords[2]
        y2 = brick_coords[3]

        # we can then get a list of all objects in that area
        results = canvas.find_overlapping(x1, y1, x2, y2)

        # checks whether the ball hits the each brick
        is_hit_this_brick = len(results)
        if is_hit_this_brick > 1:
            color = canvas.itemcget(brick, "fill")
            # if the ball hits the red bricks, red bricks become yellow
            if color == 'red':
                canvas.itemconfig(brick, fill="yellow")
                return True
            # if the ball hits the yellow bricks, yellow bricks become blue
            elif color == 'yellow':
                canvas.itemconfig(brick, fill="blue")
                return True
            # if the ball hits the blue bricks, blue bricks will be deleted from canvas and removed from the bricks list
            elif color == 'blue':
                canvas.delete(brick)
                bricks.remove(brick)
                return True
    return False


def hit_left_wall(canvas, object):
    # returns the condition - ball hits left wall
    return get_left_x(canvas, object) <= 0


def hit_top_wall(canvas, object):
    # returns the condition - ball hits top wall
    return get_top_y(canvas, object) <= 0


def hit_right_wall(canvas, object):
    # returns the condition - ball hits right wall
    return get_right_x(canvas, object) >= CANVAS_WIDTH


def hit_bottom_wall(canvas, object):
    # returns the condition - ball hits bottom wall
    return get_bottom_y(canvas, object) >= CANVAS_HEIGHT


def get_left_x(canvas, object):
    # returns the left x location of the object
    return canvas.coords(object)[0]


def get_top_y(canvas, object):
    # returns the top y location of the object
    return canvas.coords(object)[1]


def get_right_x(canvas, object):
    # returns the right x location of the object
    return canvas.coords(object)[2]


def get_bottom_y(canvas, object):
    # returns the bottom y location of the object
    return canvas.coords(object)[3]


def make_canvas(width, height, title):
    # Creates and returns a drawing canvas of the given int size with a blue border, ready for drawing.
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    # canvas.bind("<Button-1>", mouse_clicked_callback)
    canvas.pack()

    return canvas


def press_space():
    # returns True if player press space
    if keyboard.is_pressed('Space'):
        return True
    else:
        return False


if __name__ == '__main__':
    main()
