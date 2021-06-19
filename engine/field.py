from __future__ import annotations
from engine.placement import Placement, EdgeConnection
from engine.city import CityPlacement
from engine.shape import Shape


##
# This class represents each field possible placement inside a tile.
class FieldPlacement(Placement):
    def __init__(self, connections: [EdgeConnection], city_connections=None, meeple_xy=None):
        super().__init__(meeple_xy)
        self.connections = connections
        self.cityConnections = city_connections
        self.cityPlacements = set()

    def initialize_field(self, rotation: int, city_placements: [CityPlacement]):
        super(FieldPlacement, self).initialize(rotation)
        for cityConnection in self.cityConnections:
            self.cityPlacements.add(city_placements[cityConnection])

    def __str__(self):
        return f"FIELD :: {list(map(lambda l: l.name, self.connections))}"

    def __repr__(self):
        return self.__str__()

    def copy(self):
        my_copy = super(FieldPlacement, self).copy()
        my_copy.__class__ = self.__class__
        my_copy.cityPlacements = self.cityPlacements.copy()
        my_copy.cityConnections = self.cityConnections.copy()
        return my_copy


class Field(Shape):
    def __init__(self, placement: FieldPlacement, coords, n_players):
        super().__init__(placement, coords, n_players)
        self.cityPlacements = placement.cityPlacements

    def score(self):
        return sum(map(lambda c: 4 if c.completed else 0, self.adjacent_cities()))

    def merge(self, merged_field: Field):
        super(Field, self).merge(merged_field)
        self.completed = False
        for placement in merged_field.cityPlacements:
            self.cityPlacements.add(placement)

    def adjacent_cities(self):
        cities = set()
        for placement in self.cityPlacements:
            cities.add(placement.shape)
        return list(cities)

    def __str__(self):
        return f"FIELD {hex(id(self))} {self.coords} #{len(self.placements):02d} "

    def print(self):
        print(self)
        print("\tPLACEMENTS")
        placement: FieldPlacement
        for placement in self.placements:
            print(f"\t\t{placement}")
