from typing import Dict
from engine.tile_sets import base_deck
from engine.tile import Tile
from engine.city import CityPlacement
from engine.road import RoadPlacement
from engine.field import FieldPlacement
from engine.monastery import MonasteryPlacement
from engine.coords import Coords
from engine.placement import EdgeConnection, Placement, ShapeType
from engine.board import Board

import random
import numpy as np

import copy

class GameState:
    def __init__(self, n_players, tile_counts=base_deck.tile_counts, debug=0):
        self.n_players = n_players
        self.current_player = 0
        self.deck: [Tile] = None
        self.board: Board = None
        self.scores: [int] = None
        self.score_types: Dict[ShapeType, Dict[int, int]] = None
        self.meeples: [int] = None
        self.unfinished_shapes: Dict[ShapeType, list] = None
        self.debug_level = 0
        self.canonical_player = 1
        self.tile_counts = tile_counts
        self.ML_AUX_SIZE = 5
        self.next_tile: Tile = None
        self.past_actions = []
        self.initialize(tile_counts)

    def __get_copied_placement(self, my_copy, self_placement):
        if self_placement is None:
            return None
        copy_tile: Tile = my_copy.board[self_placement.coords]
        self_tile: Tile = self.board[self_placement.coords]
        return copy_tile.get_placement_by_ind(self_tile.placement_ind(self_placement))

    ##
    # TODO: This method is a total disaster, rethink it.
    #
    def copy(self):
        # Workaround until fix
        return copy.deepcopy(self)
        my_copy: GameState = GameState(self.n_players, self.tile_counts)
        my_copy.current_player = self.current_player
        my_copy.deck = []
        for tile in self.deck:
            my_copy.deck.append(tile.copy())

        ##
        # TODO: The horror ...
        my_copy.board = self.board.copy()
        for key in my_copy.board.board:
            copy_tile: Tile = my_copy.board[key]
            self_tile: Tile = self.board[key]

            for shape_type in ShapeType:
                for copy_placement in copy_tile.placements[shape_type]:
                    connected_placement: Placement = copy_placement.connected_placement
                    new_connected_placement = self.__get_copied_placement(my_copy, connected_placement)
                    copy_placement.connected_placement = new_connected_placement
                    new_shape_placements = []
                    for old_shape_placement in copy_placement.shape_placements:
                        new_shape_placement = self.__get_copied_placement(my_copy, old_shape_placement)
                        new_shape_placements.append(new_shape_placement)
                    copy_placement.shape_placements = new_shape_placements

            copy_tile.connections = {}
            for shape_type in self_tile.connections:
                copy_tile.connections[shape_type] = {}
                for connection in self_tile.connections[shape_type]:
                    new_placement = self.__get_copied_placement(my_copy, self_tile.connections[shape_type][connection])
                    copy_tile.connections[shape_type][connection] = new_placement


        my_copy.score_types = {}
        for score_type in self.score_types:
            my_copy.score_types[score_type] = self.score_types[score_type].copy()
        self.score_types.copy()

        my_copy.scores = self.scores.copy()
        my_copy.meeples = self.meeples.copy()
        my_copy.unfinished_shapes = {}
        ##
        # TODO: Horror
        for shape_type in self.unfinished_shapes:
            my_copy.unfinished_shapes[shape_type] = []
            for placement in self.unfinished_shapes[shape_type]:
                placement_copy = self.__get_copied_placement(my_copy, placement)
                my_copy.unfinished_shapes[shape_type].append(placement_copy)

        my_copy.debug_level = self.debug_level
        my_copy.next_tile = self.next_tile
        my_copy.past_actions = self.past_actions.copy()
        return my_copy

    def initialize(self, tile_counts=base_deck.tile_counts):
        self.scores = [0 for _ in range(self.n_players)]
        self.score_types = {}
        for shape_type in ShapeType:
            self.score_types[shape_type] = [0 for _ in range(self.n_players)]
        self.meeples = [7 for _ in range(self.n_players)]
        self.current_player = 0
        self.unfinished_shapes = {
            ShapeType.CITY: [],
            ShapeType.ROAD: [],
            ShapeType.MONASTERY: [],
            ShapeType.FIELD: []
        }
        # Deck initialization
        self.deck = []
        for tile_type in base_deck.tile_counts:
            # We need to duplicate all objects to avoid multiple references.
            self.deck.extend([base_deck.tile_types[tile_type].copy()
                              for _ in range(tile_counts[tile_type])])
        random.shuffle(self.deck)

        # Inserting first tile and initializing board
        initial_tile = base_deck.tile_types["D"]
        self.board = Board()
        self.board.init(Coords(0, 0), initial_tile)
        initial_tile.place(self.board, Coords(0, 0), 0, self.n_players)
        self.__insert_and_merge_shapes(ShapeType.CITY, initial_tile, initial_tile.coords)
        self.__insert_and_merge_shapes(ShapeType.ROAD, initial_tile, initial_tile.coords)
        self.__insert_and_merge_shapes(ShapeType.FIELD, initial_tile, initial_tile.coords)
        self.get_new_tile()

    def ml_get_aux(self):
        aux = np.zeros(self.ML_AUX_SIZE)
        if self.canonical_player == -1:
            aux[0:2] = self.scores[::-1]
            aux[2:4] = self.meeples[::-1]
        else:
            aux[0:2] = self.scores
            aux[2:4] = self.meeples
        aux[4] = (self.next_tile.tile_num() if self.next_tile else 0)
        return aux

    def ml_get_board(self):
        return self.board.ml_board_s0

    ##
    # TODO: Finish this, just placeholder
    def ml_get_action_id(self, tile, coords, rotation, meeple_placement):
        move_ind = tile.placement_ind(meeple_placement)
        move_ind += rotation * self.board.ML_BOARD_FEATURES
        move_ind += (coords.x + self.board.ML_BOARD_SIZE//2) * 4 * self.board.ML_BOARD_FEATURES
        move_ind += (coords.y + self.board.ML_BOARD_SIZE//2) * 4 * self.board.ML_BOARD_FEATURES * self.board.ML_BOARD_SIZE
        return move_ind

    def ml_get_action_params(self, action_id):
        mult = self.board.ML_BOARD_SIZE * self.board.ML_BOARD_FEATURES * 4
        coord_y = action_id // mult
        action_id = action_id - (coord_y*mult)
        mult /= self.board.ML_BOARD_SIZE
        coord_x = action_id // mult
        action_id = action_id - (coord_x*mult)
        mult /= 4
        rotation = action_id // mult
        placement_id = action_id - (rotation*mult)
        return int(coord_y) - self.board.ML_BOARD_SIZE//2, int(coord_x) - self.board.ML_BOARD_SIZE//2, \
               int(rotation), int(placement_id)

    def ml_action(self, action_id):

        coord_y, coord_x, ml_rotation, placement_id = self.ml_get_action_params(action_id)
        self.past_actions.append([self.next_tile.tile_num(), coord_y, coord_x, ml_rotation, placement_id])
        # print("Past")
        # for action in self.past_actions:
        #    print(action)
        ml_coords = Coords(coord_y, coord_x)
        ml_placement = self.next_tile.get_placement_by_ind(placement_id)
        self.insert_tile(ml_coords, self.next_tile, ml_rotation, ml_placement)

    def get_new_tile(self):
        if self.next_tile:
            return self.next_tile
        while True:
            if len(self.deck) == 0:
                self.next_tile = None
                return None
            self.next_tile = self.deck.pop()
            if len(self.get_available_tile_placements(self.next_tile)):
                return self.next_tile

    def calc_final_score(self):
        for shape_type in ShapeType:
            while len(self.unfinished_shapes[shape_type]) > 0:
                unfinished_shape = self.unfinished_shapes[shape_type][0]
                self.__score_shape(shape_type, unfinished_shape)

    def print_score(self):
        print("[[ SCORES ]]")
        for player_num in range(self.n_players):
            print(f"Player: {player_num:02d}")
            print(f"\tSCORE: {self.scores[player_num]}")
            for shape_type in ShapeType:
                print(f"\t\t{shape_type.name:10}: {self.score_types[shape_type][player_num]}")

    ##
    # Get available tile placements.
    def get_available_tile_placements(self, tile: Tile) -> [(Coords, int)]:
        return self.board.get_available_tile_placements(tile)

    ##
    # Get a list of all legal meeple placements + an additional None entry for no placement.
    def get_available_meeple_placements(self, tile: Tile, coords: Coords, rotation: int):
        placements = [None]
        if self.meeples[self.current_player] == 0:
            return placements
        placements.extend(self.__get_city_meeple_placements(tile, coords, rotation))
        placements.extend(tile.placements[ShapeType.MONASTERY])
        placements.extend(self.__get_road_meeple_placements(tile, coords, rotation))
        placements.extend(self.__get_field_meeple_placements(tile, coords, rotation))
        return placements

    def __score_shape(self, shape_type: ShapeType, placement: Placement):
        score = placement.score()
        winners = placement.winners()
        for winner in winners:
            if self.debug_level > 2:
                print(f"SCORING: {shape_type} :: {score} -> {winner}")
            self.scores[winner] += score
            self.score_types[shape_type][winner] += score
        for shape_placement in placement.shape_placements:
            if shape_placement.meeple is not None:
                self.meeples[shape_placement.meeple] += 1
                self.__remove_meeple(shape_placement)
        placement.reset_meeples(self.n_players)
        if self.debug_level > 4:
            print(f"REMOVE SHAPE @ SCORE :: {shape_type} :: {placement}")
        self.unfinished_shapes[shape_type].remove(placement)

    def __insert_and_merge_shapes(self, shape_type: ShapeType, tile: Tile, coords: Coords):
        if self.debug_level > 4:
            print(f"\n\nMERGE - START - {shape_type} - {coords} - {tile}")
        for placement in tile.placements[shape_type]:
            if self.debug_level > 4:
                print(f"ADD SHAPE :: {shape_type} :: {placement}")
            self.unfinished_shapes[shape_type].append(placement)

            connection: EdgeConnection
            for connection in placement.connections:
                merged_placement = self.board.get_connected_placement(shape_type, coords, connection)
                if not merged_placement:
                    continue
                while merged_placement != merged_placement.connected_placement:
                    merged_placement = merged_placement.connected_placement
                if merged_placement and merged_placement != placement:
                    completed = placement.merge(merged_placement)
                    if completed:
                        self.__score_shape(shape_type, placement)
                    if self.debug_level > 4:
                        print(f"REMOVE SHAPE @ MERGE :: {shape_type} :: {merged_placement}")
                    self.unfinished_shapes[shape_type].remove(merged_placement)
        if self.debug_level > 4:
            print(f"MERGE - END - UNFINISHED SHAPES")
            for placement in self.unfinished_shapes[shape_type]:
                print(f"\t{placement}")

    def __update_monasteries(self, tile: Tile, coords: Coords):
        for monastery in self.unfinished_shapes[ShapeType.MONASTERY]:
            monastery_coords = monastery.coords
            if monastery.coords == coords:
                continue

            if abs(monastery_coords.x - coords.x) <= 1 and \
                    abs(monastery_coords.y - coords.y) <= 1:
                monastery.inc_neighbours()
                if monastery.completed:
                    self.__score_shape(ShapeType.MONASTERY, monastery)
        for placement in tile.placements[ShapeType.MONASTERY]:
            if placement.completed:
                self.__score_shape(ShapeType.MONASTERY, placement)

    def __insert_meeple(self, tile: Tile, placement: Placement):
        if not placement:
            return
        self.meeples[self.current_player] -= 1
        placement.meeple = self.current_player
        placement.meeples[self.current_player] += 1
        ##
        # ML-Board state
        m_ind = tile.placement_ind(placement)
        assert m_ind != -1
        if m_ind:
            ml_player = (-1) ** self.current_player
            self.board.insert_meeple_ml(tile.coords, m_ind, ml_player)

    def __remove_meeple(self, placement: Placement):
        placement.meeple = None
        ##
        # ML-Board state
        # TODO - This should be done better but would require changes on the models
        tile = self.board[placement.coords]
        m_ind = tile.placement_ind(placement)
        assert m_ind != -1 and m_ind != 0
        self.board.remove_meeple_ml(placement.coords, m_ind)

    def insert_tile(self, coords: Coords, tile: Tile, rotation: int, placement: Placement):
        assert self.next_tile == tile
        assert coords not in self.board

        self.next_tile = None

        if self.debug_level > 0:
            print(f"(\"{tile.tile_type}\", ({coords.y}, {coords.x}), {rotation}),")

        tile.place(self.board, coords, rotation, self.n_players)
        self.board.insert_tile(coords, tile)

        if placement:
            self.__insert_meeple(tile, placement)

        self.__insert_and_merge_shapes(ShapeType.CITY, tile, coords)
        self.__insert_and_merge_shapes(ShapeType.ROAD, tile, coords)
        self.__insert_and_merge_shapes(ShapeType.MONASTERY, tile, coords)
        self.__insert_and_merge_shapes(ShapeType.FIELD, tile, coords)
        self.__update_monasteries(tile, coords)

        self.current_player = (self.current_player + 1) % self.n_players

    def print_open_shapes(self):
        print("OPEN SHAPES")
        print(f"[[ CITY LIST      : {len(self.unfinished_shapes[ShapeType.CITY]):03d}]]")
        for city in self.unfinished_shapes[ShapeType.CITY]:
            assert not city.completed
            city.print()
        print(f"[[ ROAD LIST      : {len(self.unfinished_shapes[ShapeType.ROAD]):03d}]]")
        for road in self.unfinished_shapes[ShapeType.ROAD]:
            assert not road.completed
            road.print()
        print(f"[[ MONASTERY LIST : {len(self.unfinished_shapes[ShapeType.MONASTERY]):03d} ]]")
        for monastery in self.unfinished_shapes[ShapeType.MONASTERY]:
            assert not monastery.completed
            monastery.print()
        print(f"[[ FIELD LIST     : {len(self.unfinished_shapes[ShapeType.FIELD]):03d} ]]")
        for field in self.unfinished_shapes[ShapeType.FIELD]:
            field.print()
            print(f"\tScore: {field.score()}")
            print("\tAdjacent cities")
            for city in field.adjacent_cities():
                print(f"\t\t{city}")

    ##
    # TODO: Experimental
    def __get_field_meeple_placements(self, tile: Tile, coords: Coords, rotation: int) -> [FieldPlacement]:
        placements = []

        for placement in tile.placements[ShapeType.FIELD]:
            empty = True
            for connection in placement.connections:
                connected_road = self.board.get_connected_placement(ShapeType.FIELD, coords, (connection + rotation * 2) % 8)
                if not connected_road:
                    continue
                n_meeples = sum(connected_road.meeples)
                if n_meeples != 0:
                    empty = False
                    break
            if empty:
                placements.append(placement)
        return placements

    ##
    # TODO: Two road placements could connect to the same road. These two placements would give the same outcome
    #       Needs Fix to improve search.
    #         _____________
    #        |-RP1 X RP2 -|
    def __get_road_meeple_placements(self, tile: Tile, coords: Coords, rotation: int) -> [RoadPlacement]:
        placements = []

        for placement in tile.placements[ShapeType.ROAD]:
            empty = True
            for connection in placement.connections:
                connected_road = self.board.get_connected_placement(ShapeType.ROAD, coords, (connection + 2*rotation) % 8)
                if not connected_road:
                    continue
                n_meeples = sum(connected_road.meeples)
                if n_meeples != 0:
                    empty = False
                    break
            if empty:
                placements.append(placement)
        return placements

    ##
    # Return a list of unique city placements:
    #
    # - If two placements connect to the same city, return only one.
    # - All connected cities must be empty.
    #
    # There are some difficulties if we want to do this before tile placement, thus before merging cities.
    #
    # For instance, tiles similar to "EP" on inns and cathedrals could merge a city that
    # initially didn't have meeples with one that has:
    #
    #   ABC    B   : city w Meeple
    #   DEF    FHI : city w/o Meeple
    #   GHI    E   : Tile with two city placements:
    #                  - 1: Connects down with FHI, and has no meeple
    #                  - 2: Connects up to B and right to EFH.
    #
    # TODO: This shouldn't be a problem with the initial tile_set, but should be fixed if we want
    #       to support inns and cathedrals.
    #
    # The basic tile_set doesn't have any tile with multiple placements where one of them merges cities.
    #
    # TODO: Returning CityPlacement temporarily
    def __get_city_meeple_placements(self, tile: Tile, coords: Coords, rotation) -> [CityPlacement]:
        placements = []

        for placement in tile.placements[ShapeType.CITY]:
            empty = True
            for connection in placement.connections:
                connected_city = self.board.get_connected_placement(ShapeType.CITY, coords, (connection + 2*rotation) % 8)
                if not connected_city:
                    continue
                n_meeples = sum(connected_city.meeples)
                if n_meeples != 0:
                    empty = False
                    break
            if empty:
                # TODO: Check if we connect to the same city as another placement.
                placements.append(placement)
        return placements
