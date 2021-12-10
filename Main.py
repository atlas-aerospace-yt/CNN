from CNN import NeuralNetwork as nn
import numpy as np
from PIL import Image

if __name__ == "__main__":

    input = np.zeros((8,8))

    input_fat =      ([[1, 0, 0, 1, 1, 0, 0, 1],
                       [1, 0, 1, 1, 1, 1, 0, 1],
                       [0, 1, 0, 1, 1, 0, 1, 0],
                       [0, 1, 1, 1, 1, 1, 1, 0],
                       [0, 1, 0, 0, 0, 0, 1, 0],
                       [0, 0, 1, 1, 1, 1, 0, 0],
                       [1, 1, 0, 1, 1, 0, 1, 1],
                       [1, 0, 0, 0, 0, 0, 0, 1]])

    input_thin =     ([[0, 0, 1, 0, 0, 1, 0, 0],
                       [0, 0, 1, 1, 1, 1, 0, 0],
                       [0, 0, 1, 1, 1, 1, 0, 0],
                       [0, 1, 0, 1, 1, 0, 1, 0],
                       [1, 0, 1, 1, 1, 1, 0, 1],
                       [0, 0, 1, 1, 1, 1, 0, 0],
                       [0, 1, 1, 0, 0, 1, 1, 0],
                       [0, 1, 0, 0, 0, 0, 1, 0]])

    model = nn(input_fat, 10, 2)

    #image = (Image.fromarray(np.array(input_thin) * 255)).resize((1000,1000), Image.ANTIALIAS)
    #image.show()
    #prediction = model.forward(input_fat)

    #for x in range(0, 100):
    model.backward(([[0, 1]]), input_fat)

    #for x in range(0, 100):
        #model.backward(([[1, 0]]), input_thin)

    #prediction = model.forward(input_fat)

    #print(prediction)
