from engine.game_state import GameState
from engine.game_ui import Gui
from engine.tile import Tile
from engine.board import Board, ML_BOARD_SIZE
import hashlib

import numpy as np

##
# TODO: Temporal mess


class   Game:
    def __init__(self, n_players=2, create_ui=False, debug=0):
        self.n_players = n_players
        self.state = None
        self.gui = None
        self.debug = debug
        if create_ui:
            self.gui = Gui(self)

    def start(self):
        base_tile_counts = {
            "A": 2,
            "B": 4,
            "C": 1,
            "D": 4,
            "E": 5,
            "F": 2,
            "G": 1,
            "H": 3,
            "I": 2,
            "J": 3,
            "K": 3,
            "L": 3,
            "M": 2,
            "N": 3,
            "O": 2,
            "P": 3,
            "Q": 1,
            "R": 3,
            "S": 2,
            "T": 1,
            "U": 8,
            "V": 9,
            "W": 4,
            "X": 1
        }

        reduced_tile_counts = {
            "A": 2,
            "B": 2,
            "C": 0,
            "D": 2,
            "E": 2,
            "F": 2,
            "G": 2,
            "H": 2,
            "I": 2,
            "J": 2,
            "K": 0,
            "L": 0,
            "M": 0,
            "N": 0,
            "O": 0,
            "P": 0,
            "Q": 0,
            "R": 0,
            "S": 0,
            "T": 0,
            "U": 0,
            "V": 0,
            "W": 0,
            "X": 0
        }
        """
        """
        self.state = GameState(self.n_players, reduced_tile_counts, debug=self.debug)
        return self.state

    def render(self):
        if self.gui:
            self.gui.draw_game_state(self.state)

    def interactive(self):
        self.gui.interactive(self.state)

    ##
    # Functions for the alpha0-general first iteration
    #
    # TODO: Refactor later.
    #

    ##
    # Finished
    def getCanonicalForm(self, game_state: GameState, n_player):
        #print("getCanonicalForm")
        new_state = game_state.copy()
        new_state.canonical_player = n_player
        return new_state

    def getBoardSize(self):
        return ML_BOARD_SIZE, ML_BOARD_SIZE

    ##
    # TODO: Refactor
    def getAuxInputSize(self):
        return 5

    def getInitBoard(self):
        return self.start()

    def getGameEnded(self, state: GameState, curPlayer):
        # print("getGameEnded")
        if len(state.deck) != 0 or state.next_tile is not None:
            return 0
        state.calc_final_score()
        if state.scores[0] == state.scores[1]:
            return -1e-6
        #if state.canonical_player * (state.scores[0] > state.scores[1]):
        # TODO: How should canonicalBoard affect here
        if curPlayer*(state.scores[0] > state.scores[1]):
            return 1 * state.canonical_player
        else:
            return -1 * state.canonical_player

    def stringRepresentation(self, state: GameState):
        my_str =  hashlib.sha256(state.board.ml_board_s0.tostring()).hexdigest()
        next_tile: Tile = state.next_tile
        # Current tile needs to be encoded on state, otherwise we mess up the tree
        # as the valid actions are tied to tile
        return (next_tile.tile_type if next_tile else "_") + my_str

    def getActionSize(self):
        return Board.getActionSize()

    def getSymmetries(self, canonicalBoard: GameState, pi):
        sym0 = np.concatenate((canonicalBoard.board.ml_board_s0[0:4], canonicalBoard.board.ml_board_s0[4:] *
                              canonicalBoard.canonical_player))
        sym1 = np.concatenate((canonicalBoard.board.ml_board_s1[0:4], canonicalBoard.board.ml_board_s1[4:] *
                               canonicalBoard.canonical_player))
        sym2 = np.concatenate((canonicalBoard.board.ml_board_s2[0:4], canonicalBoard.board.ml_board_s2[4:] *
                               canonicalBoard.canonical_player))
        sym3 = np.concatenate((canonicalBoard.board.ml_board_s3[0:4], canonicalBoard.board.ml_board_s3[4:] *
                               canonicalBoard.canonical_player))
        return [(sym0, canonicalBoard.ml_get_aux(), pi), (sym1, canonicalBoard.ml_get_aux(), pi),
                (sym2, canonicalBoard.ml_get_aux(), pi), (sym3, canonicalBoard.ml_get_aux(), pi)]

    ##
    # TODO:
    #       player used for [?]
    def getValidMoves(self, state: GameState, player, verbose=False):
        #print("getValidMoves")
        tile = state.next_tile
        tile_placements = state.get_available_tile_placements(tile)
        legalTileMoves = []
        for tile_placement in tile_placements:
            coords, rotation = tile_placement
            meeple_placements = state.get_available_meeple_placements(tile, coords, rotation)
            for meeple_placement in meeple_placements:
                legalTileMoves.append((coords, rotation, meeple_placement))

        valids = [0] * self.getActionSize()
        if len(legalTileMoves) == 0 or state.next_tile == None:
            valids[-1] = 1
            return np.array(valids)

        for coords, rotation, meeple_placement in legalTileMoves:
            move_id = state.ml_get_action_id(tile, coords, rotation, meeple_placement)
            if verbose:
                print(f"Valid move: {coords}, {rotation}, {meeple_placement}")
                print(f"        ID: {move_id}")
            valids[move_id] = 1
        return np.array(valids)

    ####################################################################################################################
    ####################################################################################################################
    # On progress
    def getNextState(self, state: GameState, cur_player: int, action: int):
        state_cur_player = (-1) ** state.current_player

        ## TODO: assert cur_player == state_cur_player * state.canonical_player
        ## print(f"getNextState {cur_player} -- {state_cur_player} || {state.canonical_player}")

        next_state: GameState = state.copy()

        if action == self.getActionSize() - 1:
            print("Invalid action thingie")
            return (next_state, -cur_player)

        next_state.ml_action(action)

        ##
        # Get new tile ?
        if len(next_state.deck) != 0:
            # print("Getting new tile ...")
            next_state.get_new_tile()

        return next_state, -cur_player


