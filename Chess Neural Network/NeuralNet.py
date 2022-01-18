import matplotlib.pyplot as plt
from warnings import warn
from PIL import Image
import numpy as nn
import random
import os

class NeuralNetwork():

    def __init__(self):

        self.width = 8
        self.height = 8

        self.loadEngineOne()
        self.loadEngineTwo()

    def loadEngineOne(self):

        try:

            with open('Engine1/weights.npy','rb') as file:

                self.weights = nn.load(file)

            with open('Engine1/bias.npy','rb')  as file:

                self.bias = nn.load(file)

        except:

            self.weights = nn.random.uniform(-1, 1, (64,128))
            self.bias = nn.random.uniform(-1, 1, (64,2))

            with open('Engine1/weights.npy','wb') as file:

                nn.save(file,self.weights)

            with open('Engine1/bias.npy','wb') as file:

                nn.save(file, self.bias)

    def loadEngineTwo(self):

        try:

            with open('Engine2/weights.npy','rb') as file:

                self.weights = nn.load(file)

            with open('Engine2/bias.npy','rb')  as file:

                self.bias = nn.load(file)

        except:

            self.weights = nn.random.uniform(-1, 1, (64,128))
            self.bias = nn.random.uniform(-1, 1, (64,2))

            with open('Engine2/weights.npy','wb') as file:

                nn.save(file,self.weights)

            with open('Engine2/bias.npy','wb') as file:

                nn.save(file, self.bias)

    # save the weight and bias matrices
    def saveEngineOne(self):

        with open('Engine1/weights.npy','wb') as file:

            nn.save(file, self.weights)

        with open('Engine1/bias.npy','wb') as file:

            nn.save(file, self.bias)

    def saveEngineTwo(self):

        with open('Engine2/weights.npy','wb') as file:

            nn.save(file, self.weights)

        with open('Engine2/bias.npy','wb') as file:

            nn.save(file, self.bias)

    def find_similarity(self, output, legal):

        #print(legal)

        for i in range(0, len(legal)):
            difference =1000
            min = 1000
            value = legal[i]
            value.split()
            if len(value) == 4:
                for i in range(0, len(value)):
                    difference += float(output[i]) - float(value[i])
                difference /= 4
            elif len(value) == 3:
                for i in range(0, len(value)):
                    difference += float(output[i]) - float(value[i])
                difference /= 3
            else:
                for i in range(0, len(value)):
                    difference += float(output[i+2]) - float(value[i])
                difference /= 2
            if difference >= min and difference < 0 or difference <= min and difference > 0:
                min = difference
                pos = i

        return pos

    def forwardChess(self, board, engine, legal):

        save = True

        for item in os.listdir("Engine1/Training"):
            prev = nn.load(f"Engine1/Training/{item}/Board.npy")

            comparison = prev == board
            equal_arrays = comparison.all()

            if equal_arrays:
                save = False
                break

        if engine == 1:
            self.loadEngineOne()
            if save == True:
                list = os.listdir("Engine1/Training")
                pos = len(list)
                os.mkdir(f"Engine1/Training/Position{pos+1}")
                nn.save(f"Engine1/Training/Position{pos+1}/Board.npy",board)
        else:
            self.loadEngineTwo()
            if save == True:
                list = os.listdir("Engine2/Training")
                pos = len(list)
                os.mkdir(f"Engine2/Training/Position{pos+1}")
                nn.save(f"Engine1/Training/Position{pos+1}/Board.npy",board)

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

        item = legal[self.find_similarity(y, legal)]

        if len(item) == 2:

            value = [-1,-1]

            for val in item:

                value.append(val)

            item = value

        if save == True:
            nn.save(f"Engine1/Training/Position{pos+1}/Answer.npy",item)

        self.backwardChess(engine)

        z = weightsLayerOne @ input + biasLayerOne
        a = self.leakyRelu(z)
        z = weightsLayerTwo @ a + biasLayerTwo
        y = self.leakyRelu(z)

        y = nn.rint(y)

        y = y.tolist()

        if y[0][0] == -1 and y[1][0] == -1:
            y.pop(0)
            y.pop(0)

        elif y[0] == -1:
            y.pop(0)

        output = []
        for item in y:
            output.append(item[0])

        return output


    # a self learning functions for just chess
    def backwardChess(self, engine, plot=False):

        if engine == 1:
            self.loadEngineOne()
        else:
            self.loadEngineTwo()

        ## TODO: self learning algorithm
        learnRate = 0.0001

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

        x = 0
        graph = []
        cost = []

        # backwards propagation
        for i in range(0, 10000):

            for item in os.listdir("Engine1/Training"):

                board = nn.load(f"Engine1/Training/{item}/Board.npy")
                actual = nn.asmatrix(nn.load(f"Engine1/Training/{item}/Answer.npy"))
                actual = actual.T
                actual = actual.astype(nn.float)
                actual = nn.asarray(actual)
                input = self.flatten(board)

                zOne = weightsLayerOne @ input + biasLayerOne
                a = self.leakyRelu(zOne)
                zTwo = weightsLayerTwo @ a + biasLayerTwo
                y = self.leakyRelu(zTwo)

                biasGradient = 2 * (y - actual) * self.leakyReluPrime(zTwo)
                weightGradient = 2 * (y - actual) * self.leakyReluPrime(zTwo) * a.T

                biasLayerTwo = biasLayerTwo - (learnRate * biasGradient)
                weightsLayerTwo = weightsLayerTwo - (learnRate * weightGradient)

                biasGradient = (2 * (y - actual) * self.leakyReluPrime(zTwo)).T @ weightsLayerTwo * self.leakyReluPrime(zOne)
                weightGradient = (2 * (y - actual) * self.leakyReluPrime(zTwo)).T @ weightsLayerTwo * self.leakyReluPrime(zOne) * input.T

                biasLayeOne = biasLayerOne - (learnRate * biasGradient)
                weightsLayerOne = weightsLayerOne - (learnRate * weightGradient)

                if plot == True:

                    temp = []

                    for val in range(0,len(y)):

                        temp.append(float((y[val]-actual[val])**2))

                    cost.append(temp)
                    graph.append(x)

                    x += 1

        for y in range(0,64):

            for x in range(0,64):

                self.weights[y][x] = weightsLayerOne[y][x]
        for y in range(0,64):

            for x in range(0,1):

                self.bias[y][x] = biasLayerOne[y][x]
        for y in range(0, 4):

            for x in range(64,128):

                self.weights[y][x] = weightsLayerTwo[y][x-64]
        for y in range(0, 4):

            for x in range(1, 2):

                self.bias[y][x] = biasLayerTwo[y][x-1]

        if engine == 1:
            self.saveEngineOne()
        else:
            self.saveEngineTwo()

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
