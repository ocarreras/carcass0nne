from __future__ import annotations
from engine.placement import Placement, EdgeConnection
from engine.coords import Coords


##
# This class represents each road part inside a tile.
class RoadPlacement(Placement):
    def __init__(self, connections: [EdgeConnection],
                 meeple_xy=None):
        super().__init__(meeple_xy)
        self.connections: [EdgeConnection] = connections
        super(RoadPlacement, self).duplicate_connections()

    def initialize_shape(self, coords: Coords, rotation: int, n_players: int):
        super(RoadPlacement, self).initialize_shape(coords, rotation, n_players)

    def copy(self):
        my_copy: RoadPlacement = super(RoadPlacement, self).copy()
        my_copy.__class__ = self.__class__
        return my_copy

    def score(self):
        return len(self.shape_placements)

    def print(self):
        print(self)
        print("\tPLACEMENTS")
        placement: RoadPlacement
        for placement in self.shape_placements:
            print(f"\t\t{placement}")

    def __str__(self):
        return f"ROAD {hex(id(self))} {self.coords} #{len(self.shape_placements):02d} " + \
               ("COMPLETED" if self.completed else "OPEN") + f"{list(map(lambda l: l.name, self.connections))}"

    def __repr__(self):
        return self.__str__()
