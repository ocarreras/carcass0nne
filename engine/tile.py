from typing import Dict

from engine.coords import Coords
from engine.placement import EdgeOrientation, Placement
from engine.city import City, CityPlacement
from engine.road import Road, RoadPlacement
from engine.monastery import Monastery, MonasteryPlacement

from engine.field import FieldPlacement
from engine.shape import ShapeType


class Tile:
    def __init__(self, borders: [ShapeType] = None,
                 city_placements: [CityPlacement] = None,
                 road_placements: [RoadPlacement] = None,
                 field_placements: [FieldPlacement] = None,
                 monastery_placement: MonasteryPlacement = None,
                 image=None):
        self.borders: [ShapeType] = borders
        self.placements: Dict[ShapeType, list] = {
            ShapeType.CITY: city_placements,
            ShapeType.ROAD: road_placements,
            ShapeType.FIELD: field_placements,
            ShapeType.MONASTERY: []
        }
        if monastery_placement:
            self.placements[ShapeType.MONASTERY] = [monastery_placement]

        self.connections: Dict[ShapeType, Dict[EdgeOrientation, Placement]] = None
        self.image = image
        self.tile_name = image[10]
        self.rotation = 0
        self.coords = 0

    def __str__(self):
        return f"Tile: {self.tile_name} R:{self.rotation}"

    ##roadPlacements
    # Place tile at coords/rotation, initialize all placemetns.
    def place(self, board, coords: Coords, rotation: int, n_players: int):
        self.coords = coords
        self.rotation = rotation
        self.__initialize_placements(board, coords, n_players)
        self.__initialize_tile_connections()

    ##
    # We need to rotate all placements to our current orientation
    def __initialize_placements(self, board, coords: Coords, n_players):
        for cityPlacement in self.placements[ShapeType.CITY]:
            cityPlacement: CityPlacement
            cityPlacement.initialize(self.rotation)
            cityPlacement.shape = City(cityPlacement, coords, n_players)
        for monasteryPlacement in self.placements[ShapeType.MONASTERY]:
            monasteryPlacement: MonasteryPlacement
            monasteryPlacement.shape = Monastery(monasteryPlacement, coords, n_players)
            monasteryPlacement.shape.initialize(board, coords)
        for roadPlacement in self.placements[ShapeType.ROAD]:
            roadPlacement: RoadPlacement
            roadPlacement.initialize(self.rotation)
            roadPlacement.shape = Road(roadPlacement, coords, n_players)

    ##
    # Initialize connections maps, so we can access placements through U D R L maps
    #
    # We need to rotate placements with __initialize_placements before calling this function.
    def __initialize_tile_connections(self):
        self.connections = {ShapeType.CITY: {},
                            ShapeType.ROAD: {},
                            ShapeType.FIELD: {}}

        for orientation in EdgeOrientation:
            self.connections[ShapeType.CITY][orientation] = None
        for orientation in EdgeOrientation:
            self.connections[ShapeType.ROAD][orientation] = None

        cityPlacement: CityPlacement
        for cityPlacement in self.placements[ShapeType.CITY]:
            for connection in cityPlacement.connections:
                self.connections[ShapeType.CITY][connection] = cityPlacement
        roadPlacement: RoadPlacement
        for roadPlacement in self.placements[ShapeType.ROAD]:
            for connection in roadPlacement.connections:
                self.connections[ShapeType.ROAD][connection] = roadPlacement

    def get_rotated_border(self, orientation: EdgeOrientation, rotation):
        return self.borders[(orientation - rotation) % 4]

    def get_border(self, orientation: EdgeOrientation):
        return self.borders[(orientation - self.rotation) % 4]
