from __future__ import annotations
from engine.placement import Placement
from engine.coords import Coords
from engine.shape import Shape


class Monastery(Shape):
    def __init__(self, placement: MonasteryPlacement, coords, n_players):
        super().__init__(placement, coords, n_players)
        self.neighbours = 0

    def initialize(self, board, coords: Coords):
        if coords.up() in board:
            self.neighbours += 1
        if coords.up().left() in board:
            self.neighbours += 1
        if coords.up().right() in board:
            self.neighbours += 1
        if coords.left() in board:
            self.neighbours += 1
        if coords.right() in board:
            self.neighbours += 1
        if coords.down() in board:
            self.neighbours += 1
        if coords.down().left() in board:
            self.neighbours += 1
        if coords.down().right() in board:
            self.neighbours += 1
        if self.neighbours == 8:
            self.completed = True

    def inc_neighbours(self):
        self.neighbours += 1
        if self.neighbours == 8:
            self.completed = True

    def score(self):
        return self.neighbours + 1

    def __str__(self):
        return f"MONASTERY {hex(id(self))} {self.coords} #{self.neighbours:02d} " + \
               ("COMPLETED" if self.completed else "OPEN")

    def print(self):
        print(self)


class MonasteryPlacement(Placement):
    def __init__(self, meeple_xy):
        super().__init__(meeple_xy)
        self.completed = False
        self.shape = None
        self.connections = []

    def __str__(self):
        if self.shape:
            return f"Monastery S:{self.shape.neighbours} M:{self.meeple}"
        else:
            return f"Monastery"

    def copy(self):
        my_copy: MonasteryPlacement = super(MonasteryPlacement, self).copy()
        my_copy.__class__ = self.__class__
        return my_copy
