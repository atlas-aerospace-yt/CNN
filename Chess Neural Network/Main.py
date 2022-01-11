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

class Learning():

    def __init__(self,width=None,height=None):

        if width != None and height != None:

            example = np.zeros((width,height))
            self.model = nn(example)

            ## TODO: find a way to model output dynamically
            
        ## TODO: Automatically organise

class Engine():

    def __init__(self):

        ## TODO: Convert chess into supported input
        pass


if __name__ == "__main__":

    ## TODO: Work on folder of positions to train
    train = Learning(width=8,height=8)

    ## TODO: Work on algorithm

    ## TODO: Save all previous games

    ## TODO: Check Mate patterns

    ## TODO: Chess openings

    ## TODO: Output the move wanted
