"""
Brick Breaker Game
The player must smash a wall of bricks by deflecting a bouncing ball with a paddle.
The paddle may move horizontally and is controlled with the computer's mouse.
The player gets 3 lives to start with; a life is lost if the ball hits the bottom of the screen.
When all the bricks have been destroyed in all levels, the player wins the game.
The game consist of 10 levels.
"""

import tkinter
import time
import keyboard

# How big is the playing area?
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 800

# Constants for the bricks
N_COLS = 10
SPACING = 5
BRICK_START_Y = 100
BRICK_HEIGHT = 20
BRICK_WIDTH = (CANVAS_WIDTH - (N_COLS + 1) * SPACING) / N_COLS

# Constants for the ball and paddle
BALL_SIZE = 40
PADDLE_Y = CANVAS_HEIGHT - 40
PADDLE_WIDTH = 120

CHANGE_X = 10
CHANGE_Y = 10
AVAILABLE_LEVEL_COUNT = 10


def main():
    level = 1
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Brick Breaker')
    totally_failed = play(canvas, level)
    if totally_failed:
        display_text(canvas, "GAME OVER")
    else:
        display_text(canvas, "YOU WIN")
    canvas.update()
    canvas.mainloop()


def play(canvas, level):
    # runs the game until '3 times failing' or 'completing all levels'
    fail_count = 0
    while fail_count < 3 and level <= AVAILABLE_LEVEL_COUNT:
        display_left_life(canvas, fail_count)
        display_level_number(canvas, level)
        failed = play_a_level(canvas, level)
        if failed:
            fail_count += 1
        else:
            level += 1

    return fail_count == 3


def display_left_life(canvas, fail_count):
    # displays the lives left at top-right of the canvas
    left_life_count = 3 - fail_count
    canvas.create_text(500, 50, fill="black", font="ComicSans 20 bold",
                       text="Life: " + str(left_life_count))


def display_level_number(canvas, level):
    # displays the level number at top-left of the canvas
    canvas.create_text(100, 50, fill="black", font="ComicSans 20 bold",
                       text="Level " + str(level))


def tell_player_to_press_space_and_wait(canvas):
    # starts the game
    display_press_space_text(canvas)
    wait_until_player_press_space(canvas)


def play_a_level(canvas, level):
    # creates game elements and starts and ends a level of the game
    bricks = build_bricks(canvas, level, N_COLS, level)
    ball = create_a_ball(canvas)
    paddle = create_paddle(canvas)

    tell_player_to_press_space_and_wait(canvas)
    failed = move_ball_interactively(canvas, ball, paddle, bricks, level)
    tell_player_to_press_space_and_wait(canvas)
    canvas.delete(tkinter.ALL)

    return failed


def build_bricks(canvas, n_rows, n_cols, level):
    # returns and creates bricks
    bricks = []
    for row in range(n_rows):
        for col in range(n_cols):
            a_brick = create_a_brick(canvas, row, col, level)
            bricks.append(a_brick)

    return bricks


def create_a_brick(canvas, row, col, level):
    # creates and returns a brick
    left_x = col * (SPACING + BRICK_WIDTH)
    top_y = BRICK_START_Y + row * (BRICK_HEIGHT + SPACING)
    end_x = left_x + (CANVAS_WIDTH - (N_COLS + 1) * SPACING) / N_COLS
    end_y = top_y + BRICK_HEIGHT
    colour = choose_brick_colour(row, level)
    brick = canvas.create_rectangle(left_x, top_y, end_x, end_y, fill=colour, outline='white')

    return brick


def choose_brick_colour(row, level):
    # returns the colour for bricks according to level and row
    if level == 1 and row == 0:
        return 'blue'
    elif level == 2 and (row == 0 or row == 1):
        return 'blue'
    elif level == 3 and (row == 0 or row == 1 or row == 2):
        return 'blue'
    elif level == 4 and row == 0:
        return 'yellow'
    elif level == 4 and (row == 1 or row == 2 or row == 3):
        return 'blue'
    elif level == 5 and (row == 0 or row == 1):
        return 'yellow'
    elif level == 5 and (row == 2 or row == 3 or row == 4):
        return 'blue'
    elif level == 6 and (row == 0 or row == 1 or row == 2):
        return 'yellow'
    elif level == 6 and (row == 3 or row == 4 or row == 5):
        return 'blue'
    elif level == 7 and row == 0:
        return 'purple'
    elif level == 7 and (row == 1 or row == 2 or row == 3):
        return 'yellow'
    elif level == 7 and (row == 4 or row == 5 or row == 6):
        return 'blue'
    elif level == 8 and (row == 0 or row == 1):
        return 'purple'
    elif level == 8 and (row == 2 or row == 3 or row == 4):
        return 'yellow'
    elif level == 8 and (row == 5 or row == 6 or row == 7):
        return 'blue'
    elif level == 9 and (row == 0 or row == 1 or row == 2):
        return 'purple'
    elif level == 9 and (row == 3 or row == 4 or row == 5):
        return 'yellow'
    elif level == 9 and (row == 6 or row == 7 or row == 8):
        return 'blue'
    elif level == 10 and row == 0:
        return 'red'
    elif level == 10 and (row == 1 or row == 2 or row == 3):
        return 'purple'
    elif level == 10 and (row == 4 or row == 5 or row == 6):
        return 'yellow'
    elif level == 10 and (row == 7 or row == 8 or row == 9):
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


def display_press_space_text(canvas):
    # displays to player the text on how to start the game
    press_space_text = canvas.create_text(300, 500, fill="black", font="ComicSans 20 bold",
                                          text="Press 'space' to start")
    canvas.update()
    canvas.delete(press_space_text)


def wait_until_player_press_space(canvas):
    # game stops until player press space
    while not space_pressed():
        time.sleep(1 / 10)


def move_ball_interactively(canvas, ball, paddle, bricks, level):
    # changes the direction of ball in case of hitting a wall or paddle and returns fail
    dx, dy = pace_of_ball(level)
    failed = False

    while True:
        move_paddle(canvas, paddle)
        canvas.move(ball, dx, dy)

        if ball_hits_left_wall(canvas, ball) or ball_hits_right_wall(canvas, ball):
            dx *= -1
        elif ball_hits_top_wall(canvas, ball):
            dy *= -1
        elif ball_hits_canvas_object(canvas, paddle):
            dx, dy = bounce_ball_when_hits_paddle(canvas, ball, paddle, dx, dy)
        elif ball_hits_bricks(canvas, bricks):
            dy *= -1
        elif is_ball_lower_than_paddle(canvas, ball, paddle):
            failed = True
            break
        elif len(bricks) == 0:  # if ball hits all bricks and there are no more bricks
            break

        canvas.update()         # redraw canvas
        time.sleep(1 / 50.)       # pause

    return failed


def move_paddle(canvas, paddle):
    # moves paddle according to mouse movement
    mouse_x = canvas.winfo_pointerx()
    paddle_left_x = min(mouse_x, CANVAS_WIDTH - PADDLE_WIDTH)
    canvas.moveto(paddle, paddle_left_x, PADDLE_Y)


def pace_of_ball(level):
    # calculates and returns the speed of ball according to levels
    if level == 1 or level == 2 or level == 3:
        dx = CHANGE_X * 0.75
        dy = CHANGE_Y * 0.75
    elif level == 4 or level == 5 or level == 6 or level == 7:
        dx = CHANGE_X
        dy = CHANGE_Y
    else:
        dx = CHANGE_X * 1.25
        dy = CHANGE_Y * 1.25

    return dx, dy


def display_text(canvas, message):
    # display the text in the middle of the canvas such as 'game over', 'you win'
    canvas.create_text(300, 500, fill="red", font="ComicSans 30 bold",
                       text=message)


def is_ball_lower_than_paddle(canvas, ball, paddle):
    # returns the condition - ball is lower than paddle
    return get_bottom_y(canvas, ball) > get_top_y(canvas, paddle)


def ball_hits_canvas_object(canvas, canvas_object):
    # this graphics method gets the location of the paddle as a list
    canvas_object_coords = canvas.coords(canvas_object)

    # the list has four elements:
    x1 = canvas_object_coords[0]
    y1 = canvas_object_coords[1]
    x2 = canvas_object_coords[2]
    y2 = canvas_object_coords[3]

    # we get a list of all objects in that area
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


def ball_hits_bricks(canvas, bricks):
    # changes colour or delete the bricks when the ball hits the bricks
    for brick in bricks:
        is_hit_this_brick = ball_hits_canvas_object(canvas, brick)

        if is_hit_this_brick:
            color = canvas.itemcget(brick, "fill")
            if color == 'red':
                canvas.itemconfig(brick, fill="purple")
            elif color == 'purple':
                canvas.itemconfig(brick, fill="yellow")
            elif color == 'yellow':
                canvas.itemconfig(brick, fill="blue")
            elif color == 'blue':
                canvas.delete(brick)
                bricks.remove(brick)

            return True

    return False


def ball_hits_left_wall(canvas, canvas_object):
    # returns the condition - ball hits left wall
    return get_left_x(canvas, canvas_object) <= 0


def ball_hits_top_wall(canvas, canvas_object):
    # returns the condition - ball hits top wall
    return get_top_y(canvas, canvas_object) <= 0


def ball_hits_right_wall(canvas, canvas_object):
    # returns the condition - ball hits right wall
    return get_right_x(canvas, canvas_object) >= CANVAS_WIDTH


def get_left_x(canvas, canvas_object):
    # returns the left x location of the object
    return canvas.coords(canvas_object)[0]


def get_top_y(canvas, canvas_object):
    # returns the top y location of the object
    return canvas.coords(canvas_object)[1]


def get_right_x(canvas, canvas_object):
    # returns the right x location of the object
    return canvas.coords(canvas_object)[2]


def get_bottom_y(canvas, canvas_object):
    # returns the bottom y location of the object
    return canvas.coords(canvas_object)[3]


def make_canvas(width, height, title):
    # Creates and returns a drawing canvas of the given int size with a blue border, ready for drawing.
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()

    return canvas


def space_pressed():
    # returns True if player press space
    return keyboard.is_pressed('Space')


if __name__ == '__main__':
    main()
