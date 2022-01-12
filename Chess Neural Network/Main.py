# Main chess engine code
# Not a lot has been done so far
# This will eventually accept a chess position
# and output the best move to make.
# The code will be based off the deeplearn ches engine
# known as Alpha-Zero.

# P = 0.1
# B = 0.2
# N = 0.3
# R = 0.5
# Q = 0.8
# K = 1.0

import matplotlib.pyplot as plt
from CNN import NeuralNetwork as nn
import numpy as np
from Chess import Board
from Chess import Pieces
from Chess import Notation
from PIL import Image
import os

class Engine():

    def __init__(self):

        self.model = nn(chess=True)

    def move(self):

        input = ([[5, 3, 2, 8, 10, 2, 3, 5],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [5, 3, 2, 8, 10, 2, 3, 5]])

        self.model.backwardChess(input, [[4],[2],[4],[4]])

if __name__ == "__main__":

    train = Engine()
    train.move()

    ## TODO: Work on algorithm

    ## TODO: Save all previous games

    ## TODO: Check Mate patterns

    ## TODO: Chess openings

    ## TODO: Output the move wanted
