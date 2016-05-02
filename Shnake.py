import pygame
import time
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Shnake")


FPS = 12
block_size = 20

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 25)

def score(score):
    text = font.render("Score: " + str(score), True , BLACK)
    gameDisplay.blit(text, [10, 10])

def snake(snakeList):
    for XandY in snakeList:

        gameDisplay.fill (GREEN, rect=[XandY[0], XandY[1], block_size, block_size])

def text_objs(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message(message , color):
    #Print message in colors color with AntiAliasing(Sp? lol)
    screen_text = font.render(message, True, color)
    gameDisplay.blit(screen_text, [display_width / 2 - screen_text.get_width() / 2, display_height / 2 - screen_text.get_height() / 2])

def gameLoop():
    gameExit = False
    gameOver = False

    parent_x = display_width / 2
    parent_y = display_height / 2
    parent_x_change = block_size
    parent_y_change = 0

    randFoodX = random.randrange(0, (display_width - block_size), block_size)
    randFoodY = random.randrange(0, (display_height - block_size), block_size)

    snakeList = []
    snakeLength = 1

    last_move = 'right'

    while not gameExit:
        while gameOver == True:
            gameDisplay.fill(WHITE)
            message("Game over, press esc to quit or space to play again", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        gameLoop()
                    elif event.key == pygame.K_ESCAPE:
                        gameExit = True
                        gameOver = False


        for event in pygame.event.get():
            if (event.type) == pygame.QUIT:
                gameExit = True
            if (event.type) == pygame.KEYDOWN:
                #Move Left
                if event.key == pygame.K_LEFT and ( last_move != 'right'):
                    parent_x_change = -(block_size)
                    parent_y_change = 0
                    last_move = 'left'

                #Move Right
                elif event.key == pygame.K_RIGHT and last_move != 'left':
                    parent_x_change = block_size
                    parent_y_change = 0
                    last_move = 'right'
                #Move Up
                elif event.key == pygame.K_UP and last_move != 'down':
                    parent_y_change = -(block_size)
                    parent_x_change = 0
                    last_move = 'up'
                #Move Down
                elif event.key == pygame.K_DOWN and last_move != 'up':
                    parent_y_change = block_size
                    parent_x_change = 0
                    last_move = 'down'

                #Quit Game
                if event.key == pygame.K_ESCAPE:
                    gameExit = True

        #Checks if you exit the game boundary
        if parent_x >= display_width or parent_x < 0 or parent_y >= display_height or parent_y < 0:
            gameOver = True


        #Changes position based on last pressed direction key (Sums position with speed (rate of change of state))
        parent_x += parent_x_change
        parent_y += parent_y_change

        #Sets background to white
        gameDisplay.fill(WHITE)
        pygame.draw.rect(gameDisplay, RED, [randFoodX , randFoodY, block_size, block_size])


        #pygame.draw.rect(gameDisplay, GREEN, [parent_x, parent_y, snake_size, snake_size])
        #params = (display layer, color, top left position (x,y), width, height)

        #Clear snakehead coords because there is now a new head
        snakeHead = []
        snakeHead.append(parent_x)
        snakeHead.append(parent_y)
        #Set new snakehead coords
        snakeList.append(snakeHead)

        #Delete oldest element to limit snake length
        if len(snakeList) > snakeLength:
            del snakeList[0]

        #Check every element in the snakelist up to the last (because this is the head) Otherwise snakehead pos == snakehead pos
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(snakeList)

        score(snakeLength - 1)

        pygame.display.update()

        #If you collide with food
        if parent_x == randFoodX and parent_y == randFoodY:
            #Generate new food at random position
            randFoodX = random.randrange(0, (display_width - block_size), block_size)
            randFoodY = random.randrange(0, (display_height - block_size), block_size)

            snakeLength += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

gameLoop()