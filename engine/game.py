from engine.game_state import GameState
from engine.game_ui import Gui
from engine.tile import Tile

class Game:
    def __init__(self, n_players=2, create_ui=True):
        self.n_players = n_players
        self.state = None
        self.gui = None
        if create_ui:
            self.gui = Gui()

    def start(self):
        self.state = GameState(self.n_players)

    def render(self):
        if self.gui:
            self.gui.draw_game_state(self.state)

    def get_new_tile(self):
        return self.state.deck.pop()

    def interactive(self):
        self.gui.interactive(self.state)
