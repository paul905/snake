import pygame
import sys
import random
from direction_enum import Direction
from snake import Snake

from time import sleep

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HIEGHT = 600
BLOCK_SIZE = 30

FPS = 10

WHITE = (200,200,200)
SCREEN_COLOR = (0,0,0)

SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HIEGHT))
SCREEN.fill(SCREEN_COLOR)
SCREEN_x, SCREEN_y = SCREEN.get_size()
CLOCK = pygame.time.Clock()

# Game Over text 
font = pygame.font.Font('freesansbold.ttf', 30)
text = font.render('GAME OVER', True, "green", "blue")
textRect = text.get_rect()
textRect.center = (WINDOW_WIDTH // 2, WINDOW_HIEGHT // 2)


# grid    
def showGrid():
    drawGrid(WHITE)

def hideGrid():
    drawGrid(SCREEN_COLOR)

def drawGrid(color):
    grid = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HIEGHT))
    for x in range(0,WINDOW_WIDTH,BLOCK_SIZE):
        for y in range(0,WINDOW_HIEGHT,BLOCK_SIZE):
            rect = pygame.Rect(x,y,BLOCK_SIZE,BLOCK_SIZE)
            pygame.draw.rect(grid,color,rect,1)
    SCREEN.blit(grid,(0,0))

def generate_food(snake: Snake):
    #TODO: food cannot be generated in cells occupided by snake
    snake_body = set(snake.body)
    while True:
        food_x = random.randrange(0,WINDOW_WIDTH-BLOCK_SIZE,BLOCK_SIZE)
        food_y = random.randrange(0,WINDOW_HIEGHT-BLOCK_SIZE,BLOCK_SIZE)
        if not (food_x,food_y) in snake_body:
            break
    
    snake_t = pygame.Rect(food_x,food_y,BLOCK_SIZE,BLOCK_SIZE)
    pygame.draw.rect(SCREEN,"red",snake_t,0,3)
    pygame.display.flip()
    return [food_x,food_y]

# testing purpose 
# show a purple rect in a given cordinates of block_size dimension   
def show_dot(x,y):
    snake_t = pygame.Rect(x,y,BLOCK_SIZE,BLOCK_SIZE)
    pygame.draw.rect(SCREEN,"purple",snake_t,0,3)
    pygame.display.flip()



## CONSOLE
def move_up(snake :Snake):
    if snake.direction == Direction.DOWN :
        move_down(snake)
        return
    if snake.head[1] - BLOCK_SIZE < 0 :
        x = snake.head[0]
        y = SCREEN_y - BLOCK_SIZE
    else:
        x = snake.head[0]
        y = snake.head[1]- BLOCK_SIZE

    draw(snake,x,y)
    snake.direction = Direction.UP
    
def move_down(snake :Snake):
    if snake.direction == Direction.UP:
        move_up(snake)
        return
    if snake.head[1] + BLOCK_SIZE == SCREEN_y :
        x = snake.head[0]
        y = 0
    else:
        x = snake.head[0]
        y = snake.head[1] + BLOCK_SIZE

    draw(snake,x,y)
    snake.direction = Direction.DOWN
    
def move_left(snake :Snake):
    if snake.direction == Direction.RIGHT:
        move_right(snake)
        return
    if snake.head[0] - BLOCK_SIZE < 0 :
        x = SCREEN_x - BLOCK_SIZE
        y = snake.head[1]
    else:
        x = snake.head[0] - BLOCK_SIZE
        y = snake.head[1]

    draw(snake,x,y)
    snake.direction = Direction.LEFT

def move_right(snake :Snake):
    if snake.direction == Direction.LEFT :
        move_left(snake)
        return
    if snake.head[0] + BLOCK_SIZE == SCREEN_x :
        x = 0
        y = snake.head[1]
    else:
        x = snake.head[0] + BLOCK_SIZE
        y = snake.head[1]

    draw(snake,x,y)
    snake.direction = Direction.RIGHT
## CONSOLE

def draw(snake:Snake,x,y):

    # color black tail element
    # remove tail 
    tail_x = snake.tail[0]
    tail_y = snake.tail[1]

    del snake.body[0]
    snake_t = pygame.Rect(tail_x,tail_y,BLOCK_SIZE,BLOCK_SIZE)
    pygame.draw.rect(SCREEN,SCREEN_COLOR,snake_t)
        
    # remove from headadd new element to the body and color it to green
    snake.body.append((x,y))
    snake_h = pygame.Rect(x,y,BLOCK_SIZE,BLOCK_SIZE)
    pygame.draw.rect(SCREEN,"green",snake_h,0,2)

    pygame.display.flip()

    snake.head = snake.body[len(snake.body)-1]
    snake.tail = snake.body[0]


def eat(snake :Snake, move):
     
    x = snake.tail[0]
    y = snake.tail[1]

    # add the new cube on the tail
    if snake.direction == Direction.UP:
        y = y + snake.block_size
    elif snake.direction == Direction.DOWN:
        y = y - snake.block_size
    elif snake.direction == Direction.LEFT:
        x = x + snake.block_size
    elif snake.direction == Direction.RIGHT:
        x = x - snake.block_size

    snake.body.insert(0,(x,y))


def check_game_over(snake :Snake) -> bool:
    return len(set(snake.body)) != len(snake.body)
    

def main():
    snake = Snake(WINDOW_WIDTH,WINDOW_HIEGHT,BLOCK_SIZE)
    running = True
    next_move = move_right
    food_x,food_y = generate_food(snake)
    pause = False
    game_over = False
    gride = False
    

    while running:
       
        CLOCK.tick(FPS)

        if not game_over and not pause:
            next_move(snake)
            game_over = check_game_over(snake)
            if game_over:
                SCREEN.blit(text, textRect)
                pygame.display.flip()
                continue
        
        if food_x == snake.head[0] and food_y == snake.head[1]:
            food_x,food_y = generate_food(snake)
            eat(snake,next_move)
            next_move(snake)
            continue
        
        for event in pygame.event.get():
            
            # quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # keydown
            if not game_over and event.type == pygame.KEYDOWN:
                # arrows
                if event.key == pygame.K_UP:
                    next_move = move_up
                elif event.key == pygame.K_DOWN:
                    next_move = move_down
                elif event.key == pygame.K_LEFT:
                    next_move = move_left
                elif event.key == pygame.K_RIGHT:
                    next_move = move_right
            
                # pause, start, grid
                elif event.key == pygame.K_SPACE:
                    pause = not pause
                elif event.key == pygame.K_g:
                    gride = not gride 
        if gride:
            showGrid()

main()




