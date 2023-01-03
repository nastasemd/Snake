import pygame as pg
import os
import numpy as np
import random

Path = os.path.dirname(os.path.abspath(__file__))

# Initializing
pg.init()
screen = pg.display.set_mode((1000, 1000))
BG = (60, 120, 250)
screen.fill(BG)

# Title, icon and images
pg.display.set_caption("Snake")
icon = pg.image.load(os.path.join(Path, 'images\icon.png'))
pg.display.set_icon(icon)

board = pg.image.load(os.path.join(Path, 'images\\board.png'))
headImg = pg.image.load(os.path.join(Path, 'images\head.png'))
bodyImg = pg.image.load(os.path.join(Path, 'images\\body.png'))
tailImg = pg.image.load(os.path.join(Path, 'images\\tail.png'))
apple = pg.image.load(os.path.join(Path, 'images\\apple.png'))
cornerDownLeft = pg.image.load(os.path.join(Path, 'images\cornerdownleft.png'))
cornerDownRight = pg.image.load(os.path.join(Path, 'images\cornerdownright.png'))
cornerUpLeft = pg.image.load(os.path.join(Path, 'images\cornerupleft.png'))
cornerUpRight = pg.image.load(os.path.join(Path, 'images\cornerupright.png'))

possiblePositions = []
possibleRotations = [0, 90, 180, 270]
for i in range(100, 400, 31):
    possiblePositions.append(i)

def getRandomPosition(possiblePositions):
    x = random.choice(possiblePositions)
    y = random.choice(possiblePositions)
    return (x,y)

def getRandomRotation(possibleRotations):
    return random.choice(possibleRotations)

def randomTailStartingPosition(head):
    options = [ (0, 31), (31, 0), (0, -31), (-31, 0)] # adds tail below, to the right, above, to the left of head
    i = random.randint(0, len(options) - 1)
    while (head[0] + options[i][0] < 100 or head[0] + options[i][0] > 379 or head[1] + options[i][1] < 100 or head[1] + options[i][1] > 379):
        options.pop(i)
        i = random.randint(0, len(options) - 1)
    return (head[0] + options[i][0], head[1] + options[i][1])

def generateStartingSnake(possiblePositions, possibleRotations):
    snake = []
    snakeRotations = []
    snakeRect = []
    while True:
        startingHeadPosition = getRandomPosition(possiblePositions)
        rotation = getRandomRotation(possibleRotations)
        i = possibleRotations.index(rotation)
        tailOptions = [(0, 31), (31, 0), (0, -31), (-31, 0)] # adds tail below, to the right, above, to the left of head
        if (startingHeadPosition[0] + tailOptions[i][0] >= 100 and startingHeadPosition[0] + tailOptions[i][0] <= 379 and startingHeadPosition[1] + tailOptions[i][1] >= 100
        and startingHeadPosition[1] + tailOptions[i][1] <= 379):
            tail = (startingHeadPosition[0] + tailOptions[i][0], startingHeadPosition[1] + tailOptions[i][1])
            snake.append(tail)
            snake.append(startingHeadPosition)
            snakeRotations.append(rotation)
            snakeRotations.append(rotation)
            break
    for x in snake:
        snakeRect.append(pg.Rect(x[0], x[1], 31, 31))
    return snake, snakeRotations, snakeRect
snake, snakeRotations, snakeRect = generateStartingSnake(possiblePositions, possibleRotations)

def getNewApple(snake, possiblePositions):
    pos = getRandomPosition(possiblePositions)
    while pos in snake:
        pos = getRandomPosition(possiblePositions)
    appleRect = pg.Rect(pos[0], pos[1], 31, 31)
    return pos, appleRect

def drawBoard(snake, snakeRotations):
    screen.blit(board, (100,100))
    screen.blit(pg.transform.rotate(headImg, snakeRotations[-1]), snake[-1]) # head
    screen.blit(pg.transform.rotate(tailImg, snakeRotations[0]), snake[0]) # tail
    screen.blit(apple, applePos)
    for i in range (1, len(snake) - 1):
        #corners
        if(snakeRotations[i-1] == 0 and snakeRotations[i+1] == 90):
            screen.blit(cornerUpLeft, snake[i])
        elif(snakeRotations[i-1] == 0 and snakeRotations[i+1] == 270):
            screen.blit(cornerUpRight, snake[i])
        elif(snakeRotations[i-1] == 180 and snakeRotations[i+1] == 90):
            screen.blit(cornerDownLeft, snake[i])
        elif(snakeRotations[i-1] == 180 and snakeRotations[i+1] == 270):
            screen.blit(cornerDownRight, snake[i])
        else:
            screen.blit(pg.transform.rotate(bodyImg, snakeRotations[i]), snake[i]) #normal bodypart

# Game logic
applePos, appleRect = getNewApple(snake, possiblePositions)
clock = pg.time.Clock()
gameOver = False
score = 0

def changePositions(snake, snakeRotations, snakeRect, possibleRotations, rotation):
    options = [(0, -31), (-31, 0), (0, 31), (31, 0)]
    x = possibleRotations.index(rotation)
    oldTail = snake[0]
    oldTailRotation = snakeRotations[0]
    if (snake[-1][0] + options[x][0] >= 100 and snake[-1][0] + options[x][0] <= 379 and snake[-1][1] + options[x][1] >= 100 and snake[-1][1] + options[x][1] <= 379):
        for i in range(len(snake) - 1):
            snake[i] = snake[i+1]
            snakeRotations[i] = snakeRotations[i+1]
            snakeRect[i] = snakeRect[i+1]
        snake.pop(-1)
        newHead = (snake[-1][0] + options[x][0], snake[-1][1] + options[x][1])
        snake.append(newHead)
        snakeRotations.pop(-1)
        snakeRotations.append(rotation)
        snakeRect.pop(-1)
        snakeRect.append(pg.Rect(newHead[0], newHead[1], 31, 31))
        if len(snake) == 2:
            snakeRotations[0] = snakeRotations[1]
    return snake, snakeRotations, snakeRect, oldTail, oldTailRotation

def addSnakePart(snake, snakeRotations, snakeRect, applePos):    
    newHead = applePos
    snake.append(newHead)
    snakeRotations.append(snakeRotations[-1])
    snakeRect.append(pg.Rect(newHead[0], newHead[1], 31, 31))
    return snake, snakeRotations, snakeRect

direction = None
# Game loop
running = True
oldTail = None
oldTailRotation = None

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                if direction != 180 and snake[-1][1] - 31 >= 100:
                    direction = 0
            if event.key == pg.K_LEFT:
                if direction != 270 and snake[-1][0] - 31 >= 100:
                    direction = 90
            if event.key == pg.K_DOWN:
                if direction != 0 and snake[-1][1] + 31 <= 379:
                    direction = 180
            if event.key == pg.K_RIGHT:
                if direction != 90 and snake[-1][0] + 31 <= 379:
                    direction = 270
    if gameOver == False:
        for x in snakeRect:
            if(x.colliderect(appleRect)):
                snake.insert(0, oldTail)
                snakeRotations.insert(0, oldTailRotation)
                snakeRect.insert(0, pg.Rect(oldTail[0], oldTail[1], 31,31))
                # snake, snakeRotations, snakeRect = addSnakePart(snake, snakeRotations, snakeRect, applePos)
                applePos, appleRect = getNewApple(snake, possiblePositions)
                screen.fill(BG)
                drawBoard(snake, snakeRotations)
                pg.display.update()
        for i in range(len(snakeRect) -1):
            for j in range(i + 1, len(snakeRect)):
                if snakeRect[i].colliderect(snakeRect[j]):
                    gameOver = True
                    print('Game over!')
        if direction != None and gameOver == False:
            snake, snakeRotations, snakeRect, oldTail, oldTailRotation = changePositions(snake, snakeRotations, snakeRect, possibleRotations, direction)
    screen.fill(BG)
    drawBoard(snake, snakeRotations)
    pg.display.update()
    clock.tick(1)
    