from direction_enum import Direction

class Snake:

    def __init__(self,WINDOW_WIDTH,WINDOW_HIEGHT,BLOCK_SIZE) -> None:
        self.body = [(WINDOW_WIDTH/2,WINDOW_HIEGHT/2)]
        self.head = self.body[0]
        self.tail = self.body[len(self.body)-1]
        self.dim = 1
        self.block_size = BLOCK_SIZE
        self.direction = Direction.RIGHT


    