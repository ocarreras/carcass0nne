import time
import random
from engine.game import Game
from engine.tile import Tile

def fit_tile(game, tile):
    for coords in game.state.freeSquares:
        for rotation in range(4):
            tile.rotation = rotation
            if game.state.fits(coords, tile):
                return coords

def get_placements(game, tile):
    placements = []

    for coords in game.state.freeSquares:
        for rotation in range(4):
            tile.rotation = rotation
            if game.state.fits(coords, tile):
                placements.append((coords, rotation))
    #print(placements)
    return placements


if __name__ == "__main__":

    game = Game()
    for i in range(1):
        game.reset()
        while len(game.state.deck) > 0:
            tile: Tile = game.get_new_tile()
            placements = get_placements(game, tile)
            if len(placements) == 0:
                # Cannot set tile
                continue
            print(tile.borders)
            print(len(placements))
            random.shuffle(placements)
            coords, rotation = placements[0]
            tile.rotation = rotation
            #print(f"Inserting {coords}")
            game.state.insert_tile(coords, tile)
        game.render()
        #for coord in game.state.board:
        #    print(f"{coord} - {game.state.board[coord]}")
    game.gui.tk_root.mainloop()
    print("Done")


