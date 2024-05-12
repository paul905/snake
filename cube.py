class Cube:
    def __init__(self,x,y) -> None:
        self._x = x
        self._y = y
    
    def getX(self):
        return self._x

    def getY(self):
        return self._y
    
    def __eq__(self, other):
        if isinstance(other, Cube):
            return (self._x, self._y) == (other._x, other._y)
        return NotImplemented
    
    def __hash__(self):
        return hash(self._x) + hash(self._y)