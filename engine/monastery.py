from engine.placement import Placement
from engine.coords import Coords


class MonasteryPlacement(Placement):
    def __init__(self, meeple_xy):
        super().__init__(meeple_xy)
        self.completed = False
        self.score = 0

    def initialize(self, board, coords: Coords):
        if coords.up() in board:
            self.score += 1
        if coords.up().left() in board:
            self.score += 1
        if coords.up().right() in board:
            self.score += 1
        if coords.left() in board:
            self.score += 1
        if coords.right() in board:
            self.score += 1
        if coords.down() in board:
            self.score += 1
        if coords.down().left() in board:
            self.score += 1
        if coords.down().right() in board:
            self.score += 1
        if self.score == 8:
            self.completed = True

    def inc_score(self):
        self.score += 1
        if self.score == 8:
            self.completed = True

    def __str__(self):
        return f"Monastery S:{self.score} M:{self.meeple}"