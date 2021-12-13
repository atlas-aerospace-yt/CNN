import matplotlib.pyplot as plt
from CNN import NeuralNetwork as nn
import numpy as np
from PIL import Image

if __name__ == "__main__":

    input = np.zeros((1,2))

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

    model = nn(input_thin, 0 , 1)

    image = Image.fromarray(np.array(input_thin).astype('uint8')*255)
    image.show()

    #prediction = model.forward(input_fat)

    #for x in range(0, 100):
    #model.backward(([[0, 1]]), input_fat)

    #cost = []

    #for x in range(0, 10000):

    #    model.backward(([[1]]), input_fat)
    #    model.backward(([[0]]), input_thin)

    #    cost.append(float(model.dCdb))

    #list = []

    #for x in range(0,len(cost)):

    #    list.append(x)

    #plt.plot(list, cost)
    #plt.show()

    #print(model.forward(input_fat))
    print(model.forward(input_thin))
