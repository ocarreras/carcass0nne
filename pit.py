import random

import agents.alpha0.Arena
from agents.alpha0.MCTS import MCTS
from agents.alpha0.nn.NNet import NNetWrapper as nn
from agents.alpha0.Arena import Arena
from engine.game import Game
from engine.game_state import GameState
from agents.alpha0.utils import *
import numpy as np

args = dotdict({
    'numIters': 1000,
    'numEps': 2,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './temp3/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
})

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

def random_play(state:GameState):
    tile = state.next_tile
    tile_placements = state.get_available_tile_placements(tile)
    legalTileMoves = []
    for tile_placement in tile_placements:
        coords, rotation = tile_placement
        meeple_placements = state.get_available_meeple_placements(tile, coords, rotation)
        for meeple_placement in meeple_placements:
            legalTileMoves.append((coords, rotation, meeple_placement))
    if len(legalTileMoves) == 0:
        print("NO MOVE!!!")
        return -1
    move_ids = []
    for coords, rotation, meeple_placement in legalTileMoves:
        #print(f"Valid move: {coords}, {rotation}, {meeple_placement}")
        move_id = state.ml_get_action_id(tile, coords, rotation, meeple_placement)
        move_ids.append(move_id)
    random.shuffle(move_ids)
    print(f"Random: {move_ids[0]}")
    return move_ids[0]

mini_othello = False  # Play in 6x6 instead of the normal 8x8.
human_vs_cpu = True

g = Game()
n1 = nn(g)

n1.load_checkpoint(folder=args.checkpoint, filename='temp.pth.tar')
n1mcts = MCTS(g, n1, args)

#n2 = nn(g)
#n2mcts = MCTS(g, n2, args)

print('PITTING AGAINST RANDOM PLAY')
arena = Arena(lambda x: np.argmax(n1mcts.getActionProb(x, temp=0)),
              lambda x: random_play(x), g)

print(arena.playGames(10, verbose=False))
