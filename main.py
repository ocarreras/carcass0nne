import argparse
import random
from engine.game import Game
from engine.game_state import GameState
from engine.tile import Tile
import copy

#@profile
def simulate_random_game(game:Game, game_state: GameState, do_visualize=True, show_score=True):
    while len(game_state.deck) > 0:
        tile: Tile = game_state.get_new_tile()
        tile_placements = game_state.get_available_tile_placements(tile)
        if len(tile_placements) == 0:
            continue
        a = []
        for tile_placement in tile_placements:
            coords, rotation = tile_placement
            meeple_placements = game_state.get_available_meeple_placements(tile, coords, rotation)
            a.append((coords, rotation, meeple_placements))
        random.shuffle(a)
        coords, rotation, meeple_placements = a[0]
        random.shuffle(meeple_placements)
        game_state.insert_tile(coords, tile, rotation, meeple_placements[0])
        if do_visualize:
            game.render()
    game_state.calc_final_score()
    if show_score:
        print("FINAL_SCORE")
        game_state.print_score()


def simulate_games(game: Game):
    game.start()
    for i in range(50):
        simulate_random_game(game, game.state.copy(), False, True)


if __name__ == "__main__":
    game = Game(create_ui=True, debug=1)
    parser = argparse.ArgumentParser(description="Simple program to test gui/etime python Carcassonne.py 1 350ngine")
    parser.add_argument('--mode', help='[random|interactive].', default='random')
    args = parser.parse_args()
    if args.mode == "random":
        #simulate_random_game(game)
        simulate_games(game)
    elif args.mode == "interactive":
        game.start()
        game.interactive()
    else:
        parser.print_help()
