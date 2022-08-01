import matplotlib.pyplot as plt
from collections import Counter
from warnings import warn
from PIL import Image
import threading
import numpy as nn
import random
import time
import os
import Chess

class DataOrganiser():

    def __init__(self):

        for engine in range(1,3):

            if not os.path.exists(f"Data"):
                os.mkdir(f"Data")
            if not os.path.exists(f"Engine{engine}"):
                os.mkdir(f"Engine{engine}")
            if not os.path.exists(f"Engine{engine}/Training"):
                os.mkdir(f"Engine{engine}/Training")

    def findMostCommonMove(self, dir, engine):

        try:
            numOfMoveFiles = len(os.listdir(f"Engine{engine}/Training/{dir}"))
        except:
            return None

        moveList = []

        for i in range(1, numOfMoveFiles):
            move = nn.load(f"Engine{engine}/Training/{dir}/Move{numOfMoveFiles - 1}.npy")
            moveList.append(move)

        move = Counter(moveList)

        print(move.most_common(1))

    def convertNotation(self, move):

        move = str(move)

        move = move.replace("Q","")
        move = move.replace("K","")
        move = move.replace("N","")
        move = move.replace("B","")
        move = move.replace("P","")
        move = move.replace("R","")
        move = move.replace("=","")
        move = move.replace("x","")

        legal_CoOrdinates = []

        if move == "O-O" and Chess.startup.white_turn:
            move = [1, 5, 1, 7]
        elif move == "O-O" and not Chess.startup.white_turn:
            move = [8, 5, 8, 7]
        elif move == "O-O-O" and Chess.startup.white_turn:
            move = [1, 5, 1, 3]
        elif move == "O-O-O" and not Chess.startup.white_turn:
            move = [8, 5, 8, 3]
        else:
            move.split()

        output = ''
        for value in move:

            if not str(value).isnumeric():

                value = Chess.notation.get_column_char(value) + 1

            output += str(f"{value} ")

        move = [int(x) for x in output.split()]

        if len(move) == 2:
            list = [0, 0]
            for item in move:
                list.append(item)
            move = list
        if len(move) == 3:
            list = [0]
            for item in move:
                list.append(item)
            move = list

        return nn.asarray(move)

    def saveGamePosition(self, item, file, engine):

        save = True

        newPosition = nn.load(f"Data/{item}/{file}/Board.npy")

        for position in os.listdir(f"Engine{engine}/Training"):

            oldPosition = nn.load(f"Engine{engine}/Training/{position}/Board.npy")

            if nn.array_equal(oldPosition, newPosition):

                try:
                    numOfMoveFiles = len(os.listdir(f"Engine{engine}/Training/{position}"))
                except:
                    numOfMoveFiles = 1

                save = False
                move = nn.load(f"Data/{item}/{file}/Move.npy")
                nn.save(f"Engine{engine}/Training/{position}/Move{numOfMoveFiles}.npy", move)

        if save:

            move = nn.load(f"Data/{item}/{file}/Move.npy")

            file = os.listdir(f"Engine{engine}/Training")
            amountOfFile = len(file)

            try:
                numOfMoveFiles = len(os.listdir(f"Engine{engine}/Training/Position{amountOfFile+1}"))
            except:
                numOfMoveFiles = 1

            os.mkdir(f"Engine{engine}/Training/Position{amountOfFile+1}")
            nn.save(f"Engine{engine}/Training/Position{amountOfFile+1}/Board.npy", newPosition)
            nn.save(f"Engine{engine}/Training/Position{amountOfFile+1}/Move{numOfMoveFiles}.npy", move)

    def organiseData(self):

        for item in os.listdir(f"Data"):

            try:
                winner = nn.load(f"Data/{item}/Winner.npy")
            except:
                winner = None

            if winner != None:
                if winner == 1:
                    black = True
                    white = False
                    engine = 2
                elif winner == -1:
                    white = True
                    black = False
                    engine = 1

                i = 0

                for file in os.listdir(f"Data/{item}"):

                    save = True

                    if file != "Winner.npy":

                        i += 1

                        if i % 2 == 0 and black:

                            self.saveGamePosition(item, file, engine)

                        elif white:

                            self.saveGamePosition(item, file, engine)

                        else:

                            pass

    def similarity(self, output, legal, promotion=False):

        if not promotion:


            output = nn.delete(output, len(output) - 1)
            min = 1e+2500

            if len(legal) > 1:

                for i in range(0, len(legal)):

                    output = nn.asarray(output).flatten()

                    if len(output) == 2:
                        val = [0, 0]
                        for item in output:
                            val.append(item)
                        output = val
                    if len(output) == 3:
                        val = [0]
                        for item in output:
                            val.append(item)
                        output = val

                    value = nn.asarray(legal[i])
                    value =  [int(d) for d in str(value)]

                    if len(value) == 2:
                        val = [0, 0]
                        for item in value:
                            val.append(item)
                        value = val
                    if len(value) == 3:
                        val = [0]
                        for item in value:
                            val.append(item)
                        value = val

                    diff = nn.asarray(output) - nn.asarray(value)

                    diff[diff < -1] = diff[diff < -1] * -1

                    difference = diff.sum()

                    difference /= len(value)

                    if difference < min:

                        min = difference
                        pos = i

            elif len(legal) == 1:
                return 0

            else:
                exit()

            return pos


class NeuralNetwork():

    def __init__(self):

        self.loopCounter = 0

        self.data = DataOrganiser()

        self.loadEngine(1)
        self.loadEngine(2)

        trainingEngineOne = threading.Thread(target=self.backwardChess, args=(1,))
        trainingEngineOne.start()

        trainingEngineTwo = threading.Thread(target=self.backwardChess, args=(2,))
        trainingEngineTwo.start()

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


    def engine(self):

        self.loopCounter += 1

        if self.loopCounter % 25 == 0 or self.loopCounter == 1:
            self.data.organiseData()

        actual_data = []
        legal_CoOrdinates = []

        for item in Chess.pieces.legal_moves:
            move = ""
            for item in self.data.convertNotation(item):

                move += str(item)

            legal_CoOrdinates.append(move)

        matrix = Chess.pieces.convert_pieces_to_matrix()

        train = True

        if Chess.startup.white_turn:
            CoOrdinates = self.forwardChess(matrix, 1, legal_CoOrdinates)
        else:
            CoOrdinates = self.forwardChess(matrix, 2, legal_CoOrdinates)

        if len(CoOrdinates) == 4:

            name = Chess.pieces.find_piece_name(int(CoOrdinates[0] - 1), int(CoOrdinates[1] - 1))

            if name == "none":
                name = ""

            Pawn = Chess.pieces.find_piece_name(int(CoOrdinates[0] - 1), int(CoOrdinates[1] - 1))

        #    print(Pawn, int(CoOrdinates[0] - 1), int(CoOrdinates[1] - 1))

            if int(CoOrdinates[0] -1) == -1 and int(CoOrdinates[1]-1) != -1:
                Pawn = True
            else:
                Pawn = False

            if Chess.pieces.find_piece_name(int(CoOrdinates[2] - 1), int(CoOrdinates[3] - 1)) == "none":

                xOne = str(Chess.notation.get_column(int(CoOrdinates[0]-1)))
                yOne = str(int(CoOrdinates[1]))
                xTwo = str(Chess.notation.get_column(int(CoOrdinates[2]-1)))
                yTwo = str(int(CoOrdinates[3]))

                if xOne.lower() == "none":
                    xOne = ""

                if yOne.lower() == "none":
                    yOne = ""
                if xTwo.lower() == "none":
                    xTwo = ""

                if yTwo.lower() == "none":
                    yTwo = ""

                move = name + xOne + yOne + xTwo + yTwo
            elif Pawn:

                xOne = str(Chess.notation.get_column(int(CoOrdinates[1]-1)))
                xTwo = str(Chess.notation.get_column(int(CoOrdinates[2]-1)))
                yTwo = str(int(CoOrdinates[3]))

                if xOne.lower() == "none":
                    xOne = ""

                if xTwo.lower() == "none":
                    xTwo = ""

                if yTwo.lower() == "none":
                    yTwo = ""

                move = xOne + "x" + xTwo + yTwo

                print("PAWN MOVe")
            else:
                xOne = str(Chess.notation.get_column(int(CoOrdinates[0]-1)))
                yOne = str(int(CoOrdinates[1]))
                xTwo = str(Chess.notation.get_column(int(CoOrdinates[2]-1)))
                yTwo = str(int(CoOrdinates[3]))

                if xOne.lower() == "none":
                    xOne = ""

                if yOne.lower() == "none":
                    yOne = ""
                if xTwo.lower() == "none":
                    xTwo = ""

                if yTwo.lower() == "none":
                    yTwo = ""

                move = name + xOne + yOne + "x" + xTwo + yTwo

        elif len(CoOrdinates) == 3:

            move = str(Chess.notation.get_column(int(CoOrdinates[0]-1))) + "x" + str(Chess.notation.get_column(int(CoOrdinates[1]-1))) + str(int(CoOrdinates[2]))
        elif len(CoOrdinates) == 2:
            move = str(Chess.notation.get_column(int(CoOrdinates[0]-1))) + str(int(CoOrdinates[1]))


        print(move)

        return move

    def forwardChess(self, board, engine, legal):

        self.loadEngine(engine)

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

        weightsLayerThree = nn.zeros((5, 64))

        for y in range(0, 5):

            for x in range(128,192):

                weightsLayerThree[y][x-128] = self.weights[y][x]

        biasLayerThree = nn.zeros((5,1))

        for y in range(0, 5):

            for x in range(2, 3):

                biasLayerThree[y][x-2] = self.bias[y][x]

        zOne = weightsLayerOne @ input + biasLayerOne
        aOne = self.tanh(zOne)
        zTwo = weightsLayerTwo @ aOne + biasLayerTwo
        aTwo = self.leakyRelu(zTwo)
        zThree = weightsLayerThree @ aTwo + biasLayerThree
        y = self.selu(zThree)

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

        print(output)

        output = legal[self.data.similarity(y, legal)]

        return [int(d) for d in str(output)]

    # a self learning functions for just chess
    def backwardChess(self, engine, plot=False, iter=100, learnRate=5e-5):

        self.loadEngine(engine)

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

        weightsLayerThree = nn.zeros((5, 64))

        for y in range(0, 5):

            for x in range(128,192):

                weightsLayerThree[y][x-128] = self.weights[y][x]

        biasLayerThree = nn.zeros((5,1))

        for y in range(0, 5):

            for x in range(2, 3):

                biasLayerThree[y][x-2] = self.bias[y][x]

        X = []
        Y = []

        minimum = 1e+10

        # backwards propagation
        while True:

            if not Chess.startup.run:

                exit()

            c = ([[0],[0],[0],[0]])

            cost = 0

            for dir in os.listdir(f"Engine{engine}/Training"):

                board = nn.load(f"Engine{engine}/Training/{dir}/Board.npy")

                actual = self.data.findMostCommonMove(dir, engine)
                actual = nn.matrix(self.data.convertNotation(actual))
                actual = actual.T
                actual = nn.asarray(actual.astype(nn.float))
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

                biasGradientThree[biasGradientThree > 1] = 1
                biasGradientThree[biasGradientThree < -1] = -1

                biasGradientTwo[biasGradientTwo > 1] = 1
                biasGradientTwo[biasGradientTwo < -1] = -1

                biasGradientOne[biasGradientOne > 1] = 1
                biasGradientOne[biasGradientOne  < -1] = -1

                weightGradientThree[weightGradientThree > 1] = 1
                weightGradientThree[weightGradientThree < -1] = -1

                weightGradientTwo[weightGradientTwo > 1] = 1
                weightGradientTwo[weightGradientTwo < -1] = -1

                weightGradientOne[weightGradientOne > 1] = 1
                weightGradientOne[weightGradientOne < -1] = -1

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

                c[c < -1] = c[c < -1] * -1

                cost += c.sum()

            if cost < minimum:

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

                for y in range(0, 5):
                    for x in range(128,192):

                        self.weights[y][x] = weightsLayerThree[y][x-128]

                for y in range(0, 5):
                    for x in range(2, 3):

                        self.bias[y][x] = biasLayerThree[y][x-2]

                self.saveEngine(engine)

                minimum = cost

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
