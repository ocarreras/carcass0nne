from __future__ import annotations
from engine.placement import Placement


class MonasteryPlacement(Placement):
    def __init__(self, meeple_xy):
        super().__init__(meeple_xy)
        self.completed = False
        self.connections = []
        self.neighbours = 0

    def copy(self):
        my_copy: MonasteryPlacement = super(MonasteryPlacement, self).copy()
        my_copy.__class__ = self.__class__
        my_copy.neighbours = self.neighbours
        my_copy.connections = self.connections
        return my_copy

    def initialize_shape(self, coords, rotation: int, n_players: int, board=None):
        super(MonasteryPlacement, self).initialize_shape(coords, rotation, n_players)
        #self.coords = None

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
