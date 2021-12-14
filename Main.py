import matplotlib.pyplot as plt
from CNN import NeuralNetwork as nn
import numpy as np
from PIL import Image

if __name__ == "__main__":

    input_white = np.zeros((8,8))
    input_black = np.ones((8,8))

    input_fat =      ([[1, 0, 0, 1, 1, 0, 0, 1],
                       [1, 0, 1, 1, 1, 1, 0, 1],
                       [0, 1, 0, 1, 1, 0, 1, 0],
                       [0, 1, 1, 1, 1, 1, 1, 0],
                       [0, 1, 0, 0, 0, 0, 1, 0],
                       [0, 0, 1, 1, 1, 1, 0, 0],
                       [1, 1, 0, 1, 1, 0, 1, 1],
                       [1, 0, 0, 0, 0, 0, 0, 1]])

    input_thin =     ([[0, 0, 1, 1, 0, 1, 0, 0],
                       [0, 0, 1, 1, 1, 1, 0, 0],
                       [0, 0, 1, 1, 1, 1, 0, 0],
                       [0, 1, 0, 1, 1, 0, 1, 0],
                       [1, 0, 1, 1, 1, 1, 0, 1],
                       [0, 0, 1, 1, 1, 1, 0, 0],
                       [0, 1, 1, 0, 0, 1, 1, 0],
                       [0, 1, 0, 0, 0, 0, 1, 0]])

    #input_thin = input_thin.astype('float32')

    model = nn(input_thin, 0, 1)

    #prediction = model.forward(input_fat)

    #for x in range(0, 100):
    model.backward(input_fat, input_thin, input_white, input_black)

    #print(model.forward(input_fat))

    test =   ([[1, 1, 0, 1, 1, 0, 0, 1],
               [1, 0, 1, 1, 1, 1, 0, 1],
               [0, 1, 0, 1, 1, 0, 1, 0],
               [0, 1, 1, 1, 1, 1, 1, 0],
               [0, 1, 0, 0, 0, 1, 1, 0],
               [0, 0, 1, 1, 1, 1, 0, 0],
               [1, 1, 0, 1, 1, 0, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 1]])


    image = Image.fromarray(np.array(test).astype('uint8')*255)
    image.show()

    print(model.round(model.forward(test)))
    print(model.round(model.forward(input_thin)))
    print(model.round(model.forward(input_white)))
    print(model.round(model.forward(input_black)))
