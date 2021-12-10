#
# This is code avaliable for anyone to edit and use.
#
# Code using this library must credit the original GitHub.
#
# This was written on the 01/12/2021.
#
# Author: Atlas Aerospace / Alexander Armitage.
#
# The code is designed to input a matrix and model a neural Network
# Then, you need to enter training data for the model to train itself.
#
# Then, this code will be able to recognise patters in any data sets.
#
# e.g. images, sequences, chess and more.
#
# The code is designed to be used as a library as will be show in the
# example when the library has finished development of version one.
#
# Version: dev:0.0.1


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
        self.learnRate = 1

        self.loadNetwork()

    # stops training the network each time and just loads previous
    def loadNetwork(self):

        try:

            with open('weights.npy','rb') as file:

                self.weights = nn.load(file)

        except:

            self.weights = nn.zeros((self.width * self.height * (self.numOfOutputs + self.numOfLayers), self.width * self.height))

    # save the weight and bias matrices
    def save(self):

        try:
            os.remove('weights.npy')
        except:
            pass

        with open('weights.npy','wb') as file:

            nn.save(file, self.weights)

    # convert a matrix to an [n,n] to [n, 1]
    def flatten(self, matrix):

        width = len(matrix)
        height = len(matrix[0])

        #Noice

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

            for x in range(l * self.width * self.height, (l + 1) * self.width * self.height):

                for y in range(0, self.width * self.height):

                    layer[y][0] = self.weights[x][y]

                output[0][x - self.width * self.height * l - 1] = self.sigmoid(nn.dot(input , layer))

            input = output

        o = l + 1

        prediction = nn.zeros((1, self.numOfOutputs))
        output = nn.zeros((self.width * self.height, 1))

        for x in range(o * self.width * self.height, self.numOfOutputs + o * self.width * self.height):

            for y in range(0, self.width * self.height):

                output[y][0] = self.weights[x][y]

            prediction[0][x - self.width * self.height * o] = self.sigmoid(nn.dot(input, output))

        self.save()

        return prediction

    # gradient weight function
    def gradientW(self, actual, prediction, layerOutput, input):

        #cw = 2 / n * self.cost(y, yHat) * self.sigmoid(z) * (1 - self.sigmoid(z)) * x

        n = self.width * self.height

        cost = nn.transpose(actual - prediction)

        layerSig = self.sigmoid(layerOutput)

        layerMinus = (1 - self.sigmoid(layerOutput))

        gradient = 2 / n * cost * layerSig * layerMinus * input

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

        return output * 1

    # backwards propagation
    def backward(self, actual, input):

        prediction = self.forward(input)

        for backwards in range(0, self.numOfLayers):

            n = self.width * self.height

            flatInput = self.flatten(input)

            layerInput = self.flatten(input)

            num = 0

            layer = nn.zeros((self.width * self.height, 1))

            output = nn.zeros((1, self.width * self.height))

            for l in range(0, self.numOfLayers):

                for x in range(l * self.width * self.height, (l + 1) * self.width * self.height):

                    for y in range(0, self.width * self.height):

                        layer[y][0] = self.weights[x][y]

                    output[0][x - self.width * self.height * l - 1] = self.sigmoid(nn.dot(layerInput , layer))

                layerInput = output

                if backwards == 0 + self.numOfLayers - num:

                    gradient = self.gradientW(actual, prediction, layerInput, flatInput)

                    weights = output - (self.learnRate * gradient)

                num = num + 1

            o = l + 1

            output = nn.zeros((self.width * self.height, 1))

            for x in range(o * self.width * self.height, self.numOfOutputs + o * self.width * self.height):

                for y in range(0, self.width * self.height):

                    output[y][0] = self.weights[x][y]

                prediction[0][x - self.width * self.height * o] = self.sigmoid(nn.dot(layerInput, output))

            if backwards == 0:

                gradient = self.gradientW(actual, prediction, prediction, layerInput)

                weights = output - (self.learnRate * gradient)

                #print(weights)

                #list = []

                #o = l + 1

                #for x in range(o, o + self.numOfOutputs):
                #    for y in range(0, self.numOfOutputs):

                #        self.weights[x][y] = weights[y][0]

                #        list.append(self.weights[x][y])

            #print(list)
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
