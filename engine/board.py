from typing import Dict

from collections.abc import MutableMapping
from engine.coords import Coords
from engine.tile import Tile
from engine.placement import EdgeConnection, BorderOrientation
from engine.placement import Placement, ShapeType
import numpy as np

##
# TODO: Refactor this
BOARD_LENGTH = 6
ML_BOARD_FEATURES = 4 + 13
ML_BOARD_SIZE = 2 * BOARD_LENGTH + 1

class Board(MutableMapping):
    def __init__(self):
        self.board: Dict[Coords, Tile] = {}
        self.freeSquares = []
        self.ml_board = []
        self.BOARD_LENGTH = BOARD_LENGTH
        self.ML_BOARD_SIZE = ML_BOARD_SIZE
        self.ML_BOARD_FEATURES = ML_BOARD_FEATURES
        self.ml_board_s0 = np.zeros((self.ML_BOARD_SIZE, self.ML_BOARD_SIZE, self.ML_BOARD_FEATURES))
        self.ml_board_s1 = np.zeros((self.ML_BOARD_SIZE, self.ML_BOARD_SIZE, self.ML_BOARD_FEATURES))
        self.ml_board_s2 = np.zeros((self.ML_BOARD_SIZE, self.ML_BOARD_SIZE, self.ML_BOARD_FEATURES))
        self.ml_board_s3 = np.zeros((self.ML_BOARD_SIZE, self.ML_BOARD_SIZE, self.ML_BOARD_FEATURES))

    @staticmethod
    def getActionSize():
        ##
        # This is huge!
        return 1 + ML_BOARD_FEATURES * ML_BOARD_SIZE * ML_BOARD_SIZE * 4

    def init(self, initial_coords: Coords, first_tile: Tile):
        self.board: Dict[Coords, Tile] = {initial_coords: first_tile}
        self.freeSquares = [
            initial_coords.up(),
            initial_coords.down(),
            initial_coords.right(),
            initial_coords.left()
        ]
        self.ml_board_s0[initial_coords.y+BOARD_LENGTH][initial_coords.x+BOARD_LENGTH][0] = first_tile.tile_num()
        self.ml_board_s1[-initial_coords.y+BOARD_LENGTH][initial_coords.x+BOARD_LENGTH][0] = first_tile.tile_num()
        self.ml_board_s2[initial_coords.y+BOARD_LENGTH][-initial_coords.x+BOARD_LENGTH][0] = first_tile.tile_num()
        self.ml_board_s3[-initial_coords.y+BOARD_LENGTH][-initial_coords.x+BOARD_LENGTH][0] = first_tile.tile_num()

    def copy(self):
        my_copy = Board()
        for key in self.board:
            my_copy.board[key] = self.board[key].copy()
        my_copy.freeSquares = []
        for freeSquare in self.freeSquares:
            my_copy.freeSquares.append(freeSquare)
        my_copy.ml_board = self.ml_board.copy()

        return my_copy

    def insert_meeple_ml(self, coords, placement_ind, ml_player):
        # TODO: Assuming placement_ind 1 based / recheck
        self.ml_board_s0[coords.y+BOARD_LENGTH][coords.x+BOARD_LENGTH][3 + placement_ind] = ml_player
        self.ml_board_s1[-coords.y+BOARD_LENGTH][coords.x+BOARD_LENGTH][3 + placement_ind] = ml_player
        self.ml_board_s2[coords.y+BOARD_LENGTH][-coords.x+BOARD_LENGTH][3 + placement_ind] = ml_player
        self.ml_board_s3[-coords.y+BOARD_LENGTH][-coords.x+BOARD_LENGTH][3 + placement_ind] = ml_player

    def remove_meeple_ml(self, coords, placement_ind):
        # TODO: Assuming placement_ind 1 based / recheck
        self.ml_board_s0[coords.y+BOARD_LENGTH][coords.x+BOARD_LENGTH][3 + placement_ind] = 0
        self.ml_board_s1[-coords.y+BOARD_LENGTH][coords.x+BOARD_LENGTH][3 + placement_ind] = 0
        self.ml_board_s2[coords.y+BOARD_LENGTH][-coords.x+BOARD_LENGTH][3 + placement_ind] = 0
        self.ml_board_s3[-coords.y+BOARD_LENGTH][-coords.x+BOARD_LENGTH][3 + placement_ind] = 0

    def insert_tile(self, coords: Coords, tile: Tile):
        self.ml_board_s0[coords.y+BOARD_LENGTH][coords.x+BOARD_LENGTH][tile.rotation] = 1 + tile.tile_num()
        self.ml_board_s1[-coords.y+BOARD_LENGTH][coords.x+BOARD_LENGTH][tile.rotation] = 1 + tile.tile_num()
        self.ml_board_s2[coords.y+BOARD_LENGTH][-coords.x+BOARD_LENGTH][tile.rotation] = 1 + tile.tile_num()
        self.ml_board_s3[-coords.y+BOARD_LENGTH][-coords.x+BOARD_LENGTH][tile.rotation] = 1 + tile.tile_num()
        self.board[coords] = tile
        self.__update_free_squares(coords)

    def fits(self, tile: Tile, coords: Coords, rotation: int):
        assert (coords not in self.board)

        if coords.up() in self.board and \
                self.board[coords.up()].get_border(BorderOrientation.D) != \
                tile.get_rotated_border(BorderOrientation.U, rotation):
            return False
        if coords.down() in self.board and \
                self.board[coords.down()].get_border(BorderOrientation.U) != \
                tile.get_rotated_border(BorderOrientation.D, rotation):
            return False
        if coords.right() in self.board and \
                self.board[coords.right()].get_border(BorderOrientation.L) != \
                tile.get_rotated_border(BorderOrientation.R, rotation):
            return False
        if coords.left() in self.board and \
                self.board[coords.left()].get_border(BorderOrientation.R) != \
                tile.get_rotated_border(BorderOrientation.L, rotation):
            return False
        return True

    def get_available_tile_placements(self, tile):
        placements = []
        for coords in self.freeSquares:
            ##
            # Forcing user to our bonding board, this is not correct according to rules,
            # but simplifies the problem.
            if abs(coords.x) > BOARD_LENGTH or abs(coords.y) > BOARD_LENGTH:
                continue
            for rotation in tile.rotations:
                if self.fits(tile, coords, rotation):
                    placements.append((coords, rotation))
        return placements

    def __get_connected_placement(self, shape_type: ShapeType, coords: Coords, connection: EdgeConnection) \
            -> Placement:
        if connection == EdgeConnection.UR:
            if coords.up() in self.board:
                return self.board[coords.up()].connections[shape_type][EdgeConnection.DR]
            return None
        if connection == EdgeConnection.UL:
            if coords.up() in self.board:
                return self.board[coords.up()].connections[shape_type][EdgeConnection.DL]
            return None
        if connection == EdgeConnection.DL:
            if coords.down() in self.board:
                return self.board[coords.down()].connections[shape_type][EdgeConnection.UL]
            return None
        if connection == EdgeConnection.DR:
            if coords.down() in self.board:
                return self.board[coords.down()].connections[shape_type][EdgeConnection.UR]
            return None
        if connection == EdgeConnection.RU:
            if coords.right() in self.board:
                return self.board[coords.right()].connections[shape_type][EdgeConnection.LU]
            return None
        if connection == EdgeConnection.RD:
            if coords.right() in self.board:
                return self.board[coords.right()].connections[shape_type][EdgeConnection.LD]
            return None
        if connection == EdgeConnection.LD:
            if coords.left() in self.board:
                return self.board[coords.left()].connections[shape_type][EdgeConnection.RD]
            return None
        if connection == EdgeConnection.LU:
            if coords.left() in self.board:
                return self.board[coords.left()].connections[shape_type][EdgeConnection.RU]
            return None

    def get_connected_placement(self, shape_type: ShapeType, coords: Coords, connection: EdgeConnection) -> Placement:
        return self.__get_connected_placement(shape_type, coords, connection)

    def __update_free_squares(self, coords: Coords):
        self.freeSquares.remove(coords)
        if coords.up() not in self.board and coords.up() not in self.freeSquares:
            self.freeSquares.append(coords.up())
        if coords.down() not in self.board and coords.down() not in self.freeSquares:
            self.freeSquares.append(coords.down())
        if coords.right() not in self.board and coords.right() not in self.freeSquares:
            self.freeSquares.append(coords.right())
        if coords.left() not in self.board and coords.left() not in self.freeSquares:
            self.freeSquares.append(coords.left())

    def __getitem__(self, key):
        return self.board[key] if key in self.board else None

    def __contains__(self, key):
        return key in self.board

    def __len__(self, key):
        return len(self.board)

    def __iter__(self):
        print("ITERING ...")
        return iter(self.board)

    def __delitem__(self, key):
        assert False, "Not implemented"

    def __setitem__(self, key, value):
        assert False, "Not implemented"
