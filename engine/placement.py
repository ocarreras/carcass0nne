from __future__ import annotations
from enum import IntEnum
from engine.coords import Coords
import copy


class Placement:
    def __init__(self, meeple_xy=[0, 0]):
        self.meeple_xy = meeple_xy
        self.connections = None
        self.meeple = None                  # id of a player or None
        self.shape = None
        self.completed = False

    def initialize(self, rotation: int):
        self.connections = list(map(lambda c: EdgeConnection((c + rotation * 2) % 8), self.connections))

    def copy(self):
        my_copy: Placement = Placement()
        my_copy.meeple_xy = self.meeple_xy.copy()
        my_copy.connections = self.connections.copy()
        my_copy.meeple = self.meeple
        my_copy.shape = self.shape
        my_copy.completed = self.completed
        return my_copy


    ##
    # Uggly!
    #
    # Duplicate connections for city/roads so we can use the same connectivity functions.
    # We initially only set LD/DL/UL/RU and we need to add the other parities to keep connectivity.
    def duplicate_connections(self):
        new_connections = copy.copy(self.connections)
        for connection in self.connections:
            if connection == EdgeConnection.LD:
                new_connections.append(EdgeConnection.LU)
            if connection == EdgeConnection.DL:
                new_connections.append(EdgeConnection.DR)
            if connection == EdgeConnection.UL:
                new_connections.append(EdgeConnection.UR)
            if connection == EdgeConnection.RU:
                new_connections.append(EdgeConnection.RD)
        self.connections = new_connections

class BorderOrientation(IntEnum):
    U = 0
    R = 1
    D = 2
    L = 3


class EdgeConnection(IntEnum):
    UL = 0
    UR = 1
    RU = 2
    RD = 3
    DR = 4
    DL = 5
    LD = 6
    LU = 7
    U = UL
    D = DL
    R = RU
    L = LD


class Edge:
    def __init__(self, coords: Coords, connection: EdgeConnection):
        self.coords: Coords = coords
        self.connection = connection

    def opposite(self):
        if self.connection == EdgeConnection.UL or self.connection == EdgeConnection.UR:
            return Edge(self.coords.up(), EdgeConnection((self.connection + 4) % 8))
        if self.connection == EdgeConnection.DL or self.connection == EdgeConnection.DR:
            return Edge(self.coords.down(), EdgeConnection((self.connection + 4) % 8))
        if self.connection == EdgeConnection.RU or self.connection == EdgeConnection.RD:
            return Edge(self.coords.right(), EdgeConnection((self.connection + 4) % 8))
        if self.connection == EdgeConnection.LU or self.connection == EdgeConnection.LD:
            return Edge(self.coords.left(), EdgeConnection((self.connection + 4) % 8))

    def __str__(self):
        return f"EDGE({self.coords}:{self.connection.name})"

    def __eq__(self, other: Edge):
        return self.coords == other.coords and self.connection == other.connection

    def __ne__(self, other: Edge):
        return not(self == other)
