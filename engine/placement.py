from __future__ import annotations
from enum import IntEnum
from engine.coords import Coords
from enum import Enum


class ShapeType(Enum):
    ROAD = 1
    FIELD = 2
    CITY = 3
    MONASTERY = 4


class Placement:
    def __init__(self, meeple_xy=[0, 0]):
        self.meeple_xy = meeple_xy
        self.connections = None
        self.meeple = None                  # id of a player or None
        self.shape = None
        self.completed = False
        self.connected_placement = None     # None if not connected
        self.shape_placements = []
        self.open_edges = []
        self.meeples = None
        self.coords = None

    def initialize_rotation(self, rotation: int):
        self.connections = list(map(lambda c: EdgeConnection((c + rotation * 2) % 8), self.connections))

    def initialize_shape(self, coords: Coords, rotation: int, n_players):
        self.coords = coords
        self.initialize_rotation(rotation)
        self.initialize_open_edges(coords)
        self.shape_placements = [self]
        self.meeples = [0 for _ in range(n_players)]
        self.connected_placement = self

    def copy(self):
        my_copy: Placement = Placement()
        my_copy.meeple_xy = self.meeple_xy.copy()
        my_copy.connections = self.connections.copy()
        my_copy.meeple = self.meeple
        my_copy.shape = self.shape
        my_copy.completed = self.completed

        my_copy.connected_placement = self.connected_placement
        my_copy.shape_placements = self.shape_placements.copy()
        my_copy.open_edges = self.open_edges.copy()
        if self.meeples:
            my_copy.meeples = self.meeples.copy()
        my_copy.coords = self.coords
        return my_copy

    def winners(self):
        max_meeples = max(self.meeples)
        winners = []
        if max_meeples == 0:
            return winners
        return [i for i in range(len(self.meeples)) if self.meeples[i] == max_meeples]

    def initialize_open_edges(self, coords):
        self.open_edges = []
        for connection in self.connections:
            self.open_edges.append(Edge(coords, connection))

    def insert_meeple(self, n_player):
        self.meeples[n_player] += 1

    def reset_meeples(self, n_players):
        self.meeples = [0 for _ in range(n_players)]

    ##
    # Returns true if the merge completes the shape
    def merge(self, merged_placement: Placement) -> bool:
        assert merged_placement != self

        while merged_placement.connected_placement and merged_placement.connected_placement != merged_placement:
            old = merged_placement
            merged_placement = merged_placement.connected_placement
            old.connected_placement = self
        new_open_edges = self.open_edges.copy()
        for edge in merged_placement.open_edges:
            if edge.opposite() in self.open_edges:
                new_open_edges.remove(edge.opposite())
            else:
                new_open_edges.append(edge)
        self.open_edges = new_open_edges
        merged_placement.connected_placement = self
        self.shape_placements.extend(merged_placement.shape_placements)
        # We leave references only @ head.
        merged_placement.shape_placements = []
        self.meeples = [x + y for x, y in zip(self.meeples, merged_placement.meeples)]

        if len(self.open_edges) == 0:
            self.completed = True
        return self.completed

    ##
    # Uggly!
    #
    # Duplicate connections for city/roads so we can use the same connectivity functions.
    # We initially only set LD/DL/UL/RU and we need to add the other parities to keep connectivity.
    def duplicate_connections(self):
        new_connections = self.connections.copy()
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
