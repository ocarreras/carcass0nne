from __future__ import annotations
from enum import IntEnum
from engine.coords import Coords


class Placement:
    def __init__(self, meeple_xy=[0, 0]):
        self.meeple_xy = meeple_xy
        self.connections = None
        self.meeple = None                  # id of a player or None


class EdgeOrientation(IntEnum):
    U = 0
    R = 1
    D = 2
    L = 3


class Edge:
    def __init__(self, coords: Coords, orientation):
        self.coords: Coords = coords
        self.orientation = orientation

    def opposite(self):
        if self.orientation == EdgeOrientation.U:
            return Edge(self.coords.up(), EdgeOrientation.D)
        if self.orientation == EdgeOrientation.D:
            return Edge(self.coords.down(), EdgeOrientation.U)
        if self.orientation == EdgeOrientation.R:
            return Edge(self.coords.right(), EdgeOrientation.L)
        if self.orientation == EdgeOrientation.L:
            return Edge(self.coords.left(), EdgeOrientation.R)

    def __str__(self):
        return f"EDGE({self.coords}:{self.orientation.name})"

    def __eq__(self, other: Edge):
        return self.coords == other.coords and self.orientation == other.orientation

    def __ne__(self, other: Edge):
        return not(self == other)
