import time
import random
from engine.game import Game
from engine.tile import Tile

if __name__ == "__main__":
    game = Game()
    for i in range(100):
        game.reset()

        while len(game.state.deck) > 0:
            tile: Tile = game.get_new_tile()
            placements = game.state.get_available_placements(tile)
            if len(placements) == 0:
                continue
            #random.shuffle(placements)
            coords, rotation = placements[0]
            game.state.insert_tile(coords, tile, rotation)
        game.render()
        #game.gui.tk_root.mainloop()
    print("Done")

