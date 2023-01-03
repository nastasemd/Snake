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

possiblePositions = []
possibleRotations = [0, 90, 180, 270]
for i in range(100, 400, 31):
    possiblePositions.append(i)
print(possiblePositions)
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
    return snake, snakeRotations
snake, snakeRotations = generateStartingSnake(possiblePositions, possibleRotations)
def drawBoard():
    screen.blit(board, (100,100))
    screen.blit(pg.transform.rotate(headImg, snakeRotations[-1]), snake[-1])
    screen.blit(pg.transform.rotate(tailImg, snakeRotations[-2]), snake[-2])

# Game logic
clock = pg.time.Clock()
gameOver = False
score = 0

def changePositions(snake, snakeRotations, possibleRotations, rotation):
    options = [(0, -31), (-31, 0), (0, 31), (31, 0)]
    x = possibleRotations.index(rotation)
    if (snake[-1][0] + options[x][0] >= 100 and snake[-1][0] + options[x][0] <= 379 and snake[-1][1] + options[x][1] >= 100 and snake[-1][1] + options[x][1] <= 379):
        for i in range(len(snake) - 1):
            snake[i] = snake[i+1]
            snakeRotations[i] = snakeRotations[i+1]
        snake.pop(-1)
        newHead = (snake[-1][0] + options[x][0], snake[-1][1] + options[x][1])
        snake.append(newHead)
        snakeRotations.pop(-1)
        snakeRotations.append(rotation)
        if len(snake) == 2:
            snakeRotations[0] = snakeRotations[1]
    return snake, snakeRotations
    
direction = None
# Game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                if direction != 180:
                    direction = 0
            if event.key == pg.K_LEFT:
                if direction != 270:
                    direction = 90
            if event.key == pg.K_DOWN:
                if direction != 0:
                    direction = 180
            if event.key == pg.K_RIGHT:
                if direction != 90:
                    direction = 270
    if direction != None:
        snake, snakeRotations = changePositions(snake, snakeRotations, possibleRotations, direction)
    screen.fill(BG)
    drawBoard()
    pg.display.update()
    clock.tick(3)
    