from pydantic import BaseModel


class Position(BaseModel):
    x: int
    y: int

    class Config:
        frozen = True

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, tup):
        if isinstance(tup, tuple):
            return Position(x=self.x + tup[0], y=self.y + tup[1])
        return NotImplemented

    def __mul__(self, scalar):
        if isinstance(scalar, int):
            return Position(x=self.x * scalar, y=self.y * scalar)
        return NotImplemented

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y