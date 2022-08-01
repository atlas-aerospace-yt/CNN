import matplotlib.pyplot as plt
from CNN import NeuralNetwork as nn
import numpy as np
from PIL import Image
import os

if __name__ == "__main__":

    # Initialises the CNN library
    input = np.zeros((21,21))
    model = nn(input, dir='TrainingData/')

    # Gets every image file in the TestingData directory
    for file in os.listdir('TestingData/'):
        if file.endswith('.png'):

            # Converts the image to a numeric Vector
            input = model.img('TestingData/' + file)

            # Predicts the shape in the image
            output = model.round(model.forward(input, img=True))

            # Outputs the filename and the predicted shape
            print(file, model.outputs[int(output)])
