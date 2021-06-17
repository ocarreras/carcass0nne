from __future__ import annotations
from engine.placement import Placement, Edge, EdgeOrientation
from engine.coords import Coords


##
# This class represents each independent possible city placement inside a tile.
class CityPlacement(Placement):
    def __init__(self, connections: [EdgeOrientation], shield=None, meeple_xy=None):
        super().__init__(meeple_xy)
        self.connections: [EdgeOrientation] = connections
        self.score: int = 2 if shield else 1
        self.city: City = None

    def initialize(self, rotation: int):
        self.connections = list(map(lambda c: EdgeOrientation((c+rotation) % 4), self.connections))

    def __str__(self):
        return f"CITY :: {list(map(lambda l: l.name, self.connections))}"

    def __repr__(self):
        return self.__str__()


class City:
    def __init__(self, placement: CityPlacement, coords, n_players):
        self.completed = False
        self.placements = [placement]
        self.open_edges = []
        self.initialize_open_edges(placement, coords)
        self.meeples = [0 for _ in range(n_players)]
        self.coords = coords

    def score(self):
        score = sum(map(lambda p: p.score, self.placements))
        if self.completed:
            score = score*2
        return score

    def winners(self):
        max_meeples = max(self.meeples)
        winners = []
        if max_meeples == 0:
            return winners
        return [i for i in range(len(self.meeples)) if self.meeples[i] == max_meeples]

    def initialize_open_edges(self, placement: CityPlacement, coords):
        self.open_edges = []
        for connection in placement.connections:
            self.open_edges.append(Edge(coords, connection))

    def insert_meeple(self, n_player):
        self.meeples[n_player] += 1

    def reset_meeples(self, n_players):
        self.meeples = [0 for _ in range(n_players)]

    ##
    # Returns true if the merge completes the city
    def merge_city(self, city: City) -> bool:
        assert city != self

        for placement in city.placements:
            placement.city = self
        for edge in city.open_edges:
            if edge.opposite() in self.open_edges:
                self.open_edges.remove(edge.opposite())
            else:
                self.open_edges.append(edge)
        self.placements.extend(city.placements)
        self.meeples = [x+y for x, y in zip(self.meeples, city.meeples)]

        if len(self.open_edges) == 0:
            self.completed = True
        return self.completed

    def __str__(self):
        return f"CITY {hex(id(self))} {self.coords} #{len(self.placements):02d} " + \
               ("COMPLETED" if self.completed else "OPEN")

    def print(self):
        print(self)
        if not self.completed:
            print("\tEDGE_LIST:")
            for edge in self.open_edges:
                print(f"\t\t{edge}")
        print("\tPLACEMENTS")
        placement: CityPlacement
        for placement in self.placements:
            print(f"\t\t{placement}")
