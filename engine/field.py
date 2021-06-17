from __future__ import annotations
from enum import Enum
from engine.placement import Placement, EdgeConnection
from engine.shape import Shape


##
# This class represents each field possible placement inside a tile.
class FieldPlacement(Placement):
    def __init__(self, connections: [EdgeConnection], city_connections=None, meeple_xy=None):
        super().__init__(meeple_xy)
        self.connections = connections
        self.cityConnections = city_connections

    def __str__(self):
        return f"FIELD :: {list(map(lambda l: l.name, self.connections))}"

    def __repr__(self):
        return self.__str__()


class Field(Shape):
    def __init__(self, placement: FieldPlacement, coords, n_players):
        super().__init__(placement, coords, n_players)

    def score(self):
        return len(self.placements)

    def merge(self, merged_field):
        super(Field, self).merge(merged_field)
        self.completed = False

    def __str__(self):
        return f"FIELD {hex(id(self))} {self.coords} #{len(self.placements):02d} "

    def print(self):
        print(self)
        print("\tPLACEMENTS")
        placement: FieldPlacement
        for placement in self.placements:
            print(f"\t\t{placement}")
