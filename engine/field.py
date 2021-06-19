from __future__ import annotations
from engine.placement import Placement, EdgeConnection
from engine.city import CityPlacement


##
# This class represents each field possible placement inside a tile.
class FieldPlacement(Placement):
    def __init__(self, connections: [EdgeConnection], city_connections=None, meeple_xy=None):
        super().__init__(meeple_xy)
        self.connections = connections
        self.cityConnections = city_connections
        self.cityPlacements = set()

    def initialize_shape(self, coords, rotation: int, n_players: int, city_placements: [CityPlacement]=None):
        super(FieldPlacement, self).initialize_shape(coords, rotation, n_players)
        for cityConnection in self.cityConnections:
            self.cityPlacements.add(city_placements[cityConnection])

    def copy(self):
        my_copy = super(FieldPlacement, self).copy()
        my_copy.__class__ = self.__class__
        my_copy.cityPlacements = self.cityPlacements.copy()
        my_copy.cityConnections = self.cityConnections.copy()

        my_copy.cityPlacements = self.cityPlacements.copy()
        return my_copy

    def score(self):
        return sum(map(lambda c: 4 if c.completed else 0, self.adjacent_cities()))

    def merge(self, merged_field: FieldPlacement):
        super(FieldPlacement, self).merge(merged_field)
        self.completed = False
        for placement in merged_field.cityPlacements:
            self.cityPlacements.add(placement)

    def adjacent_cities(self):
        ##
        # TODO: Traverse the placement.connected_placement list.
        cities = set()
        for placement in self.cityPlacements:
            cities.add(placement)
        return list(cities)

    def __str__(self):
        return f"FIELD {hex(id(self))} {self.coords} #{len(self.shape_placements):02d}" + \
               f" {list(map(lambda l: l.name, self.connections))}"

    def __repr__(self):
        return self.__str__()

    def print(self):
        print(self)
        print("\tPLACEMENTS")
        placement: FieldPlacement
        for placement in self.shape_placements:
            print(f"\t\t{placement}")
