from engine.tile_sets import base_deck
from engine.tile import Tile
from engine.city import CityPlacement, City
from engine.coords import Coords
from engine.placement import EdgeOrientation

import random
import copy


class GameState:
    def __init__(self, n_players):
        self.deck = []
        self.board: dict[Coords, Tile] = {}
        self.freeSquares = {}
        self.scores = [0 for _ in range(n_players)]
        self.cities: [City] = []
        self.roads = []
        self.monasteries = []
        self.initialize()

    def initialize(self):
        # Deck initialization
        for tile_type in base_deck.tile_counts:
            ##
            # We want that each tile placements are independent objects.
            self.deck.extend([copy.deepcopy(base_deck.tile_types[tile_type])
                              for _ in range(base_deck.tile_counts[tile_type])])
        random.shuffle(self.deck)
        # print(f"Deck size {len(self.deck)}")

        # Board
        ##
        # TODO: Cleanup // Refactor
        initial_tile = base_deck.tile_types["D"]
        initial_tile.place(Coords(0, 0), 0)
        self.__merge_city_placements(initial_tile, initial_tile.coords)

        self.board = {Coords(0, 0): initial_tile}
        self.freeSquares = [
            Coords(1, 0),
            Coords(-1, 0),
            Coords(0, 1),
            Coords(0, -1)
        ]
        # Initialize citiesTileBorderType
        # Initialize roads
        # Initialize monasteries

    ##
    # Does tile fit into current board at coord / rotation
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

    def get_available_placements(self, tile: Tile):
        placements = []
        for coords in self.freeSquares:
            for rotation in range(4):
                if self.fits(coords, tile, rotation):
                    placements.append((coords, rotation))
        return placements

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

    def __get_connected_city_placement(self, coords: Coords, connection: EdgeOrientation) -> CityPlacement:
        if connection == EdgeOrientation.U:
            if coords.up() in self.board:
                return self.board[coords.up()].cityPlacementMap[EdgeOrientation.D]
            return None
        if connection == EdgeOrientation.D:
            if coords.down() in self.board:
                return self.board[coords.down()].cityPlacementMap[EdgeOrientation.U]
            return None
        if connection == EdgeOrientation.R:
            if coords.right() in self.board:
                return self.board[coords.right()].cityPlacementMap[EdgeOrientation.L]
            return None
        if connection == EdgeOrientation.L:
            if coords.left() in self.board:
                return self.board[coords.left()].cityPlacementMap[EdgeOrientation.R]
            return None

    ##
    # Merge city placements into cities
    def __merge_city_placements(self, tile, coords: Coords):
        placement: CityPlacement

        for placement in tile.cityPlacements:
            self.cities.append(placement.city)
            ##
            # Create city for current cityPlacement, all connected cities will be merged to it.
            connection: EdgeOrientation
            for connection in placement.connections:
                connected_placement = self.__get_connected_city_placement(coords, connection)
                if connected_placement:
                    merged_city = connected_placement.city
                    if merged_city == placement.city:
                        continue
                    placement.city.merge_city(merged_city)
                    self.cities.remove(merged_city)

    def __print_city_list(self):
        print("City list")
        for city in self.cities:
            if not city.completed:
                city.print()
        for city in self.cities:
            if city.completed:
                city.print()

    def insert_tile(self, coords: Coords, tile: Tile, rotation):
        assert coords not in self.board
        assert coords in self.freeSquares

        print(f"(\"{tile.tile_name}\", ({coords.y}, {coords.x}), {rotation}),")

        tile.place(coords, rotation)
        self.__merge_city_placements(tile, coords)
        self.board[coords] = tile
        self.__update_free_squares(coords)

        print("END_INSERT :")
        self.__print_city_list()
        if 0:
            for coords in self.board.keys():
                print(f"@{coords}")
                print(self.board[coords].borders)
