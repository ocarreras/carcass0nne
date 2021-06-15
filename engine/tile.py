from enum import Enum, IntEnum

from engine.placement import EdgeOrientation
from engine.coords import Coords
from engine.city import City, CityPlacement
from engine.road import RoadPlacement
from engine.field import FieldPlacement
from engine.monastery import MonasteryPlacement


class TileBorderType(Enum):
    ROAD = 1
    FIELD = 2
    CITY = 3


class Tile:
    def __init__(self, borders: [TileBorderType] = None,
                 city_placements: [CityPlacement] = None,
                 road_placements: [RoadPlacement] = None,
                 field_placements: [FieldPlacement] = None,
                 monastery=False,
                 image=None):
        self.borders: [TileBorderType] = borders
        self.cityPlacements: [CityPlacement] = city_placements
        self.cityPlacementMap = {}
        self.roadPlacements: [RoadPlacement] = road_placements
        self.fieldPlacements: [FieldPlacement] = field_placements
        self.monasteryPlacement: MonasteryPlacement = None
        if monastery:
            self.monasteryPlacement = MonasteryPlacement()
        self.image = image
        self.tile_name = image[10]
        self.rotation = 0
        self.coords = 0

    def __str__(self):
        return f"{self.tile_name} R:{self.rotation}"

    ##
    # Place tile at coords/rotation, initialize it.
    def place(self, coords, rotation):
        self.coords = coords
        self.rotation = rotation
        self.__place_placements()

        for placement in self.cityPlacements:
            placement.city = City(placement, self.coords)
        self.__initialize_placement_maps()

    ##
    # TODO: yeah, this name ...
    def __place_placements(self):
        cityPlacement: CityPlacement
        for cityPlacement in self.cityPlacements:
            cityPlacement.place(self.coords, self.rotation)

    ##
    # Initialize placementMaps to access placement objects without iterating the lists.
    # Take into account current tile rotation.
    def __initialize_placement_maps(self):
        self.cityPlacementMap = {}
        for orientation in EdgeOrientation:
            self.cityPlacementMap[orientation] = None
        cityPlacement: CityPlacement
        for cityPlacement in self.cityPlacements:
            for connection in cityPlacement.connections:
                self.cityPlacementMap[connection] = cityPlacement

    def get_rotated_border(self, orientation: EdgeOrientation, rotation):
        return self.borders[(orientation - rotation) % 4]

    def get_border(self, orientation: EdgeOrientation):
        return self.borders[(orientation - self.rotation) % 4]
