import argparse
import random
from engine.game import Game
from engine.tile import Tile
import copy

def simulate_random_game(game: Game, do_visualize=True, show_score=True):
    s = game.start()
    while len(game.state.deck) > 0:
        tile: Tile = game.get_new_tile()
        tile_placements = game.state.get_available_tile_placements(tile)
        if len(tile_placements) == 0:
            continue
        a = []
        for tile_placement in tile_placements:
            coords, rotation = tile_placement
            meeple_placements = game.state.get_available_meeple_placements(tile, coords, rotation)
            a.append((coords, rotation, meeple_placements))
        random.shuffle(a)
        coords, rotation, meeple_placements = a[0]
        random.shuffle(meeple_placements)
        game.state.insert_tile(coords, tile, rotation, meeple_placements[0])
        if do_visualize:
            game.render()
    game.state.calc_final_score()
    if show_score:
        print("FINAL_SCORE")
        game.state.print_score()


def simulate_games(game: Game):
    for i in range(350):
        game.start()
        print(i)
        simulate_random_game(game, False, False)


if __name__ == "__main__":
    game = Game(create_ui=True)
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
