from typing import Dict

from engine.placement import EdgeConnection, BorderOrientation, Placement, ShapeType
from engine.city import CityPlacement
from engine.road import RoadPlacement
from engine.field import FieldPlacement
from engine.monastery import MonasteryPlacement
from engine.coords import Coords


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

    ##
    # </ ML
    def copy(self):
        my_copy = Tile()
        my_copy.borders = self.borders.copy()
        my_copy.placements = {}
        for placement_type in self.placements:
            my_copy.placements[placement_type] = []
            for placement in self.placements[placement_type]:
                placement_copy = placement.copy()
                my_copy.placements[placement_type].append(placement_copy)
        my_copy.tile_type = self.tile_type
        my_copy.rotation = self.rotation
        my_copy.coords = self.coords
        my_copy.rotations = self.rotations
        return my_copy

    def tile_num(self):
        return ord(self.tile_type[0])-65

    def placement_ind(self, placement):
        if not placement:
            return 0
        if type(placement) == RoadPlacement:
            return 1 + self.placements[ShapeType.ROAD].index(placement)
        elif type(placement) == FieldPlacement:
            return 5 + self.placements[ShapeType.FIELD].index(placement)
        elif type(placement) == CityPlacement:
            return 9 + self.placements[ShapeType.CITY].index(placement)
        elif type(placement) == MonasteryPlacement:
            return 13
        return -1

    def get_placement_by_ind(self, placement_ind):
        assert 13 >= placement_ind >= 0
        if placement_ind == 13:
            return self.placements[ShapeType.MONASTERY][0]
        elif placement_ind >= 9:
            return self.placements[ShapeType.CITY][placement_ind-9]
        elif placement_ind >= 5:
            return self.placements[ShapeType.FIELD][placement_ind-5]
        elif placement_ind >= 1:
            return self.placements[ShapeType.ROAD][placement_ind-1]
        return None

    ##
    # End ML />

    def meeple_repr(self):
        meeple_repr = 0
        for ind1, shape_type in enumerate(ShapeType):
            for ind2, placement in enumerate(self.placements[shape_type]):
                placement: Placement
                if placement.meeple is not None:
                    meeple_repr = (ind1*4 + ind2) * (1 if placement.meeple == 0 else -1)
                    break
            if meeple_repr:
                break
        return meeple_repr

    # Place tile at coords/rotation, initialize all placements.
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
            cityPlacement.initialize_shape(coords, self.rotation, n_players)
        for monasteryPlacement in self.placements[ShapeType.MONASTERY]:
            monasteryPlacement: MonasteryPlacement
            monasteryPlacement.initialize_shape(coords, self.rotation, n_players, board)
        for roadPlacement in self.placements[ShapeType.ROAD]:
            roadPlacement: RoadPlacement
            roadPlacement.initialize_shape(coords, self.rotation, n_players)
        for fieldPlacement in self.placements[ShapeType.FIELD]:
            fieldPlacement: FieldPlacement
            fieldPlacement.initialize_shape(coords, self.rotation, n_players, self.placements[ShapeType.CITY])

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
        return f"TILE: {self.tile_type} {hex(id(self))}  R:{self.rotation}"