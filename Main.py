from CNN import NeuralNetwork as nn
import numpy as np

if __name__ == "__main__":

    input = np.random.uniform(-1, 1, (8, 8))
    model = nn(input, 3, 6)

    model.forward(input)
