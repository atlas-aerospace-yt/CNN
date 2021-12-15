import matplotlib.pyplot as plt
from CNN import NeuralNetwork as nn
import numpy as np
from PIL import Image
import os

if __name__ == "__main__":

    input = np.zeros((21,21))
    model = nn(input, dir='TrainingData/', train=True)

    for file in os.listdir('TestingData/'):

        if file.endswith('.png'):

            input = model.img('TestingData/' + file)

            output = model.round(model.forward(input, img=True))

            print(model.outputs[int(output)])
