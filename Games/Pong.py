from turtle import Turtle, Screen
from random import randint, choice

ballspeed = 8
playerspeed = 50

cursor_size = 20
player_height = 60
player_width = 20

court_width = 1000
court_height = 600

FONT = ("Arial", 44, "normal")

def draw_border():
    border.pensize(3)
    border.penup()
    border.setposition(-court_width/2, court_height/2)
    border.pendown()
    border.forward(court_width)
    border.penup()
    border.sety(-court_height/2)
    border.pendown()
    border.backward(court_width)

def filet():
    border.penup()
    border.pensize(1)
    border.setposition(0, -court_height/2)
    border.setheading(90)
    border.pendown()

    for _ in range(court_height // 50):
        border.forward(50 / 2 + 1)
        border.penup()
        border.forward(50 / 2 + 1)
        border.pendown()

# Player 1 Movement
def up1():
    y = player1.ycor()
    y += playerspeed
    if y < court_height/2 - player_height/2:
        player1.sety(y)

def down1():
    y = player1.ycor()
    y -= playerspeed
    if y > player_height/2 - court_height/2:
        player1.sety(y)

# Player 2 movement
def up2():
    y = player2.ycor()
    y += playerspeed
    if y < court_height/2 - player_height/2:
        player2.sety(y)

def down2():
    y = player2.ycor()
    y -= playerspeed
    if y > player_height/2 - court_height/2:
        player2.sety(y)

def reset_ball():
    ball.setposition(0, 0)
    ball.setheading(choice([0, 180]) + randint(-60, 60))

def distance(t1, t2):
    my_distance = t1.distance(t2)

    if my_distance < player_height/2:
        t2.setheading(180 - t2.heading())
        t2.forward(ballspeed)

# Mainloop
def move():
    global score1, score2

    ball.forward(ballspeed)

    x, y = ball.position()

    if x > court_width/2 + cursor_size: # We define scoring
        score1 += 1
        s1.undo()
        s1.write(score1, font=FONT)
        reset_ball()
    elif x < cursor_size - court_width/2:
        score2 += 1
        s2.undo()
        s2.write(score2, font=FONT)
        reset_ball()
    elif y > court_height/2 - cursor_size or y < cursor_size - court_height/2:
        # We define the border collision
        ball.setheading(-ball.heading())
    else:
        # Check collision between players and ball
        distance(player1, ball)
        distance(player2, ball)

    screen.ontimer(move, 20)

# screen
screen = Screen()
screen.title("Pong")
screen.bgcolor("black")
screen.setup(width=1.0, height=1.0)

# border
border = Turtle(visible=False)
border.speed('fastest')
border.color("white")

draw_border()
filet()

# Ball
ball = Turtle("circle")
ball.color("white")
ball.penup()
ball.speed("fastest")

reset_ball()

# Player 1
player1 = Turtle("square")
player1.turtlesize(player_height / cursor_size, player_width / cursor_size)
player1.color("white")
player1.penup()
player1.setx(cursor_size - court_width/2)
player1.speed("fastest")

# Player 2
player2 = Turtle("square")
player2.shapesize(player_height / cursor_size, player_width / cursor_size)
player2.color("white")
player2.penup()
player2.setx(court_width/2 + cursor_size)
player2.speed("fastest")

# Player 1 score
score1 = 0
s1 = Turtle(visible=False)
s1.speed("fastest")
s1.color("white")
s1.penup()
s1.setposition(-court_width/4, court_height/3)
s1.write(score1, font=FONT)

# Player 2 score"s
score2 = 0
s2 = Turtle(visible=False)
s2.speed("fastest")
s2.color("white")
s2.penup()
s2.setposition(court_width/4, court_height/3)
s2.write(score2, font=FONT)

# We assign s/z to move the player 1
screen.onkey(up1, "s")
screen.onkey(down1, "z")

# We assign up and down arrow to move the player 2
screen.onkey(up2, "Up")
screen.onkey(down2, "Down")

# Restart
screen.onkey(reset_ball, "p")

screen.listen()

move()
screen.mainloop()