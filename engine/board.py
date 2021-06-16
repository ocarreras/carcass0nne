from typing import Dict

from engine.coords import Coords
from engine.tile import Tile
from engine.placement import EdgeOrientation
from engine.city import City, CityPlacement
from engine.road import Road, RoadPlacement

class Board:
    def __init__(self, initial_coords: Coords, first_tile: Tile):
        self.board: Dict[Coords, Tile] = {initial_coords: first_tile}
        self.freeSquares = [
            initial_coords.up(),
            initial_coords.down(),
            initial_coords.right(),
            initial_coords.left()
        ]

    def insert_tile(self, coords: Coords, tile: Tile):
        self.board[coords] = tile
        self.__update_free_squares(coords)

    def fits(self, coords: Coords, tile: Tile, rotation: int):
        assert (coords not in self.board)

        if coords.up() in self.board and \
                self.board[coords.up()].get_border(EdgeOrientation.D) != \
                tile.get_rotated_border(EdgeOrientation.U, rotation):
            return False
        if coords.down() in self.board and \
                self.board[coords.down()].get_border(EdgeOrientation.U) != \
                tile.get_rotated_border(EdgeOrientation.D, rotation):
            return False
        if coords.right() in self.board and \
                self.board[coords.right()].get_border(EdgeOrientation.L) != \
                tile.get_rotated_border(EdgeOrientation.R, rotation):
            return False
        if coords.left() in self.board and \
                self.board[coords.left()].get_border(EdgeOrientation.R) != \
                tile.get_rotated_border(EdgeOrientation.L, rotation):
            return False
        return True

    ##
    # TODO:
    #   __get_connected_city_placement
    #   __get_connected_road_placement -> similar, needs refactor
    def __get_connected_city_placement(self, coords: Coords, connection: EdgeOrientation) -> CityPlacement:
        if connection == EdgeOrientation.U:
            if coords.up() in self.board:
                return self.board[coords.up()].cityConnections[EdgeOrientation.D]
            return None
        if connection == EdgeOrientation.D:
            if coords.down() in self.board:
                return self.board[coords.down()].cityConnections[EdgeOrientation.U]
            return None
        if connection == EdgeOrientation.R:
            if coords.right() in self.board:
                return self.board[coords.right()].cityConnections[EdgeOrientation.L]
            return None
        if connection == EdgeOrientation.L:
            if coords.left() in self.board:
                return self.board[coords.left()].cityConnections[EdgeOrientation.R]
            return None
    ##
    # TODO:
    #   __get_connected_city_placement
    #   __get_connected_road_placement -> similar, needs refactor
    def __get_connected_road_placement(self, coords: Coords, connection: EdgeOrientation) -> RoadPlacement:
        if connection == EdgeOrientation.U:
            if coords.up() in self.board:
                return self.board[coords.up()].roadConnections[EdgeOrientation.D]
            return None
        if connection == EdgeOrientation.D:
            if coords.down() in self.board:
                return self.board[coords.down()].roadConnections[EdgeOrientation.U]
            return None
        if connection == EdgeOrientation.R:
            if coords.right() in self.board:
                return self.board[coords.right()].roadConnections[EdgeOrientation.L]
            return None
        if connection == EdgeOrientation.L:
            if coords.left() in self.board:
                return self.board[coords.left()].roadConnections[EdgeOrientation.R]
            return None

    def get_connected_city(self, coords: Coords, connection: EdgeOrientation) -> City:
        placement = self.__get_connected_city_placement(coords, connection)
        return placement.city if placement else None

    def get_connected_road(self, coords: Coords, connection: EdgeOrientation) -> Road:
        placement = self.__get_connected_road_placement(coords, connection)
        return placement.road if placement else None


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