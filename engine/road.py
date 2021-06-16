from __future__ import annotations
from engine.placement import Placement, EdgeOrientation
from engine.coords import Coords


##
# This class represents each road part inside a tile.
class RoadPlacement(Placement):
    def __init__(self, connections: [EdgeOrientation],
                 meeple_xy=None):
        super().__init__(meeple_xy)
        self.connections = connections
        self.road: Road = None

    def initialize(self, rotation: int):
        self.connections = list(map(lambda c: EdgeOrientation((c+rotation) % 4), self.connections))

    def __str__(self):
        return f"ROAD :: {list(map(lambda l: l.name, self.connections))}"

    def __repr__(self):
        return self.__str__()


class Road:
    def __init__(self, placement: RoadPlacement, coords: Coords, n_players: int):
        self.completed = False
        self.placements = [placement]
        self.n_open_edges = None
        self.initialize_open_edges(placement, coords)
        self.meeples = [0 for _ in range(n_players)]
        self.coords = coords

    def score(self):
        return len(self.placements)

    def winners(self):
        max_meeples = max(self.meeples)
        winners = []
        if max_meeples == 0:
            return winners
        return [i for i in range(len(self.meeples)) if self.meeples[i] == max_meeples]

    def insert_meeple(self, n_player):
        self.meeples[n_player] += 1

    def reset_meeples(self, n_players):
        self.meeples = [0 for _ in range(n_players)]

    def initialize_open_edges(self, placement: RoadPlacement, coords):
        self.n_open_edges = len(placement.connections)

    ##
    # Returns true if the merge completes the road
    def merge_road(self, road: Road) -> bool:
        assert road != self

        for placement in road.placements:
            placement.road = self
        self.placements.extend(road.placements)
        self.meeples = [x+y for x, y in zip(self.meeples, road.meeples)]

        ##
        # we need to account for a road finishing two of our current open edges
        if road.n_open_edges == 1:
            self.n_open_edges -= 1

        if self.n_open_edges == 0:
            self.completed = True
        return self.completed

    def __str__(self):
        return f"ROAD {hex(id(self))} {self.coords} #{len(self.placements):02d} " + ("COMPLETED" if self.completed else "OPEN")

    def print(self):
        print(self)
        print("\tPLACEMENTS")
        placement: RoadPlacement
        for placement in self.placements:
            print(f"\t\t{placement}")
