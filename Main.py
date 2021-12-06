from CNN import NeuralNetwork as nn
import numpy as np

if __name__ == "__main__":

    input = np.zeros((8,8))

    input_fat = ([[1, 0, 0, 1, 1, 0, 0, 1],
                       [1, 0, 1, 1, 1, 1, 0, 1],
                       [0, 1, 0, 1, 1, 0, 1, 0],
                       [0, 1, 1, 1, 1, 1, 1, 0],
                       [0, 1, 0, 0, 0, 0, 1, 0],
                       [0, 0, 1, 1, 1, 1, 0, 0],
                       [1, 1, 0, 1, 1, 0, 1, 1],
                       [1, 0, 0, 0, 0, 0, 0, 1]])

    input_thin = np.matrix([[0, 0, 1, 0, 0, 1, 0, 0],
                       [0, 0, 1, 1, 1, 1, 0, 0],
                       [0, 0, 1, 1, 1, 1, 0, 0],
                       [0, 1, 0, 1, 1, 0, 1, 0],
                       [1, 0, 1, 1, 1, 1, 0, 1],
                       [0, 0, 1, 1, 1, 1, 0, 0],
                       [0, 1, 1, 0, 0, 1, 1, 0],
                       [0, 1, 0, 0, 0, 0, 1, 0]])

    model = nn(input, 3, 2)

    model.forward(input_fat)

    for x in range(0, 100):
        model.backward(input_fat, 2)

    for x in range(0, 100):
        model.backward(input_thin, 1)
