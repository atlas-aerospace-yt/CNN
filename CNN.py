import numpy as nn
import random

class NeuralNetwork():


    def __init__(self, matrix, numOfLayers, numOfOutputs):

        self.matrix = matrix
        self.numOfLayers = numOfLayers
        self.numOfOutputs = numOfOutputs
        self.width = len(self.matrix)
        self.height = len(self.matrix[0])

        self.loadNetwork()

    # stops training the network each time and just loads previous
    def loadNetwork(self):

        try:

            with open('weights.npy','rb') as file:

                self.weights = nn.load(file)

        except:

            self.weights = nn.random.uniform(0, 1, (self.width * self.height * (1 + self.numOfLayers), self.width * self.height))

    # save the weight and bias matrices
    def save(self):

        with open('weights.npy','wb') as file:

            nn.save(file, self.weights)

    # convert a matrix to an [n,n] to [n, 1]
    def flatten(self, matrix):

        width = len(matrix)
        height = len(matrix[0])

        list = []

        output = nn.zeros((1, len(matrix) * len(matrix[0])))

        for x in range(0, width):

            for y in range(0, height):

                value = matrix[x][y]

                list.append(value)

        num = 0

        for item in list:

            output[0][num] = float(item)

            num = num + 1

        return output

    # forward propagation... pattern recognition
    def forward(self,input):

        input = self.flatten(input)

        num = 0

        layer = nn.zeros((self.width * self.height, 1))

        output = nn.zeros((1, self.width * self.height))

        for l in range(0, self.numOfLayers):

            for x in range(l * self.width * self.height, self.width * self.height):

                for y in range(0, self.width * self.height):

                    layer[y][0] = self.weights[x][y]

                output[0][x] = self.sigmoid(nn.dot(input , layer))

            input = output

        o = l + 1

        prediction = nn.zeros((1, self.numOfOutputs))
        output = nn.zeros((self.width * self.height, 1))

        for x in range(o * self.width * self.height):

            for y in range(0, self.numOfOutputs):

                output[y][0] = self.weights[x][y]

            if x < self.numOfOutputs:
                prediction[0][x] = self.sigmoid(nn.dot(input, output))

            else:
                pass

        print(prediction)

        self.save()



    # gradient weight function
    def gradientW(self, y, x):

        cw = 2 / n * self.cost(y, yHat) * self.sigmoid(z) * (1 - self.sigmoid(z)) * x

    # backwards propagation
    def backward(self, y, x):

        n = self.width * self.height

        input = self.flatten(input)

        num = 0

        layer = nn.zeros((self.width * self.height, 1))

        output = nn.zeros((1, self.width * self.height))

        for l in range(0, self.numOfLayers):

            for x in range(l * self.width * self.height, self.width * self.height):

                for y in range(0, self.width * self.height):

                    layer[y][0] = self.weights[x][y]

                output[0][x] = self.sigmoid(nn.dot(input , layer))

            input = output

        o = l + 1

        prediction = nn.zeros((1, self.numOfOutputs))
        output = nn.zeros((self.width * self.height, 1))

        for x in range(o * self.width * self.height):

            for y in range(0, self.numOfOutputs):

                output[y][0] = self.weights[x][y]

            if x < self.numOfOutputs:
                prediction[0][x] = self.sigmoid(nn.dot(input, output))

            else:
                pass

        gradientW = self.gradientW(n, y, yHat, z, x)

    # mathematical activation functions
    def sigmoid(self, input):

        return 1 / (1 + nn.exp(-input))

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
