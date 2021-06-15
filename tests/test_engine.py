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
                   rotation
                   )


def insert_tiles(tiles):
    gs = GameState(2)
    for tile in tiles:
        insert_tile(gs, *tile)
    return gs


def test_1():
    test_tile_info = [
        ("D", (-1, 0), 2),
    ]
    gs = insert_tiles(test_tile_info)
    render_loop(gs)

    assert len(gs.cities) == 1
    assert gs.cities[0].completed


def test_2():
    test_tile_info = [
        ("R", (1, 0), 2),
        ("N", (2, 0), 0),
        ("O", (1, 1), 3),
        ("D", (1, -1), 1)]
    gs = insert_tiles(test_tile_info)
    render_loop(gs)
    assert len(gs.cities) == 2

