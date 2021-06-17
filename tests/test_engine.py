import pytest

from engine.tile_sets.base_deck import tile_types
from engine.coords import Coords
from engine.game_state import GameState
from engine.game_ui import Gui
from engine.shape import Shape, ShapeType
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
##
# Create road donut and complete it with a single tile while scoring.
def test_road_connection():
    gs = GameState(2)
    test_tile_info = [
        ("V", (0, 1), 0),
        ("V", (1, 1), 1),
        ("V", (0, -1), 3),
        ("V", (1, -1), 2),
        ("U", (1, 0), 1),
    ]
    insert_tiles(test_tile_info, gs)
    print("UNFINISHED ROADS")
    for road in gs.unfinished_shapes[ShapeType.ROAD]:
        road.print()
    render_loop(gs)
"""


def test_autocompleted_city():
    gs = GameState(2)
    tile = copy.deepcopy(tile_types["D"])
    for road in gs.unfinished_shapes[ShapeType.ROAD]:
        road.print()
    tile_placements = gs.get_available_tile_placements(tile)
    assert (Coords(-1, 0), 2) in tile_placements
    meeple_placements = gs.get_available_meeple_placements(tile, Coords(-1, 0), 2)
    assert tile.placements[ShapeType.CITY][0] in meeple_placements
    gs.insert_tile(Coords(-1, 0), tile, 2, tile.placements[ShapeType.CITY][0])
    assert gs.scores[0] == 4
    assert gs.meeples[0] == gs.meeples[1]
    assert tile.placements[ShapeType.CITY][0].meeple is None


def create_monastery_donut(gs):
    test_tile_info = [
        ("D", (0, 1), 0),
        ("E", (1, 1), 1),
        ("E", (2, 1), 1),
        ("E", (2, 0), 2),
        ("E", (2, -1), 3),
        ("E", (1, -1), 3),
        ("V", (0, -1), 2),
    ]
    insert_tiles(test_tile_info, gs)


def test_autocompleted_monastery():
    gs = GameState(2)
    create_monastery_donut(gs)
    tile = copy.deepcopy(tile_types["B"])
    tile_placements = gs.get_available_tile_placements(tile)
    assert (Coords(1, 0), 0) in tile_placements
    meeple_placements = gs.get_available_meeple_placements(tile, Coords(1, 0), 0)
    monastery_placement = tile.placements[ShapeType.MONASTERY][0]
    assert monastery_placement in meeple_placements
    gs.insert_tile(Coords(1, 0), tile, 0, monastery_placement)
    assert gs.scores[1] == 9
    assert gs.scores[0] == 0
    assert gs.meeples[0] == gs.meeples[1]
    assert monastery_placement.meeple is None
    gs.print_open_shapes()
    render_loop(gs)

def test_monastery_completion():
    gs = GameState(2)
    tile = copy.deepcopy(tile_types["B"])
    meeple_placements = gs.get_available_meeple_placements(tile, Coords(1, 0), 0)
    monastery_placement = tile.placements[ShapeType.MONASTERY][0]
    assert monastery_placement in meeple_placements
    gs.insert_tile(Coords(1, 0), tile, 0, monastery_placement)
    create_monastery_donut(gs)
    assert gs.scores[0] == 9
    assert gs.scores[1] == 0
    assert gs.meeples[0] == gs.meeples[1]
    assert monastery_placement.meeple is None


##
# Create road donut and complete it with a single tile while scoring.
def test_autocomplete_road():
    gs = GameState(2)
    test_tile_info = [
        ("V", (0, 1), 0),
        ("V", (1, 1), 1),
        ("V", (0, -1), 3),
        ("V", (1, -1), 2),
    ]
    insert_tiles(test_tile_info, gs)
    tile = copy.deepcopy(tile_types["U"])
    road_placement = tile.placements[ShapeType.ROAD][0]
    tile_placements = gs.get_available_tile_placements(tile)
    assert (Coords(1, 0), 1) in tile_placements
    meeple_placements = gs.get_available_meeple_placements(tile, Coords(1, 0), 0)
    assert road_placement in meeple_placements
    gs.insert_tile(Coords(1, 0), tile, 1, road_placement)
    assert gs.scores[0] == 6
    assert gs.scores[1] == 0
    assert gs.meeples[0] == gs.meeples[1]
    assert road_placement.meeple is None


##
# Place meeple in a road and complete it doing a circle/donut.
def test_road_completion():
    gs = GameState(2)
    tile = copy.deepcopy(tile_types["V"])
    tile_placements = gs.get_available_tile_placements(tile)
    road_placement = tile.placements[ShapeType.ROAD][0]
    assert (Coords(0, 1), 0) in tile_placements
    meeple_placements = gs.get_available_meeple_placements(tile, Coords(0, 1), 0)
    assert road_placement in meeple_placements
    gs.insert_tile(Coords(0, 1), tile, 0, road_placement)
    test_tile_info = [
        ("V", (1, 1), 1),
        ("V", (0, -1), 3),
        ("V", (1, -1), 2),
        ("U", (1, 0), 1)
    ]
    insert_tiles(test_tile_info, gs)
    assert gs.scores[0] == 6
    assert gs.scores[1] == 0
    assert gs.meeples[0] == gs.meeples[1]
    assert road_placement.meeple is None
