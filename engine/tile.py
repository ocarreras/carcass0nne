from enum import Enum

from engine.coords import Coords
from engine.placement import EdgeOrientation, Placement
from engine.city import City, CityPlacement
from engine.road import Road, RoadPlacement
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
                 monastery_placement: MonasteryPlacement = None,
                 image=None):
        self.borders: [TileBorderType] = borders

        self.cityPlacements: [CityPlacement] = city_placements
        self.cityConnections: dict[EdgeOrientation, CityPlacement] = {}
        self.roadPlacements: [RoadPlacement] = road_placements
        self.roadConnections: dict[EdgeOrientation, RoadPlacement] = {}
        self.fieldPlacements: [FieldPlacement] = field_placements
        self.monasteryPlacement: MonasteryPlacement = monastery_placement
        self.image = image
        self.tile_name = image[10]
        self.rotation = 0
        self.coords = 0

    def __str__(self):
        return f"Tile: {self.tile_name} R:{self.rotation}"

    ##
    # Place tile at coords/rotation, initialize all placemetns.
    def place(self, board, coords: Coords, rotation: int, n_players: int):
        self.coords = coords
        self.rotation = rotation
        self.__initialize_placements(board, coords, n_players)
        self.__initialize_tile_connections()

    ##
    # We need to rotate all placements to our current orientation
    def __initialize_placements(self, board, coords: Coords, n_players):
        cityPlacement: CityPlacement
        for cityPlacement in self.cityPlacements:
            cityPlacement.initialize(self.rotation)
            cityPlacement.city = City(cityPlacement, coords, n_players)
        if self.monasteryPlacement:
            self.monasteryPlacement.initialize(board.board, coords)
        roadPlacement: RoadPlacement
        for roadPlacement in self.roadPlacements:
            roadPlacement.initialize(self.rotation)
            roadPlacement.road = Road(roadPlacement, coords, n_players)
    ##
    # Initialize <resource>Connection maps, so we can access them through U D R L
    #
    # We need to rotate placements with __initialize_placements before calling this.
    def __initialize_tile_connections(self):

        self.cityConnections = {}
        for orientation in EdgeOrientation:
            self.cityConnections[orientation] = None
        cityPlacement: CityPlacement
        for cityPlacement in self.cityPlacements:
            for connection in cityPlacement.connections:
                self.cityConnections[connection] = cityPlacement
        self.roadConnections = {}
        for orientation in EdgeOrientation:
            self.roadConnections[orientation] = None
        roadPlacement: RoadPlacement
        for roadPlacement in self.roadPlacements:
            for connection in roadPlacement.connections:
                self.roadConnections[connection] = roadPlacement

    def get_rotated_border(self, orientation: EdgeOrientation, rotation):
        return self.borders[(orientation - rotation) % 4]

    def get_border(self, orientation: EdgeOrientation):
        return self.borders[(orientation - self.rotation) % 4]
