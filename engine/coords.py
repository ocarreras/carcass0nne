class Coords:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def up(self):
        return Coords(self.y - 1, self.x)

    def down(self):
        return Coords(self.y + 1, self.x)

    def right(self):
        return Coords(self.y, self.x+1)

    def left(self):
        return Coords(self.y, self.x-1)

    def __str__(self):
        return f"COORD({self.y}, {self.x})"

    ##
    # So we can use it as a key on board{}
    def __hash__(self):
        # TODO: Could be optimized
        return hash((self.y, self.x))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not(self == other)

