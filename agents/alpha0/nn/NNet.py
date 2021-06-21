import argparse
import os
import shutil
import time
import random
import numpy as np
import math
import sys
sys.path.append('../..')
from agents.alpha0.utils import *
from agents.alpha0.NeuralNet import NeuralNet

import argparse

from .CarcassoneNNet import CarcassoneNNet as onnet

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': False,
    'num_channels': 512,
})


class NNetWrapper(NeuralNet):
    def __init__(self, game):
        self.nnet = onnet(game, args)
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        input_boards, input_aux, target_pis, target_vs = list(zip(*examples))
        input_boards = np.asarray(input_boards)
        input_aux = np.asarray(input_aux)
        target_pis = np.asarray(target_pis)
        target_vs = np.asarray(target_vs)
        self.nnet.model.fit(x = [input_boards, input_aux], y = [target_pis, target_vs], batch_size = args.batch_size, epochs = args.epochs)

    def predict(self, board, input_aux):
        """
        board: np array with board
        """
        # timing
        start = time.time()

        ##
        # TODO: maybe use game state logic here
        #
        # preparing input
        board = board[np.newaxis, :, :]

        # TODO: Prepare input_aux =>
        input_aux = np.reshape(input_aux,(1, 5))
        pi, v = self.nnet.model.predict([board, input_aux])

        #print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return pi[0], v[0]

    # TODO: Hardcoded model names with .h5 -> change better
    def save_checkpoint(self, folder='checkpoint', filename='model_weights.h5'):
        filepath = os.path.join(folder, "model_weights.h5")
        print(f"PS: {filepath}")
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save_weights(filepath)

    def load_checkpoint(self, folder='checkpoint', filename="model_weights.h5"):
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, "model_weights.h5")
        print(f"PL: {filepath}")
        if not os.path.exists(filepath):
            raise("No model in path {}".format(filepath))
        self.nnet.model.load_weights(filepath)
