import time
import random
from engine.game import Game
from engine.tile import Tile

def do_main(game):
    while len(game.state.deck) > 0:
        tile: Tile = game.get_new_tile()
        tile_placements = game.state.get_available_tile_placements(tile)
        if len(tile_placements) == 0:
            continue
        #random.shuffle(tile_placements)
        coords, rotation = tile_placements[0]
        meeple_placements = game.state.get_available_meeple_placements(tile, coords, rotation)
        random.shuffle(meeple_placements)
        meeple_placement = meeple_placements[0] if len(meeple_placements) > 0 else None
        game.state.insert_tile(coords, tile, rotation, meeple_placement)

        #game.render()
        #time.sleep(0.5)
    #game.state.print_open_shapes()
    print("FINAL_SCORE")
    game.state.calc_final_score()
    game.state.print_score()
    print("LEFT")
    #game.gui.tk_root.mainloop()

if __name__ == "__main__":
    game = Game(create_ui=True)

    for i in range(30):
        game.start()
        do_main(game)
