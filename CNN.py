import matplotlib.pyplot as plt
from PIL import Image
import numpy as nn
import random
import os

class NeuralNetwork():

    def __init__(self, matrix, numOfOutputs = None, dir = None, train=False):

        self.matrix = matrix

        if numOfOutputs != None:
            self.numOfOutputs = numOfOutputs
        elif dir != None:
            self.numOfOutputs = len(self.getOutputs(dir))
            self.outputs = self.getOutputs(dir)
        else:
            print("Error: Input NumOfOutputs or Directory expected, got neither!")
            exit()

        self.width = len(self.matrix)
        self.height = len(self.matrix[0])
        self.learnRate = 0.1
        self.cost = 0

        self.loadNetwork()

        if dir != None and train != False:

            self.autoBackward(dir)

    # stops training the network each time and just loads previous
    def loadNetwork(self):

        # Attempts to load the networks weights and biases
        try:
            with open('./ANN/weights.npy','rb') as file:
                self.weights = nn.load(file)

            with open('./ANN/bias.npy','rb')  as file:
                self.bias = nn.load(file)
        # Creates random weights and biases if there are none
        except:
            self.weights = nn.random.uniform(-1, 1, (self.width * self.height * self.numOfOutputs, self.width * self.height))
            with open('./ANN/weights.npy','wb') as file:
                nn.save(file, self.weights)

            self.bias = nn.random.uniform(-1, 1, (1, self.width * self.height))
            with open('./ANN/bias.npy','wb') as file:
                nn.save(file, self.bias)

    # Save the weight and bias matrices
    def save(self):
        with open('./ANN/weights.npy','wb') as file:
            nn.save(file, self.weights)

        with open('./ANN/bias.npy','wb') as file:
            nn.save(file, self.bias)

    # convert a matrix to an [n,n] to [n, 1]
    def flatten(self, matrix):

        width = len(matrix)
        height = len(matrix[0])

        list = []

        output = nn.zeros((len(matrix) * len(matrix[0]),1))

        for x in range(0, width):
            for y in range(0, height):
                value = matrix[x][y]
                list.append(value[0])

        num = 0
        for item in list:
            output[num][0] = float(item)
            num = num + 1

        return output

    # forward propagation... pattern recognition
    def forward(self, input, img=False):

        input = self.flatten(input)

        weights = nn.zeros((self.numOfOutputs, self.width * self.height))

        bias = nn.zeros((self.numOfOutputs , 1))

        for x in range(0, self.numOfOutputs):

            for y in range(0, self.width * self.height):

                weights[x][y] = self.weights[x][y]

                if y < self.numOfOutputs:

                    bias[y][0] = self.bias[0][y]

        if img != True:
            return self.sigmoid(nn.dot(weights , input) + bias)
        else:
            output = self.round(self.sigmoid(nn.dot(weights , input) + bias))
            ans = []
            for x in output:
                ans.append(float(x))
            pos = ans.index(1)

            return pos

    # gradient weight function
    def gradient(self, actual, prediction, layerOutput, layerInput):

        z = self.sigmoidPrime(layerOutput)

        self.dCdb = z * 2 * (prediction - actual)

        return self.dCdb

    # backwards propagation
    def update(self, actual, input):

        prediction = self.forward(input)

        input = self.flatten(input)

        weights = nn.zeros((self.numOfOutputs, self.width * self.height))
        bias = nn.zeros((self.numOfOutputs , 1))

        for x in range(0, self.numOfOutputs):

            for y in range(0, self.width * self.height):

                weights[x][y] = self.weights[x][y]

                if y < self.numOfOutputs:
                    bias[y][0] = self.bias[0][y]

        layerOutput = self.sigmoid(nn.dot(weights , input) + bias)

        gradient = self.gradient(actual, prediction, layerOutput, input)

        weights = weights - self.learnRate * nn.dot(gradient , nn.transpose(input))
        bias = bias - self.learnRate * gradient

        for x in range(0, self.numOfOutputs):

            for y in range(0, self.width * self.height):

                self.weights[x][y] = weights[x][y]

                if y < self.numOfOutputs:
                    self.bias[0][y] = bias[y][0]

        self.save()

    # automatic update function that trains the CNN
    def autoBackward(self, dir):

        training = []

        for file in os.listdir(dir):

            if file.endswith('.png'):

                training.append(dir + file)

        for loop in range(0, 500):
            for item in training:

                pos = self.outputs.index(item.replace(dir,'').split('_')[0])

                actual = nn.zeros((self.numOfOutputs, 1))
                actual[pos][0] = 1

                image = self.img(item)
                self.update(actual, image)

    # gets the text output based on which value is 1
    def  getOutputs(self, dir):

        numOfOutputs = []

        for file in os.listdir(dir):
            if file.endswith('.png'):
                if file.split("_")[0] not in numOfOutputs:

                    numOfOutputs.append(file.split("_")[0])

        return numOfOutputs

    # import images to train
    def img(self, input):

        nn.set_printoptions(threshold=nn.inf)

        image = Image.open(input)
        data = nn.asarray(image) / 255

        return data

    # displays the image
    def display(self, input):

        image = Image.open(input)
        image.show()

    # mathematical activation functions
    def sigmoid(self, input):

        return 1 / (1 + nn.exp(-input))

    def sigmoidPrime(self, input):

        return self.sigmoid(input) * (1.0 - self.sigmoid(input))

    def swish(self, input):

        return input / (1 + nn.exp(-input))

    def leakyRelu(self, input):

        if input > 0:
            return input
        else:
            return 0.1 * input

    def relu(self, input):

        if input > 0:
            return input
        else:
            return 0

    def linear(self, input):

        return input

    def tanh(self, input):

        return (nn.exp(input) - nn.exp(-input)) / (nn.exp(input) + nn.exp(-input))

    def step(self, input):

        if input >= 0:
            return 1
        if input < 0:
            return 0

    # round the output to nearest 0.5
    def round(self, input):

        return nn.around(input * 2.0) / 2.0
