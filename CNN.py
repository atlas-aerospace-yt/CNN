import numpy as nn
import random

class NeuralNetwork():


    def __init__(self, matrix):

        self.loadNetwork(matrix)

    def loadNetwork(self, matrix):

        try:

            with open('weights.npy','rb') as file:

                self.LayerOneWeights = nn.load(file)

                print(self.LayerOneWeights)

        except:

            self.LayerOneWeights = nn.zeros((len(matrix) * len(matrix[0]), LayerInput))


    def save(self):

        with open('weights.npy','wb') as file:

            nn.save(file, self.LayerOneWeights)

    def flatten(self, matrix):

        width = len(matrix)
        height = len(matrix[0])

        output = []

        for x in range(0,height):

            for y in range(0,width):

                num = matrix[x][y]

                output.append(num)

        return output

    def hiddenLayer(self, matrix):

        matrix = nn.dot(matrix, self.LayerOneWeights)

        return matrix

    def forward(self,input):

        x = self.flatten(input)
        x = self.hiddenLayer(x)


        self.save()

        print(x)

input = ([[1,2, 3, 4, 5, 6, 7, 8],
        [9, 10,11,12,13,14,15,16],
        [17,18,19,20,21,22,23,24],
        [25,26,27,28,29,30,31,32],
        [33,34,35,36,37,38,39,40],
        [41,42,43,44,45,46,47,48],
        [49,50,51,52,53,54,55,56],
        [57,58,59,60,61,62,63,64]])

model = NeuralNetwork(input)

model.forward(input)
