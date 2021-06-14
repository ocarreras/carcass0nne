import time
from engine.game import Game

def fit_tile(game, tile):
    for coords in game.state.freeSquares:
        for rotation in range(4):
            tile.rotation = rotation
            if game.state.fits(coords, tile):
                return coords

if __name__ == "__main__":

    game = Game()
    for i in range(1):
        game.reset()
        while len(game.state.deck) > 0:
            tile = game.get_new_tile()
            coords = fit_tile(game, tile)
            game.state.insert_tile(coords, tile)
        game.render()
        for coord in game.state.board:
            print(f"{coord} - {game.state.board[coord]}")
        game.gui.tk_root.mainloop()


