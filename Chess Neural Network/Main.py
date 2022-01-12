# Main chess engine code
# Not a lot has been done so far
# This will eventually accept a chess position
# and output the best move to make.
# The code will be based off the deeplearn ches engine
# known as Alpha-Zero.

import matplotlib.pyplot as plt
from CNN import NeuralNetwork as nn
import numpy as np
import Chess
from PIL import Image
import os

class Engine():

    def __init__(self):

        self.model = nn(chess=True)

    def move(self):

        self.model.forwardChess(board)

if __name__ == "__main__":

    train = Engine()

    ## TODO: Work on algorithm

    ## TODO: Save all previous games

    ## TODO: Check Mate patterns

    ## TODO: Chess openings

    ## TODO: Output the move wanted
