from engine.game_state import GameState
from engine.game_ui import Gui


class Game:
    def __init__(self, n_players=2):
        self.n_players = n_players
        self.state = GameState(self.n_players)
        self.gui = Gui()

    def reset(self):
        self.state = GameState(self.n_players)
        #self.gui = Gui()

    def render(self):
        self.gui.draw_game_state(self.state)

    def get_new_tile(self):
        return self.state.deck.pop()


