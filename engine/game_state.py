from engine.tile_sets import base_deck
from engine.tile import Tile, TileBorderType, TileBorderOrientation
import random
import copy

class GameState:
    def __init__(self, n_players):
        self.deck = []
        self.board = {}
        self.freeSquares = {}
        self.scores = [0 for _ in range(n_players)]
        self.cities = []
        self.roads = []
        self.monasteries = []
        self.initialize()

    def initialize(self):
        # Deck initialization
        for tile_type in base_deck.tile_counts:
            self.deck.extend([copy.copy(base_deck.tile_types[tile_type])
                              for _ in range(base_deck.tile_counts[tile_type])])
        random.shuffle(self.deck)
        #print(f"Deck size {len(self.deck)}")

        # Board
        self.board = {(0, 0): base_deck.tile_types["D"]}
        self.freeSquares = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]
        # Initialize cities
        # Initialize roads
        # Initialize monasteries

    def fits(self, coords, tile: Tile):
        assert(coords not in self.board)

        debug = False
        coords_up = (coords[0] - 1, coords[1])
        if coords_up in self.board and \
                self.board[coords_up].get_border(TileBorderOrientation.DOWN) != \
                tile.get_border(TileBorderOrientation.UP):
            return False
        if debug and coords_up in self.board:
            print(f"UP: {self.board[coords_up].get_border(TileBorderOrientation.DOWN)} - {tile.get_border(TileBorderOrientation.UP)}")

        coords_down = (coords[0] + 1, coords[1])
        if coords_down in self.board and \
                self.board[coords_down].get_border(TileBorderOrientation.UP) != \
                tile.get_border(TileBorderOrientation.DOWN):
            return False
        if debug and coords_down in self.board:
            print(f"DW: {self.board[coords_down].get_border(TileBorderOrientation.UP)} - {tile.get_border(TileBorderOrientation.DOWN)}")

        coords_right = (coords[0], coords[1] + 1)
        if coords_right in self.board and \
                self.board[coords_right].get_border(TileBorderOrientation.LEFT) != \
                tile.get_border(TileBorderOrientation.RIGHT):
            return False
        if debug and coords_right in self.board:
            print(f"RG: {self.board[coords_right].get_border(TileBorderOrientation.LEFT)} - {tile.get_border(TileBorderOrientation.RIGHT)}")

        coords_left = (coords[0], coords[1] - 1)
        if coords_left in self.board and \
                self.board[coords_left].get_border(TileBorderOrientation.RIGHT) != \
                tile.get_border(TileBorderOrientation.LEFT):
            return False
        if debug and coords_left in self.board:
            print(f"LF: {self.board[coords_left].get_border(TileBorderOrientation.RIGHT)} - {tile.get_border(TileBorderOrientation.LEFT)}")
        return True

    def insert_tile(self, coords, tile: Tile):
        assert coords not in self.board
        assert coords in self.freeSquares

        self.freeSquares.remove(coords)
        self.board[coords] = tile
        coords_up = (coords[0] - 1, coords[1])
        coords_down = (coords[0] + 1, coords[1])
        coords_right = (coords[0], coords[1] + 1)
        coords_left = (coords[0], coords[1] - 1)
        if coords_up not in self.board and coords_up not in self.freeSquares:
            self.freeSquares.append(coords_up)
        if coords_down not in self.board and coords_down not in self.freeSquares:
            self.freeSquares.append(coords_down)
        if coords_right not in self.board and coords_right not in self.freeSquares:
            self.freeSquares.append(coords_right)
        if coords_left not in self.board and coords_left not in self.freeSquares:
            self.freeSquares.append(coords_left)

        # self.freeSquares.sort()
        # random.shuffle(self.freeSquares)

