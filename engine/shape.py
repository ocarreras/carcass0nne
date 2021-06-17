from __future__ import annotations
from enum import Enum
from engine.placement import Placement, Edge, EdgeOrientation


class ShapeType(Enum):
    ROAD = 1
    FIELD = 2
    CITY = 3
    MONASTERY = 4


##
# Super class or Road / City / Field
#
# Contains the shared functions for scoring / merging / meeple management.
class Shape:
    def __init__(self, placement: Placement, coords, n_players):
        self.completed = False
        self.placements = [placement]
        self.open_edges = []
        self.initialize_open_edges(placement, coords)
        self.meeples = [0 for _ in range(n_players)]
        self.coords = coords

    def winners(self):
        max_meeples = max(self.meeples)
        winners = []
        if max_meeples == 0:
            return winners
        return [i for i in range(len(self.meeples)) if self.meeples[i] == max_meeples]

    def initialize_open_edges(self, placement: Placement, coords):
        self.open_edges = []
        for connection in placement.connections:
            self.open_edges.append(Edge(coords, connection))

    def insert_meeple(self, n_player):
        self.meeples[n_player] += 1

    def reset_meeples(self, n_players):
        self.meeples = [0 for _ in range(n_players)]

    ##
    # Returns true if the merge completes the shape
    def merge(self, merged_shape: Shape) -> bool:
        assert merged_shape != self

        for edge in merged_shape.open_edges:
            if edge.opposite() in self.open_edges:
                self.open_edges.remove(edge.opposite())
            else:
                self.open_edges.append(edge)
        self.placements.extend(merged_shape.placements)
        self.meeples = [x + y for x, y in zip(self.meeples, merged_shape.meeples)]

        if len(self.open_edges) == 0:
            self.completed = True

        for placement in merged_shape.placements:
            placement.shape = self

        return self.completed
