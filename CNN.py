import numpy as nn
import random
import os

class NeuralNetwork():


    def __init__(self, matrix, numOfLayers, numOfOutputs):

        self.matrix = matrix
        self.numOfLayers = numOfLayers
        self.numOfOutputs = numOfOutputs
        self.width = len(self.matrix)
        self.height = len(self.matrix[0])
        self.learnRate = 0.1

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

        os.remove('weights.npy')
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

        return prediction

    # gradient weight function
    def gradientW(self, actual, prediction, layerInput, input, weights):

        #cw = 2 / n * self.cost(y, yHat) * self.sigmoid(z) * (1 - self.sigmoid(z)) * x

        n = self.width * self.height

        cost = nn.transpose(actual - prediction)

        layerOutput = self.sigmoid(layerInput)

        layerInput = (1 - self.sigmoid(layerInput)) * input

        gradient = 2 / n * cost * layerOutput * layerInput

        list = []

        value = 0

        for y in range(0, self.width * self.height):

            for x in range(0, self.numOfOutputs):


                if x % self.numOfOutputs == 0:

                    list.append(value + gradient[x][y])

                    value = 0

                else:

                    value += gradient[x][y]

        num = 0
        output = nn.zeros((self.width * self.height, 1))

        for value in list:

            output[num][0] = value

            num = num + 1

        weight =  weights - (self.learnRate * output)

        return weight

    # backwards propagation
    def backward(self, actual, input):

        for backwards in range(1):#(0, self.numOfLayers):

            n = self.width * self.height

            flatInput = self.flatten(input)

            layerInput = self.flatten(input)

            num = 0

            layer = nn.zeros((self.width * self.height, 1))

            output = nn.zeros((1, self.width * self.height))

            for l in range(0, self.numOfLayers):

                for x in range(l * self.width * self.height, self.width * self.height):

                    for y in range(0, self.width * self.height):

                        layer[y][0] = self.weights[x][y]

                    output[0][x] = self.sigmoid(nn.dot(layerInput , layer))

                layerInput = output

            o = l + 1

            prediction = nn.zeros((1, self.numOfOutputs))
            output = nn.zeros((self.width * self.height, 1))

            x = o * self.width * self.height


            for y in range(0, self.height * self.width):

                output[y][0] = self.weights[x][y]

            prediction = self.sigmoid(nn.dot(layerInput, output))

            if backwards == 0:

                gradient = self.gradientW(actual, prediction, layerInput, flatInput, output)

                x = o * self.width * self.height

                list = []

                for y in range(0, self.width*self.height):

                    self.weights[x][y] = gradient[y][0]

                    list.append(self.weights[x][y])
        self.save()

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
