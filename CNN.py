import numpy as nn
import random

class NeuralNetwork():


    def __init__(self, matrix, numOfNodes, numOfLayers):

        self.matrix = matrix
        self.numOfNodes = numOfNodes
        self.numOfLayers = numOfLayers

        self.loadNetwork()

    # stops training the network each time and just loads previous
    def loadNetwork(self):

        try:

            with open('weights.npy','rb') as file:

                self.Weights = nn.load(file)

        except:

            self.Weights = nn.zeros((len(self.matrix) * len(self.matrix[0]), self.numOfNodes * self.numOfLayers))#, LayerInput))

    # save the weight and bias matrices
    def save(self):

        with open('weights.npy','wb') as file:

            nn.save(file, self.Weights)

    # convert a matrix to an [n,n] to [n, 1]
    def flatten(self, matrix):

        width = len(matrix)
        height = len(matrix[0])

        output = []

        for x in range(0,height):

            for y in range(0,width):

                num = matrix[x][y]

                output.append(num)

        return output

    # main neural network model
    def hiddenLayers(self, matrix):

        return nn.dot(matrix, self.Weights)


    # forward propagation... pattern recognition
    def forward(self,input):

        x = self.flatten(input)
        x = self.hiddenLayers(x)

        self.save()

        print(x)

    # mathematical activation functions
    def sigmoid(self, input):

        return 1 / (1 + nn.exp(-input))

    def leakyRelu(self, input):

        if x >= 0:
            return input
        else:
            return 0.1 * input

    def relu(self, input):

        if x >= 0:
            return input
        else:
            return 0

    def step(self, input):

        if input >= 0.5:
            return 1
        if input < 0.5:
            return 0

    def backward(self, input, output):

        pass
