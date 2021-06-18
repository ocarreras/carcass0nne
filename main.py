import time
import random
from engine.game import Game
from engine.tile import Tile

def visualize_random_game(game):
    game.start()

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
        game.render()
    print("FINAL_SCORE")
    game.state.calc_final_score()
    game.state.print_score()



if __name__ == "__main__":
    game = Game(create_ui=True)
    visualize_random_game(game)
    # game.start()
    # game.interactive()

    #for i in range(0):
    #    random_game(game)
