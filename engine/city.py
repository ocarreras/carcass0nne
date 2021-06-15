from __future__ import annotations
from engine.placement import Placement, Edge, EdgeOrientation
from engine.coords import Coords


##
# This class represents each independent possible city placement inside a tile.
class CityPlacement(Placement):
    def __init__(self, connections: [EdgeOrientation], shield=False, meeple_xy=None):
        super().__init__(meeple_xy)
        self.connections: [EdgeOrientation] = connections
        self.shield: bool = shield
        self.city: City = None
        self.coords = None

    def place(self, coords: Coords, rotation: int):
        self.coords = coords
        self.connections = list(map(lambda c: EdgeOrientation((c+rotation) % 4), self.connections))

    def __str__(self):
        return f"{self.coords} :: {list(map(lambda l: l.name, self.connections))}"

    def __repr__(self):
        return self.__str__()


class City:
    def __init__(self, placement: CityPlacement, coords):
        self.completed = False
        self.placements = [placement]
        self.openEdges = []
        self.initialize_open_edges(placement, coords)

    def initialize_open_edges(self, placement: CityPlacement, coords):
        self.openEdges = []
        for connection in placement.connections:
            self.openEdges.append(Edge(coords, connection))

    def merge_city(self, city: City):
        assert city != self
        for placement in city.placements:
            placement.city = self
        for edge in city.openEdges:
            if edge.opposite() in self.openEdges:
                self.openEdges.remove(edge.opposite())
            else:
                self.openEdges.append(edge)
        self.placements.extend(city.placements)

        if len(self.openEdges) == 0:
            print("Completed CITY!!")
            print(len(self.placements))
            self.completed = True

    def __str__(self):
        return f"CITY {hex(id(self))} #{len(self.placements):02d} " + ("COMPLETED" if self.completed else "OPEN")

    def print(self):
        print(self)
        if not self.completed:
            print("\tEDGE_LIST:")
            for edge in self.openEdges:
                print(f"\t\t{edge}")
        print("\tPLACEMENTS")
        placement: CityPlacement
        for placement in self.placements:
            print(f"\t\t{placement}")
