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

    model = nn(input_thin, 0, 2)

    #image = Image.fromarray(np.array(input_thin).astype('uint8')*255)
    #image.show()

    #prediction = model.forward(input_fat)

    #for x in range(0, 100):
    #model.backward(([[0, 1]]), input_fat)

    costFat = []
    costThin = []
    costWhite = []
    costBlack = []

    for x in range(0, 1000):

        model.backward(([[1],[0]]), input_fat)
        costFat.append(float(model.dCdb[0]))
        model.backward(([[0],[1]]), input_thin)
        costThin.append(float(model.dCdb[0]))
        model.backward(([[0.5],[0.5]]), input_white)
        costWhite.append(float(model.dCdb[0]))
        model.backward(([[0.5],[0.5]]), input_black)
        costBlack.append(float(model.dCdb[0]))

    list = []

    for x in range(0,len(costFat)):

        list.append(x)

    plt.plot(list, costFat)
    plt.plot(list, costThin)
    plt.plot(list, costWhite)
    plt.plot(list, costBlack)
    plt.show()

    #print(model.forward(input_fat))

    test =   ([[1, 1, 0, 1, 1, 0, 0, 1],
               [1, 0, 1, 1, 1, 1, 0, 1],
               [0, 1, 0, 1, 1, 0, 1, 0],
               [0, 1, 1, 1, 1, 1, 1, 0],
               [0, 1, 0, 0, 0, 1, 1, 0],
               [0, 0, 1, 1, 1, 1, 0, 0],
               [1, 1, 0, 1, 1, 0, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 1]])


    print(model.round(model.forward(test)))
    #print(model.round(model.forward(input_fat)))
    #print(model.round(model.forward(input_white)))
    #print(model.round(model.forward(input_black)))
