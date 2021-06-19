from typing import Dict

from engine.coords import Coords
from engine.placement import EdgeConnection, BorderOrientation, Placement
from engine.city import City, CityPlacement
from engine.road import Road, RoadPlacement
from engine.field import Field, FieldPlacement
from engine.monastery import Monastery, MonasteryPlacement
from engine.shape import ShapeType


class Tile:
    def __init__(self, borders: [ShapeType] = None,
                 city_placements: [CityPlacement] = None,
                 road_placements: [RoadPlacement] = None,
                 field_placements: [FieldPlacement] = None,
                 monastery_placement: MonasteryPlacement = None,
                 tile_type: str = None,
                 rotations: [int] = None):
        self.borders: [ShapeType] = borders
        self.placements: Dict[ShapeType, list] = {
            ShapeType.CITY: city_placements,
            ShapeType.ROAD: road_placements,
            ShapeType.FIELD: field_placements,
            ShapeType.MONASTERY: []
        }
        if monastery_placement:
            self.placements[ShapeType.MONASTERY] = [monastery_placement]

        self.connections: Dict[ShapeType, Dict[EdgeConnection, Placement]] = None
        self.tile_type = tile_type
        self.rotation = 0
        self.coords = 0
        self.rotations = rotations

    def copy(self):
        my_copy = Tile()
        my_copy.borders = self.borders.copy()
        my_copy.placements = {}
        for placement_type in self.placements:
            my_copy.placements[placement_type] = []
            for placement in self.placements[placement_type]:
                my_copy.placements[placement_type].append(placement.copy())
        my_copy.tile_type = self.tile_type
        my_copy.rotation = self.rotation
        my_copy.coords = self.coords
        my_copy.rotations = self.rotations
        return my_copy

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
        for fieldPlacement in self.placements[ShapeType.FIELD]:
            fieldPlacement: FieldPlacement
            fieldPlacement.initialize_field(self.rotation, self.placements[ShapeType.CITY])
            fieldPlacement.shape = Field(fieldPlacement, coords, n_players)

    ##
    # Initialize connections maps, so we can access placements through U D R L maps
    #
    # We need to rotate placements with __initialize_placements before calling this function.
    def __initialize_tile_connections(self):
        shape_types = [ShapeType.CITY, ShapeType.ROAD, ShapeType.FIELD]
        self.connections = {}
        for shape_type in shape_types:
            self.connections[shape_type] = {}
            for orientation in EdgeConnection:
                self.connections[shape_type][orientation] = None
            for placement in self.placements[shape_type]:
                for connection in placement.connections:
                    self.connections[shape_type][connection] = placement

    def get_rotated_border(self, orientation: BorderOrientation, rotation):
        return self.borders[(orientation - rotation) % 4]

    def get_border(self, orientation: BorderOrientation):
        return self.borders[(orientation - self.rotation) % 4]

    def __str__(self):
        return f"Tile: {self.tile_name} R:{self.rotation}"