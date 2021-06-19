from __future__ import annotations
from engine.placement import Placement, Edge, EdgeConnection
from engine.coords import Coords
from engine.shape import Shape


##
# This class represents each road part inside a tile.
class RoadPlacement(Placement):
    def __init__(self, connections: [EdgeConnection],
                 meeple_xy=None):
        super().__init__(meeple_xy)
        self.connections: [EdgeConnection] = connections
        super(RoadPlacement, self).duplicate_connections()

    def __str__(self):
        return f"ROAD :: {list(map(lambda l: l.name, self.connections))}"

    def __repr__(self):
        return self.__str__()

    def copy(self):
        my_copy: RoadPlacement = super(RoadPlacement, self).copy()
        my_copy.__class__ = self.__class__
        return my_copy


class Road(Shape):
    def __init__(self, placement: RoadPlacement, coords: Coords, n_players: int):
        super().__init__(placement, coords, n_players)

    def score(self):
        return len(self.placements)

    def __str__(self):
        return f"ROAD {hex(id(self))} {self.coords} #{len(self.placements):02d} " + ("COMPLETED" if self.completed else
                                                                                     "OPEN")

    def print(self):
        print(self)
        print("\tPLACEMENTS")
        placement: RoadPlacement
        for placement in self.placements:
            print(f"\t\t{placement}")

