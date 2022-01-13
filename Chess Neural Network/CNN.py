#
# This is code avaliable for anyone to edit and use.
#
# Code using this library must credit the original GitHub.
#
# This was written on the 15/12/2021.
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
# Version: dev.0.0.2
#

import matplotlib.pyplot as plt
from warnings import warn
from PIL import Image
import numpy as nn
import random
import os

class NeuralNetwork():

    def __init__(self, matrix=None, numOfOutputs=None, dir=None, train=False, chess=False):

        if matrix != None:
            self.matrix = matrix

        elif chess == True:
            self.matrix = nn.zeros((8,8))

        else:
            warn("Warning: No matrix input!")
            exit()

        if numOfOutputs != None:
            self.numOfOutputs = numOfOutputs

        elif dir != None:
            self.numOfOutputs = len(self.getOutputs(dir))
            self.outputs = self.getOutputs(dir)

        elif numOfOutputs != None and chess == False:
            warn("Error: Input NumOfOutputs or Directory expected, got neither!")
            exit()

        self.width = len(self.matrix)
        self.height = len(self.matrix[0])
        self.learnRate = 0.1
        self.cost = 0

        if dir != None and train != False:

            self.autoBackward(dir)

        if chess == True:

            self.loadNetwork(chess=True)

        else:

            self.loadNetwork()

    # calculates output size for a network
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

    # stops training the network each time and just loads previous
    def loadNetwork(self, chess=False):

        try:

            with open('weights.npy','rb') as file:

                self.weights = nn.load(file)

            with open('bias.npy','rb')  as file:

                self.bias = nn.load(file)
        except:

            if chess == False:

                self.weights = nn.random.uniform(-1, 1, (self.width * self.height * self.numOfOutputs, self.width * self.height))
                self.bias = nn.random.uniform(-1, 1, (1, self.width * self.height))

            else:

                self.weights = nn.random.uniform(-1, 1, (64,128))
                self.bias = nn.random.uniform(-1, 1, (64,65))

            with open('weights.npy','wb') as file:

                nn.save(file,self.weights)

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

                try:
                    list.append(value[0])
                except:
                    list.append(value)
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
    def backward(self, actual, input):

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

    # predict the best chess move function
    def forwardChess(self, board):

        input = self.flatten(board)

        weightsLayerOne = nn.zeros((64,64))

        for y in range(0,64):

            for x in range(0,64):

                weightsLayerOne[y][x] = self.weights[y][x]

        biasLayerOne = nn.zeros((64,1))

        for y in range(0,64):

            for x in range(0,1):

                biasLayerOne[y][x] = self.bias[y][x]

        weightsLayerTwo = nn.zeros((4, 64))

        for y in range(0, 4):

            for x in range(64,128):

                weightsLayerTwo[y][x-64] = self.weights[y][x]

        biasLayerTwo = nn.zeros((4,1))

        for y in range(0, 4):

            for x in range(1, 2):

                biasLayerTwo[y][x-1] = self.bias[y][x]

        z = weightsLayerOne @ input + biasLayerOne
        a = self.leakyRelu(z)
        z = weightsLayerTwo @ a + biasLayerTwo
        y = self.leakyRelu(z)

        return y


    # a self learning functions for just chess
    def backwardChess(self, board, actual):

        ## TODO: self learning algorithm
        ## Plan:
        ## cost function is based on material lost
        ## once material loss is trained
        ## focus on optimizing the bot until it beats the other
        ## then make the other bot beat the bot that was beaten

        learnRate = 0.01

        input = self.flatten(board)

        weightsLayerOne = nn.zeros((64,64))

        for y in range(0,64):

            for x in range(0,64):

                weightsLayerOne[y][x] = self.weights[y][x]

        biasLayerOne = nn.zeros((64,1))

        for y in range(0,64):

            for x in range(0,1):

                biasLayerOne[y][x] = self.bias[y][x]

        weightsLayerTwo = nn.zeros((4, 64))

        for y in range(0, 4):

            for x in range(64,128):

                weightsLayerTwo[y][x-64] = self.weights[y][x]

        biasLayerTwo = nn.zeros((4,1))

        for y in range(0, 4):

            for x in range(1, 2):

                biasLayerTwo[y][x-1] = self.bias[y][x]

        # backwards propagation

        for i in range(0, 1000):

            zOne = weightsLayerOne @ input + biasLayerOne
            a = self.leakyRelu(zOne)
            zTwo = weightsLayerTwo @ a + biasLayerTwo
            y = self.leakyRelu(zTwo)

            biasGradient = self.leakyReluPrime(zTwo) * 2 * (y - actual)
            weightGradient = a * self.leakyReluPrime(zTwo) * 2 * (y - actual)

            print(weightGradient)

            biasLayerTwo = biasLayerTwo - (learnRate * biasGradient)
            weightsLayerTwo = weightsLayerTwo - (learnRate * weightGradient)

            #biasGradient = weightsLayerTwo @ self.leakyReluPrime(zOne) @ self.leakyReluPrime(zTwo).T * 2 * (y - actual).T
            #weightGradient = biasGradient * input.T

            #biasLayeOne = biasLayerOne - (learnRate * biasGradient)
            #weightsLayerOne = weightsLayerOne - (learnRate * weightGradient)


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
                self.backward(actual, image)

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

        output = nn.zeros((len(input),len(input[0])))

        for x in range(0, len(input)):

            for y in range(0, len(input[0])):

                if input[x][y] > 0.0:
                    output[x][y] = input[x][y]
                else:
                    output[x][y] = 0.1 * input[x][y]

        return output

    def leakyReluPrime(self, input):

        output = nn.zeros((len(input),len(input[0])))

        for x in range(0, len(input)):

            for y in range(0, len(input[0])):

                if input[x][y] > 0.0:
                    output[x][y] = 1.0
                else:
                    output[x][y] = 0.1

        return output

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
