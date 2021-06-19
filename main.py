import argparse
import random
from engine.game import Game
from engine.tile import Tile
import copy

@profile
def simulate_random_game(game, do_visualize=True, show_score=True):
    s = game.start()
    while len(game.state.deck) > 0:
        tile: Tile = game.get_new_tile()
        tile_placements = game.state.get_available_tile_placements(tile)
        if len(tile_placements) == 0:
            continue
        random.shuffle(tile_placements)
        coords, rotation = tile_placements[0]
        meeple_placements = game.state.get_available_meeple_placements(tile, coords, rotation)
        random.shuffle(meeple_placements)
        meeple_placement = meeple_placements[0] if len(meeple_placements) > 0 else None
        game.state.insert_tile(coords, tile, rotation, meeple_placement)
        if do_visualize:
            game.render()
    if show_score:
        print("FINAL_SCORE")
        game.state.calc_final_score()
        game.state.print_score()


def simulate_games(game):
    for i in range(50):
        game.start()
        print(i)
        simulate_random_game(game, False, False)


if __name__ == "__main__":
    game = Game(create_ui=True)
    parser = argparse.ArgumentParser(description="Simple program to test gui/engine")
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
