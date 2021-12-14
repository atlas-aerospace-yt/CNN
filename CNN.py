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
        self.learnRate = 0.1
        self.cost = 0

        self.loadNetwork()

    # stops training the network each time and just loads previous
    def loadNetwork(self):

        try:

            with open('weights.npy','rb') as file:

                self.weights = nn.load(file)

            with open('bias.npy','rb')  as file:

                self.bias = nn.load(file)
        except:

            self.weights = nn.random.uniform(-1, 1, (self.width * self.height * self.numOfOutputs + self.numOfLayers, self.width * self.height))

            with open('weights.npy','wb') as file:

                nn.save(file, self.weights)

            self.bias = nn.random.uniform(-1, 1, (self.numOfLayers + 1, self.width * self.height))

            with open('bias.npy','wb') as file:

                nn.save(file, self.bias)

    # save the weight and bias matrices
    def save(self):

        with open('weights.npy','wb') as file:

            nn.save(file, self.weights)

        with open('bias.npy','wb') as file:

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

                list.append(value)

        num = 0

        for item in list:

            output[num][0] = float(item)

            num = num + 1

        return output

    # forward propagation... pattern recognition
    def forward(self,input):

        input = self.flatten(input)

        weights = nn.zeros((self.width * self.height, self.width * self.height))

        bias = nn.zeros((self.width * self.height , 1))

        if self.numOfLayers <= 0:

            l = -1

        for l in range(0, self.numOfLayers):

            for x in range(l * self.width * self.height, (l + 1) * self.width * self.height):

                for y in range(0, self.width * self.height):

                    weights[x - self.width * self.height * (l + 1)][y] = self.weights[x][y]
                    bias[y][0] = self.bias[l][y]

            output = self.sigmoid(nn.dot(weights , input) + bias)
            input = output

        weights = nn.zeros((self.numOfOutputs, self.width * self.height))

        bias = nn.zeros((self.numOfOutputs , 1))

        for x in range((l + 1) * self.width * self.height, self.numOfOutputs + (l + 1) * self.width * self.height):

            for y in range(0, self.width * self.height):

                weights[x - self.width * self.height * (l + 1)][y] = self.weights[x][y]

                if y < self.numOfOutputs:

                    bias[y][0] = self.bias[l + 1][y]

        return self.sigmoid(nn.dot(weights , input) + bias)

    # gradient weight function
    def gradient(self, actual, prediction, layerOutput, layerInput):

        #self.MSE = nn.square(nn.subtract(prediction , actual)).mean()

        z = self.sigmoidPrime(layerOutput)

        self.dCdb = z * 2 * (prediction - actual)

        return self.dCdb

    # backwards propagation
    def backward(self, actual, input):

        prediction = self.forward(input)

        input = self.flatten(input)

        weights = nn.zeros((self.width * self.height, self.width * self.height))
        bias = nn.zeros((self.width * self.height , 1))

        if self.numOfLayers <= 0:
            l = -1

        for l in range(0, self.numOfLayers):

            for x in range(l * self.width * self.height, (l + 1) * self.width * self.height):

                for y in range(0, self.width * self.height):

                    weights[x - self.width * self.height * (l + 1)][y] = self.weights[x][y]
                    bias[y][0] = self.bias[l][y]

            layerOutput = self.sigmoid(nn.dot(weights , input) + bias)

            gradient = self.gradient(actual, prediction, layerOutput, input)

            weights = weights - self.learnRate * gradient * input

            bias = bias - self.learnRate * gradient

            for x in range(l * self.width * self.height, (l + 1) * self.width * self.height):

                for y in range(0, self.width * self.height):

                    self.weights[x][y] = weights[x - self.width * self.height * (l + 1)][y]
                    self.bias[l][y] = bias[y][0]

            input = layerOutput

        weights = nn.zeros((self.numOfOutputs, self.width * self.height))
        bias = nn.zeros((self.numOfOutputs , 1))

        for x in range((l + 1) * self.width * self.height, self.numOfOutputs + (l + 1) * self.width * self.height):

            for y in range(0, self.width * self.height):

                weights[x - self.width * self.height * (l + 1)][y] = self.weights[x][y]

                if y < self.numOfOutputs:
                    bias[y][0] = self.bias[l + 1][y]

        layerOutput = self.sigmoid(nn.dot(weights , input) + bias)

        gradient = self.gradient(actual, prediction, layerOutput, input)

        weights = weights - self.learnRate * nn.dot(gradient , nn.transpose(input))
        bias = bias - self.learnRate * gradient

        for x in range((l + 1) * self.width * self.height, self.numOfOutputs + (l + 1) * self.width * self.height):

            for y in range(0, self.width * self.height):

                self.weights[x][y] = weights[x - self.width * self.height * (l + 1)][y]

                if y < self.numOfOutputs:
                    self.bias[l][y] = bias[y][0]

        self.save()

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
