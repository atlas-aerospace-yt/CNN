import matplotlib.pyplot as plt
from CNN import NeuralNetwork as nn
import numpy as np
from PIL import Image

if __name__ == "__main__":

    input = np.zeros((1,2))

    #input_fat =      ([[1, 0, 0, 1, 1, 0, 0, 1],
    #                   [1, 0, 1, 1, 1, 1, 0, 1],
    #                   [0, 1, 0, 1, 1, 0, 1, 0],
    #                   [0, 1, 1, 1, 1, 1, 1, 0],
    #                   [0, 1, 0, 0, 0, 0, 1, 0],
    #                   [0, 0, 1, 1, 1, 1, 0, 0],
    #                   [1, 1, 0, 1, 1, 0, 1, 1],
    #                   [1, 0, 0, 0, 0, 0, 0, 1]])

    #input_fat = input_fat.astype('float32')

    #input_thin =     ([[0, 0, 1, 0, 0, 1, 0, 0],
    #                   [0, 0, 1, 1, 1, 1, 0, 0],
    #                   [0, 0, 1, 1, 1, 1, 0, 0],
    #                   [0, 1, 0, 1, 1, 0, 1, 0],
    #                   [1, 0, 1, 1, 1, 1, 0, 1],
    #                   [0, 0, 1, 1, 1, 1, 0, 0],
    #                   [0, 1, 1, 0, 0, 1, 1, 0],
    #                   [0, 1, 0, 0, 0, 0, 1, 0]])

    #input_thin = input_thin.astype('float32')

    model = nn(input, 1, 1)

    #image = (Image.fromarray(np.array(input_thin) * 255)).resize((1000,1000), Image.ANTIALIAS)
    #image.show()
    #prediction = model.forward(input_fat)

    #for x in range(0, 100):
    #model.backward(([[0, 1]]), input_fat)

    cost = []

    for x in range(0, 1000):

        model.backward(([[0]]), ([[0],[1]]))
        model.backward(([[0]]), ([[0],[0]]))
        model.backward(([[1]]), ([[1],[0]]))
        model.backward(([[1]]), ([[1],[1]]))

        cost.append(model.MSE)

    list = []

    for x in range(0,len(cost)):

        list.append(x)

    plt.plot(list, cost)
    plt.show()

    print(model.bias)
    print(model.weights)
    print(model.forward(([[1],[0]])))
    print(model.forward(([[0],[1]])))
