import matplotlib.pyplot as plt
from warnings import warn
from PIL import Image
import numpy as nn
import random
import time
import os

class NeuralNetwork():

    def __init__(self):

        for engine in range(1,3):
            if not os.path.exists(f"Engine{engine}"):
                os.mkdir(f"Engine{engine}")
            if not os.path.exists(f"Engine{engine}/Training"):
                os.mkdir(f"Engine{engine}/Training")

        self.width = 8
        self.height = 8

        self.loadEngine(1)
        self.loadEngine(2)

    def loadEngine(self, engine):

        try:

            with open(f'Engine{engine}/weights.npy','rb') as file:

                self.weights = nn.load(file)

            with open(f'Engine{engine}/bias.npy','rb')  as file:

                self.bias = nn.load(file)

        except:

            self.weights = nn.random.uniform(-1,1,(64,192))
            self.bias = nn.random.uniform(-1,1,(64,3))

            with open(f'Engine{engine}/weights.npy','wb') as file:

                nn.save(file,self.weights)

            with open(f'Engine{engine}/bias.npy','wb') as file:

                nn.save(file, self.bias)

    def saveEngine(self, engine):

        with open(f'Engine{engine}/weights.npy','wb') as file:

            nn.save(file, self.weights)

        with open(f'Engine{engine}/bias.npy','wb') as file:

            nn.save(file, self.bias)


    def find_similarity(self, output, legal):

        min = 1e+2500

        if len(legal) > 1:
            for i in range(0, len(legal)):
                value = legal[i]
                value.split()
                difference = 0
                if len(value) == 4:
                    for i in range(0, len(value)):
                        difference += float(output[i]) - float(value[i])
                    difference /= 4
                elif len(value) == 3:
                    for i in range(0, len(value)):
                        difference += float(output[i+1]) - float(value[i])
                    difference /= 3
                else:
                    for i in range(0, len(value)):
                        difference += float(output[i+2]) - float(value[i])
                    difference /= 2

                if difference > min and difference < 0 - min or difference < min and difference > 0 - min:
                    min = difference
                    pos = i
        elif len(legal) == 1:
            return 0

        else:
            print("no legal mnoves")
            exit()

        return pos

    def savePos(self, board, actual):

        engine = 1

        for item in os.listdir(f"Engine{engine}/Training"):
            prev = nn.load(f"Engine{engine}/Training/{item}/Board.npy")
            comparison = prev == board
            equal_arrays = comparison.all()
            if equal_arrays:

                nn.save(f"Engine{engine}/Training/{item}/Board.npy", board)
                nn.save(f"Engine{engine}/Training/{item}/Answer.npy", actual)

                return 0

        list = os.listdir(f"Engine{engine}/Training")
        pos = len(list)

        os.mkdir(f"Engine{engine}/Training/Position{pos+1}")
        nn.save(f"Engine{engine}/Training/Position{pos+1}/Board.npy",board)
        nn.save(f"Engine{engine}/Training/Position{pos+1}/Answer.npy",actual)

    def forwardChess(self, board, engine, legal):

        save = True

        for item in os.listdir(f"Engine{engine}/Training"):
            prev = nn.load(f"Engine{engine}/Training/{item}/Board.npy")
            comparison = prev == board
            equal_arrays = comparison.all()
            if equal_arrays:
                save = False
                break

        self.loadEngine(engine)
        list = os.listdir(f"Engine{engine}/Training")
        pos = len(list)
        if save == True:
            os.mkdir(f"Engine{engine}/Training/Position{pos+1}")
            nn.save(f"Engine{engine}/Training/Position{pos+1}/Board.npy",board)


        input = self.flatten(board)

        weightsLayerOne = nn.zeros((64,64))

        for y in range(0,64):

            for x in range(0,64):

                weightsLayerOne[y][x] = self.weights[y][x]

        biasLayerOne = nn.zeros((64,1))

        for y in range(0,64):

            for x in range(0,1):

                biasLayerOne[y][x] = self.bias[y][x]

        weightsLayerTwo = nn.zeros((64,64))

        for y in range(0,64):

            for x in range(64,128):

                weightsLayerTwo[y][x-64] = self.weights[y][x]

        biasLayerTwo = nn.zeros((64,1))

        for y in range(0,64):

            for x in range(1,2):

                biasLayerTwo[y][x-1] = self.bias[y][x]

        weightsLayerThree = nn.zeros((4, 64))

        for y in range(0, 4):

            for x in range(128,192):

                weightsLayerThree[y][x-128] = self.weights[y][x]

        biasLayerThree = nn.zeros((4,1))

        for y in range(0, 4):

            for x in range(2, 3):

                biasLayerThree[y][x-2] = self.bias[y][x]

        zOne = weightsLayerOne @ input + biasLayerOne
        aOne = self.tanh(zOne)
        zTwo = weightsLayerTwo @ aOne + biasLayerTwo
        aTwo = self.leakyRelu(zTwo)
        zThree = weightsLayerThree @ aTwo + biasLayerThree
        y = self.selu(zThree)

        if save == True:
            move = legal[self.find_similarity(y, legal)]

            if len(move) == 2:
                value = [0,0]
                for val in move:
                    value.append(val)
                move = value
            elif len(move) == 3:
                value = [0]
                for val in move:
                    value.append(val)
                move = value
            elif len(move) == 4:
                value = []
                for val in move:
                    value.append(val)
                move = value
            nn.save(f"Engine{engine}/Training/Position{pos+1}/Answer.npy",move)

        else:

            for item in os.listdir(f"Engine{engine}/Training"):
                prev = nn.load(f"Engine{engine}/Training/{item}/Board.npy")
                comparison = prev == board
                equal_arrays = comparison.all()
                if equal_arrays:
                    move = nn.asarray(nn.load(f"Engine{engine}/Training/{item}/Answer.npy"))

        cost = self.backwardChess(engine)
        #cost = 0

        y = nn.rint(y)
        y = y.tolist()

        if y[0][0] <= 0 and y[1][0] <= 0:
            y.pop(0)
            y.pop(0)

        elif y[0][0] <= 0:
            y.pop(0)

        output = []
        for val in y:
            output.append(val[0])

        return output, move, cost


    # a self learning functions for just chess
    def backwardChess(self, engine, plot=False, iter=100, learnRate=5e-5):

        self.loadEngine(engine)

        ## TODO: self learning algorithm

        weightsLayerOne = nn.zeros((64,64))

        for y in range(0,64):

            for x in range(0,64):

                weightsLayerOne[y][x] = self.weights[y][x]

        biasLayerOne = nn.zeros((64,1))

        for y in range(0,64):

            for x in range(0,1):

                biasLayerOne[y][x] = self.bias[y][x]

        weightsLayerTwo = nn.zeros((64,64))

        for y in range(0,64):

            for x in range(64,128):

                weightsLayerTwo[y][x-64] = self.weights[y][x]

        biasLayerTwo = nn.zeros((64,1))

        for y in range(0,64):

            for x in range(1,2):

                biasLayerTwo[y][x-1] = self.bias[y][x]

        weightsLayerThree = nn.zeros((4, 64))

        for y in range(0, 4):

            for x in range(128,192):

                weightsLayerThree[y][x-128] = self.weights[y][x]

        biasLayerThree = nn.zeros((4,1))

        for y in range(0, 4):

            for x in range(2, 3):

                biasLayerThree[y][x-3] = self.bias[y][x]

        X = []
        Y = []

        # backwards propagation
        for i in range(0, iter):

            cost = 0

            c = ([[0],[0],[0],[0]])

            for item in os.listdir(f"Engine{engine}/Training"):

                board = nn.load(f"Engine{engine}/Training/{item}/Board.npy")
                actual = nn.asmatrix(nn.load(f"Engine{engine}/Training/{item}/Answer.npy"))
                actual = actual.T
                actual = actual.astype(nn.float)
                actual = nn.asarray(actual)
                input = self.flatten(board)

                zOne = weightsLayerOne @ input + biasLayerOne
                aOne = self.tanh(zOne)
                zTwo = weightsLayerTwo @ aOne + biasLayerTwo
                aTwo = self.leakyRelu(zTwo)
                zThree = weightsLayerThree @ aTwo + biasLayerThree
                y = self.selu(zThree)

                c = y - actual

                biasGradientThree = 2 * c * self.seluPrime(zThree)
                weightGradientThree = 2 * c * self.seluPrime(zThree) @ aTwo.T

                biasGradientTwo = (2 * c * self.seluPrime(zThree)).T @ weightsLayerThree * self.leakyReluPrime(zTwo)
                weightGradientTwo = (2 * c * self.seluPrime(zThree)).T @ weightsLayerThree * self.leakyReluPrime(zTwo) @ aOne

                biasGradientOne = (2 * c * self.seluPrime(zThree)).T @ weightsLayerThree * self.leakyReluPrime(zTwo) @ weightsLayerTwo * self.tanhPrime(zOne)
                weightGradientOne = (2 * c * self.seluPrime(zThree)).T @ weightsLayerThree * self.leakyReluPrime(zTwo) @ weightsLayerTwo * self.tanhPrime(zOne) @ input

                array_sum = nn.sum(biasGradientThree)
                if nn.isnan(array_sum):
                    break
                array_sum = nn.sum(weightGradientThree)
                if nn.isnan(array_sum):
                    break
                array_sum = nn.sum(biasGradientTwo)
                if nn.isnan(array_sum):
                    break
                array_sum = nn.sum(weightGradientTwo)
                if nn.isnan(array_sum):
                    break
                array_sum = nn.sum(biasGradientOne)
                if nn.isnan(array_sum):
                    break
                array_sum = nn.sum(weightGradientOne)
                if nn.isnan(array_sum):
                    break


                biasLayerThree = biasLayerThree - (learnRate * biasGradientThree)
                weightsLayerThree = weightsLayerThree - (learnRate * weightGradientThree)

                biasLayeTwo = biasLayerTwo - (learnRate * biasGradientTwo)
                weightsLayerTwo = weightsLayerTwo - (learnRate * weightGradientTwo)

                biasLayeOne = biasLayerOne - (learnRate * biasGradientOne)
                weightsLayerOne = weightsLayerOne - (learnRate * weightGradientOne)

                cost += c

            if plot:

                X.append(i)

                temp = []

                for item in cost:
                    temp.append(item[0])
                Y.append(temp)

        if plot:

            plt.plot(X,Y)
            plt.show()

        for y in range(0,64):
            for x in range(0,64):

                self.weights[y][x] = weightsLayerOne[y][x]

        for y in range(0,64):
            for x in range(0,1):

                self.bias[y][x] = biasLayerOne[y][x]

        for y in range(0,64):
            for x in range(64,128):

                self.weights[y][x] = weightsLayerTwo[y][x-64]

        for y in range(0,64):
            for x in range(1,2):

                self.bias[y][x] = biasLayerTwo[y][x-1]

        for y in range(0, 4):
            for x in range(128,192):

                self.weights[y][x] = weightsLayerThree[y][x-128]

        for y in range(0, 4):
            for x in range(2, 3):

                self.bias[y][x] = biasLayerThree[y][x-2]

        self.saveEngine(engine)

        return cost

    def tanh(self, input):

        return (nn.exp(input)-nn.exp(-input))/(nn.exp(input)+nn.exp(-input))

    def tanhPrime(self, input):

        return 1 - ((nn.exp(input)-nn.exp(-input))/(nn.exp(input)+nn.exp(-input))) ** 2

    def sigmoid(self, input):

        return 1 / (1 + nn.exp(-input))

    def sigmoidPrime(self, input):

        return self.sigmoid(input) * (1.0 - self.sigmoid(input))

    def selu(self, input):

        SCALE = 1.05070098
        ALPHA = 1.67326324

        output = nn.zeros((len(input),len(input[0])))

        for x in range(0, len(input)):

            for y in range(0, len(input[0])):

                if input[x][y] > 0.0:
                    output[x][y] = SCALE * input[x][y]
                else:
                    output[x][y] =  SCALE * ALPHA * (nn.exp(input[x][y]) - 1)

        return output

    def seluPrime(self, input):

        SCALE = 1.05070098
        ALPHA = 1.67326324

        output = nn.zeros((len(input),len(input[0])))

        for x in range(0, len(input)):

            for y in range(0, len(input[0])):

                if input[x][y] > 0.0:
                    output[x][y] = SCALE
                else:
                    output[x][y] = SCALE * ALPHA * nn.exp(input[x][y])

        return output

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
