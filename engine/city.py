from __future__ import annotations
from engine.placement import Placement, Edge, EdgeConnection


class CityPlacement(Placement):
    def __init__(self, connections: [EdgeConnection], shield=None, meeple_xy=None):
        super().__init__(meeple_xy)
        self.connections: [EdgeConnection] = connections
        super(CityPlacement, self).duplicate_connections()
        self.has_shield: bool = shield

    def initialize_shape(self, coords, rotation, n_players):
        super(CityPlacement, self).initialize_shape(coords, rotation, n_players)

    def copy(self):
        my_copy: CityPlacement = super(CityPlacement, self).copy()
        my_copy.__class__ = self.__class__
        my_copy.has_shield = self.has_shield
        return my_copy

    def score(self):
        score = sum(map(lambda p: 2 if p.has_shield else 1, self.shape_placements))
        if self.completed:
            score = score*2
        return score

    def print(self):
        print(self)
        if not self.completed:
            print("\tEDGE_LIST:")
            for edge in self.open_edges:
                print(f"\t\t{edge}")
        print("\tPLACEMENTS")
        placement: CityPlacement
        for placement in self.shape_placements:
            print(f"\t\t{placement}")

    def __str__(self):
        return f"CITY :: {list(map(lambda l: l.name, self.connections))}"

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"CITY {hex(id(self))} {self.coords} #{len(self.shape_placements):02d} " + \
               ("COMPLETED" if self.completed else "OPEN")
