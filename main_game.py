import pygame
import sys
import random
from direction_enum import Direction as direction

from time import sleep

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HIEGHT = 600
BLOCK_SIZE = 30

WHITE = (200,200,200)
BLACK = (0,0,0)

SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HIEGHT))
SCREEN.fill(BLACK)
SCREEN_x, SCREEN_y = SCREEN.get_size()
CLOCK = pygame.time.Clock()
CLOCK.tick(60)

class Cube:
    def __init__(self,x,y) -> None:
        self.__x = x
        self.__y = y
    
    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

class Snake:

    def __init__(self) -> None:
        self.body = [Cube(WINDOW_WIDTH/2,WINDOW_HIEGHT/2)]
        self.head = self.body[0]
        self.tail = self.body[0]
        self.dim = 1
        self.direction = direction.RIGHT

    def move_up(self):
        if self.dim > 1 and self.direction == direction.DOWN :
                    self.move_down()
                    return
        if self.head.getY() - BLOCK_SIZE < 0 :
            x = self.head.getX()
            y = SCREEN_y - BLOCK_SIZE
        else:
            x = self.head.getX()
            y = self.head.getY() - BLOCK_SIZE

        self.body.append(Cube(x,y))
        self.direction = direction.UP
    
    def move_down(self):
        if self.dim > 1 and self.direction == direction.UP:
                    self.move_up()
                    return
        if self.head.getY() + BLOCK_SIZE == SCREEN_y :
            x = self.head.getX()
            y = 0
        else:
            x = self.head.getX()
            y = self.head.getY() + BLOCK_SIZE

        self.body.append(Cube(x,y))
        self.direction = direction.DOWN
    
    def move_left(self):
        if self.dim > 1 and self.direction == direction.RIGHT:
                    self.move_right()
                    return
        if self.head.getX() - BLOCK_SIZE < 0 :
            x = SCREEN_x - BLOCK_SIZE
            y = self.head.getY()
        else:
            x = self.head.getX() - BLOCK_SIZE
            y = self.head.getY()

        self.body.append(Cube(x,y))
        self.direction = direction.LEFT

    def move_right(self):
        if self.dim > 1 and self.direction == direction.LEFT :
                    self.move_left()
                    return
        if self.head.getX() + BLOCK_SIZE == SCREEN_x :
            x = 0
            y = self.head.getY()
        else:
            x = self.head.getX() + BLOCK_SIZE
            y = self.head.getY()

        self.body.append(Cube(x,y))
        self.direction = direction.RIGHT  

    def start(self):
        self.move_up()
            
    def eat(self):
            x = self.head.getX()
            y = self.head.getY()

            if self.direction == direction.UP:
                y = y - BLOCK_SIZE
            if self.direction == direction.DOWN:
                y = y + BLOCK_SIZE
            if self.direction == direction.LEFT:
                x = x - BLOCK_SIZE
            if self.direction == direction.RIGHT:
                x = x + BLOCK_SIZE

            self.body.append(Cube(x,y))
            self.dim = self.dim +1

def draw(snake :Snake):
    snake.head = snake.body[len(snake.body)-1]
    snake.tail = snake.body[0]
                
    if len(snake.body)>1:
        # remove tail 
        tail_x = snake.tail.getX()
        tail_y = snake.tail.getY()
        snake.body.remove(snake.tail)
        snake_t = pygame.Rect(tail_x,tail_y,BLOCK_SIZE,BLOCK_SIZE)
        pygame.draw.rect(SCREEN,"black",snake_t)
        # pygame.display.flip()

        # draw head
        for cube in snake.body:
            snake_h = pygame.Rect(cube.getX(),cube.getY(),BLOCK_SIZE,BLOCK_SIZE)
            pygame.draw.rect(SCREEN,"green",snake_h,0,2)

    pygame.display.flip()

# grid    
def showGrid():
    drawGrid(WHITE)

def hideGrid():
    drawGrid(BLACK)

def drawGrid(color):
    for x in range(0,WINDOW_WIDTH,BLOCK_SIZE):
        for y in range(0,WINDOW_HIEGHT,BLOCK_SIZE):
            rect = pygame.Rect(x,y,BLOCK_SIZE,BLOCK_SIZE)
            pygame.draw.rect(SCREEN,color,rect,1)




def generate_food():
    #TODO: food cannot be generated in cells occupided by snake 
    food_x = random.randrange(0,WINDOW_WIDTH-BLOCK_SIZE,BLOCK_SIZE)
    food_y = random.randrange(0,WINDOW_HIEGHT-BLOCK_SIZE,BLOCK_SIZE)
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

def main():
    snake = Snake()
    running = True
    food_x,food_y = generate_food()
    next_move = snake.move_right
    gride = False

    while True:
        if running: 
            next_move()

            # TODO: GAME OVER check

            if food_x == snake.head.getX() and food_y == snake.head.getY():
                 food_x,food_y = generate_food()
                 snake.eat()
                 next_move()
                 pygame.display.flip()
        
        for event in pygame.event.get():
            # keydown
            if event.type == pygame.KEYDOWN:
                # arrows
                if event.key == pygame.K_UP:
                    next_move = snake.move_up
                elif event.key == pygame.K_DOWN:
                    next_move = snake.move_down
                elif event.key == pygame.K_LEFT:
                    next_move = snake.move_left
                elif event.key == pygame.K_RIGHT:
                    next_move = snake.move_right

                # space
                elif event.key == pygame.K_SPACE:
                    snake.eat()
                    next_move()
                
                # pause, start, grid
                elif event.key == pygame.K_p:
                    running = False
                elif event.key == pygame.K_s:
                    running = True
                elif event.key == pygame.K_g:
                    if gride:
                        hideGrid()
                        gride = False
                    else:
                         showGrid()
                         gride = True
                if not running :
                    break

            # quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        if running:     
            draw(snake)
            pygame.display.flip()

        sleep(0.12)


main()




