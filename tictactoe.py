import turtle
import random

# Screen setup
sc = turtle.Screen()
sc.setup(800, 800)
sc.bgcolor("black")
sc.title("Tic Tac Toe 5x5")
sc.tracer(0)

# Globals
l = 500  # board size
cell = l / 5
nx, rx = -l / 2, l / 2
ty, by = l / 2, -l / 2

game_mode = None
current_player = "X"
gameOver = False
draw = False

# Turtles
drawer = turtle.Turtle()
drawer.ht()
drawer.color("white")
drawer.width(3)

a = turtle.Turtle()
a.ht()
a.pu()
a.color("yellow")

ref = turtle.Turtle()
ref.ht()
ref.color("blue")

button_t = turtle.Turtle()
button_t.ht()
button_t.pu()

winLiner = turtle.Turtle()
winLiner.ht()
winLiner.width(6)

boardStatus = [""] * 25
boxCoords = []

# Generate coordinates for each box (top-left corners)
for row in range(5):
    for col in range(5):
        boxCoords.append((nx + col * cell, ty - row * cell))

# --- Draw board ---
def drawBoard():
    drawer.clear()
    for i in range(6):
        # horizontal lines
        drawer.pu()
        drawer.goto(nx, ty - i * cell)
        drawer.pd()
        drawer.goto(rx, ty - i * cell)

        # vertical lines
        drawer.pu()
        drawer.goto(nx + i * cell, ty)
        drawer.pd()
        drawer.goto(nx + i * cell, by)
    sc.update()

# --- Buttons ---
def createButton(x, y, width, height, label):
    button_t.color("white")
    button_t.goto(x, y)
    button_t.pd()
    button_t.begin_fill()
    button_t.fillcolor("gray20")
    for _ in range(2):
        button_t.fd(width)
        button_t.rt(90)
        button_t.fd(height)
        button_t.rt(90)
    button_t.end_fill()
    button_t.pu()
    button_t.color("yellow")
    button_t.goto(x + width / 2, y - height / 1.5)
    button_t.write(label, align="center", font=("Arial", 14, "bold"))
    sc.update()

def clearButtons():
    button_t.clear()

# --- Start Menu ---
def showStartMenu():
    clearButtons()
    ref.clear()
    ref.goto(0, 200)
    ref.write("Tic Tac Toe 5x5", align="center", font=("Magneto", 28, "bold"))
    createButton(-100, 50, 200, 50, "Play vs Computer")
    createButton(-100, -50, 200, 50, "Play vs Human")

def startGame(mode):
    global game_mode, boardStatus, current_player, gameOver, draw
    game_mode = mode
    clearButtons()
    ref.clear()
    a.clear()
    winLiner.clear()
    drawBoard()
    boardStatus = [""] * 25
    current_player = "X"
    gameOver = draw = False
    ref.goto(0, ty + 30)
    ref.write(f"Current Turn: {current_player}", align="center", font=("Magneto", 24, "normal"))
    createButton(-100, -350, 200, 40, "Restart")

def restart():
    if game_mode:
        startGame(game_mode)

# --- Game Logic ---
def drawLine(startBox, endBox):
    winLiner.color("white")
    winLiner.pu()
    winLiner.goto(boxCoords[startBox][0] + cell / 2, boxCoords[startBox][1] - cell / 2)
    winLiner.pd()
    winLiner.goto(boxCoords[endBox][0] + cell / 2, boxCoords[endBox][1] - cell / 2)
    sc.update()

def checkWinner():
    global draw
    lines = []

    # Rows
    for i in range(0, 25, 5):
        lines.append(range(i, i + 5))
    # Columns
    for i in range(5):
        lines.append(range(i, 25, 5))
    # Diagonals
    lines.append(range(0, 25, 6))
    lines.append(range(4, 21, 4))

    for line in lines:
        if all(boardStatus[i] == current_player for i in line):
            drawLine(line[0], line[-1])
            return True

    if "" not in boardStatus:
        draw = True
    return False

def stamp(boxNo):
    global current_player, gameOver, draw
    if boardStatus[boxNo] == "" and not gameOver:
        a.goto(boxCoords[boxNo][0] + cell / 3, boxCoords[boxNo][1] - cell * 0.75)
        a.write(current_player, font=("Arial Black", 24, "normal"))
        boardStatus[boxNo] = current_player

        if checkWinner():
            ref.clear()
            ref.write(f"{current_player} Wins!", align="center", font=("Magneto", 24, "normal"))
            gameOver = True
            return
        elif draw:
            ref.clear()
            ref.write("Draw!", align="center", font=("Magneto", 24, "normal"))
            gameOver = True
            return

        current_player = "O" if current_player == "X" else "X"
        ref.clear()
        ref.write(f"Current Turn: {current_player}", align="center", font=("Magneto", 24, "normal"))
        if game_mode == "computer" and current_player == "O":
            sc.ontimer(playComputer, 400)

def playComputer():
    if gameOver:
        return
    empty = [i for i, v in enumerate(boardStatus) if v == ""]
    if empty:
        stamp(random.choice(empty))

def clickHandler(x, y):
    global game_mode
    # Menu buttons
    if -100 < x < 100 and 50 > y > 0:
        startGame("computer")
    elif -100 < x < 100 and -50 > y > -100:
        startGame("human")
    elif -100 < x < 100 and -350 > y > -390:
        restart()
    else:
        if game_mode:
            for i in range(25):
                bx, byy = boxCoords[i]
                if bx < x < bx + cell and byy - cell < y < byy:
                    if game_mode == "human" or (game_mode == "computer" and current_player == "X"):
                        stamp(i)

# --- Run ---
showStartMenu()
sc.onclick(clickHandler)
sc.listen()
sc.mainloop()
