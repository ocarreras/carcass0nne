from engine.tile_sets import base_deck
from engine.tile import Tile
from engine.city import CityPlacement, City
from engine.road import RoadPlacement, Road
from engine.monastery import MonasteryPlacement
from engine.coords import Coords
from engine.placement import EdgeOrientation, Placement
from engine.board import Board
from enum import IntEnum

import random
import copy


class GameState:
    def __init__(self, n_players):
        self.n_players = n_players
        self.current_player = 0
        self.deck: [Tile] = []
        self.board: Board = None
        self.scores: [int] = []
        self.meeples: [int] = []
        self.cities: [City] = []
        self.monasteries: [MonasteryPlacement] = []
        self.roads = []
        self.monasteries = []
        self.initialize()

    def initialize(self):
        self.scores = [0 for _ in range(self.n_players)]
        self.meeples = [7 for _ in range(self.n_players)]
        self.current_player = 0

        # Deck initialization
        for tile_type in base_deck.tile_counts:
            # We need to duplicate all objects to avoid multiple references.
            self.deck.extend([copy.deepcopy(base_deck.tile_types[tile_type])
                              for _ in range(base_deck.tile_counts[tile_type])])
        random.shuffle(self.deck)

        # Inserting first tile and initializing board
        initial_tile = base_deck.tile_types["D"]
        self.board = Board(Coords(0, 0), initial_tile)
        initial_tile.place(self.board, Coords(0, 0), 0, self.n_players)
        self.__insert_and_merge_cities(initial_tile, initial_tile.coords)
        self.__insert_and_merge_roads(initial_tile, initial_tile.coords)

    ##
    # Get available tile placements.
    def get_available_tile_placements(self, tile: Tile) -> [(Coords, int)]:
        placements = []
        for coords in self.board.freeSquares:
            for rotation in range(4):
                if self.board.fits(coords, tile, rotation):
                    placements.append((coords, rotation))
        return placements

    ##
    # Get a list of all legal meeple placements + an additional None entry for no placement.
    def get_available_meeple_placements(self, tile: Tile, coords: Coords, rotation: int):
        placements = [None]
        if self.meeples[self.current_player] == 0:
            return placements

        # placements.extend(self.__get_city_meeple_placements(tile, coords, rotation))
        # if tile.monasteryPlacement:
        #    placements.append(tile.monasteryPlacement)
        placements.extend(self.__get_road_meeple_placements(tile, coords, rotation))
        return placements

    ##
    # TODO: Two road placements could connect to the same road. These two placements would give the same outcome    #
    #       Needs Fix to improve search.
    #         _____________
    #        |-RP1 X RP2 -|
    def __get_road_meeple_placements(self, tile: Tile, coords: Coords, rotation: int) -> [RoadPlacement]:
        placements = []

        for placement in tile.roadPlacements:
            empty = True
            for connection in placement.connections:
                connected_road = self.board.get_connected_road(coords, (connection+rotation) % 4)
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
    # Return a list of unique city actions:
    #
    # - If two placements connect to the same city, return only one action.
    # - All connected cities must be empty.
    #
    # There are some difficulties if we want to do this before tile placement, thus before merging cities.
    #
    # For instance, tiles similar to "EP" on inns and cathedrals could merge a city that
    # initially didn't have meeples with a city that has:
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
    def __get_city_meeple_placements(self, tile:Tile, coords: Coords, rotation) -> [CityPlacement]:
        placements = []

        for placement in tile.cityPlacements:
            empty = True
            for connection in placement.connections:
                connected_city = self.board.get_connected_city(coords, (connection+rotation) % 4)
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

    ##
    # TODO: Refactor w road
    def __score_city(self, city: City):
        city_score = city.score()
        winners = city.winners()
        for winner in winners:
            self.scores[winner] += city_score
        placement: CityPlacement
        for placement in city.placements:
            if placement.meeple is not None:
                self.meeples[placement.meeple] += 1
                placement.meeple = None
        city.reset_meeples(self.n_players)
        self.cities.remove(city)

    ##
    # TODO: Refactor w city
    def __score_road(self, road: Road):
        road_score = road.score()
        winners = road.winners()
        for winner in winners:
            self.scores[winner] += road_score
        placement: RoadPlacement
        for placement in road.placements:
            if placement.meeple is not None:
                self.meeples[placement.meeple] += 1
                placement.meeple = None
        road.reset_meeples(self.n_players)
        self.roads.remove(road)

    def __score_monastery(self, monastery: MonasteryPlacement):
        if monastery.meeple is not None:
            self.scores[monastery.meeple] += monastery.score
            self.meeples[monastery.meeple] += 1
            monastery.meeple = None

    ##
    # TODO: Very similar to roads -> Refactor.
    def __insert_and_merge_cities(self, tile: Tile, coords: Coords):
        placement: CityPlacement
        for placement in tile.cityPlacements:
            self.cities.append(placement.city)
            connection: EdgeOrientation
            for connection in placement.connections:
                merged_city = self.board.get_connected_city(coords, connection)
                if merged_city:
                    if merged_city == placement.city:
                        continue
                    completed = placement.city.merge_city(merged_city)
                    if completed:
                        self.__score_city(placement.city)
                    self.cities.remove(merged_city)

    ##
    # TODO: Very similar to cities -> Refactor.
    def __insert_and_merge_roads(self, tile: Tile, coords: Coords):
        placement: RoadPlacement
        for placement in tile.roadPlacements:
            self.roads.append(placement.road)
            connection: EdgeOrientation
            for connection in placement.connections:
                merged_road = self.board.get_connected_road(coords, connection)
                if merged_road:
                    if merged_road == placement.road:
                        continue
                    completed = placement.road.merge_road(merged_road)
                    if completed:
                        self.__score_road(placement.road)
                    self.roads.remove(merged_road)

    ##
    # Update score on the neighbour monasteries
    def __insert_and_update_monasteries(self, tile: Tile, coords: Coords):
        if tile.monasteryPlacement:
            self.monasteries.append(tile.monasteryPlacement)

        neighbours = [
            coords.up(), coords.down(), coords.up().left(), coords.up().right(),
            coords.left(), coords.right(), coords.down().left(), coords.down().right()
        ]
        for neighbour in neighbours:
            if neighbour in self.board.board:
                placement: MonasteryPlacement = self.board.board[neighbour].monasteryPlacement
                if placement:
                    placement.inc_score()
                    if placement.completed:
                        print("SCORING monastery")
                        self.__score_monastery(placement)

    def __insert_meeple(self, tile: Tile, placement: Placement):
        assert self.meeples[self.current_player] > 0
        if not placement:
            return
        self.meeples[self.current_player] -= 1
        placement.meeple = self.current_player
        if type(placement) == CityPlacement:
            placement: CityPlacement
            placement.city.meeples[self.current_player] += 1
        if type(placement) == MonasteryPlacement:
            placement: MonasteryPlacement
            placement.meeple = self.current_player
            if placement.completed:
                self.__score_monastery(placement)
        if type(placement) == RoadPlacement:
            placement: RoadPlacement
            placement.road.meeples[self.current_player] += 1

    def insert_tile(self, coords: Coords, tile: Tile, rotation: int, placement: Placement):
        assert coords not in self.board.board
        assert coords in self.board.freeSquares

        print(f"(\"{tile.tile_name}\", ({coords.y}, {coords.x}), {rotation}),")

        tile.place(self.board, coords, rotation, self.n_players)
        self.board.insert_tile(coords, tile)

        if placement:
            self.__insert_meeple(tile, placement)

        self.__insert_and_merge_cities(tile, coords)
        self.__insert_and_merge_roads(tile, coords)
        self.__insert_and_update_monasteries(tile, coords)

        self.current_player = (self.current_player + 1) % self.n_players

    def __print_city_list(self):
        print("City list")
        for city in self.cities:
            if not city.completed:
                city.print()
        for city in self.cities:
            if city.completed:
                city.print()
