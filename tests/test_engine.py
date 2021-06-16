import pytest

from engine.tile_sets.base_deck import tile_types
from engine.coords import Coords
from engine.game_state import GameState
from engine.game_ui import Gui
import copy


def render_loop(gs):
    gui = Gui()
    gui.draw_game_state(gs)
    gui.tk_root.mainloop()


def insert_tile(gs, tile_name, coord_tuple, rotation):
    coords = Coords(*coord_tuple)
    gs.insert_tile(coords,
                   copy.deepcopy(tile_types[tile_name]),
                   rotation,
                   None
                   )


def insert_tiles(tiles, gs=None):
    if not gs:
        gs = GameState(2)
    for tile in tiles:
        insert_tile(gs, *tile)
    return gs

"""
def test_dummy():
    test_tile_info = [
        ("T", (-1, 0), 1),
        ("O", (0, 1), 1),
    ]
    gs = insert_tiles(test_tile_info)
    for city in gs.cities:
        city.print()
    render_loop(gs)
"""

def test_create_city_1():
    test_tile_info = [
        ("D", (-1, 0), 2),
    ]
    gs = insert_tiles(test_tile_info)

    placements = gs.board.board[Coords(-1, 0)].cityPlacements
    gs.board.board[Coords(-1, 0)].meeplePlacement = placements[0]
    gs.board.board[Coords(-1, 0)].meeplePlayer = 0
    render_loop(gs)
    assert len(gs.cities) == 0

def test_autocompleted_city():
    gs = GameState(2)
    tile = copy.deepcopy(tile_types["D"])
    tile_placements = gs.get_available_tile_placements(tile)
    assert (Coords(-1, 0), 2) in tile_placements
    meeple_placements = gs.get_available_meeple_placements(tile, Coords(-1, 0), 2)
    assert tile.cityPlacements[0] in meeple_placements
    gs.insert_tile(Coords(-1, 0), tile, 2, tile.cityPlacements[0])
    assert gs.scores[0] == 4
    assert gs.meeples[0] == gs.meeples[1]
    assert tile.cityPlacements[0].meeple is None

##
# Place - autocomplete
def test_autocompleted_monastery():
    gs = GameState(2)
    test_tile_info = [
        ("D", (0, 1), 0),
        ("E", (1, 1), 1),
        ("E", (2, 1), 1),
        ("E", (2, 0), 2),
        ("E", (2, -1), 3),
        ("E", (1, -1), 3),
        ("V", (0, -1), 2),
    ]
    gs = insert_tiles(test_tile_info)
    tile = copy.deepcopy(tile_types["B"])
    tile_placements = gs.get_available_tile_placements(tile)
    assert (Coords(1, 0), 0) in tile_placements
    meeple_placements = gs.get_available_meeple_placements(tile, Coords(1, 0), 0)
    assert tile.monasteryPlacement in meeple_placements
    gs.insert_tile(Coords(1, 0), tile, 0, tile.monasteryPlacement)
    assert gs.scores[1] == 8
    assert gs.scores[0] == 0
    assert gs.meeples[0] == gs.meeples[1]
    assert tile.monasteryPlacement.meeple is None

def test_monastery_completion():
    gs = GameState(2)
    tile = copy.deepcopy(tile_types["B"])
    tile_placements = gs.get_available_tile_placements(tile)
    assert (Coords(1, 0), 0) in tile_placements
    meeple_placements = gs.get_available_meeple_placements(tile, Coords(1, 0), 0)
    assert tile.monasteryPlacement in meeple_placements
    gs.insert_tile(Coords(1, 0), tile, 0, tile.monasteryPlacement)
    test_tile_info = [
        ("D", (0, 1), 0),
        ("E", (1, 1), 1),
        ("E", (2, 1), 1),
        ("E", (2, 0), 2),
        ("E", (2, -1), 3),
        ("E", (1, -1), 3),
        ("V", (0, -1), 2),
    ]
    gs = insert_tiles(test_tile_info, gs)
    assert gs.scores[0] == 8
    assert gs.scores[1] == 0
    assert gs.meeples[0] == gs.meeples[1]
    assert tile.monasteryPlacement.meeple is None

"""
def test_available_city_actions():
    test_tile_info = [
        ("K", (-1, 0), 2),
        ("O", (0, 1), 1),
        ("U", (1, 0), 1),
        ("X", (0, -1), 0),
        ("W", (-2, 0), 0),
        ("U", (-1, -1), 0),
        ("F", (0, 2), 0),
        ("S", (-1, 1), 1),
    ]
    gs = insert_tiles(test_tile_info)
    for city in gs.cities:
        city.print()

    render_loop(gs)
    

"""
"""
def test_incomplete_cities():
    test_tile_info = [
        ("R", (1, 0), 2),
        ("N", (2, 0), 0),
        ("O", (1, 1), 3),
        ("D", (1, -1), 1)]
    gs = insert_tiles(test_tile_info)
    render_loop(gs)
    assert len(gs.cities) == 2
"""