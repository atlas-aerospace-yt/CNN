import matplotlib.pyplot as plt
import numpy as np
import random

weights = [1, 1]
bias  = [1, 1]

def forward(input):

    # layer one pass
    layerOneOutput = weights[0] * input + bias[0]

    # activation function for layer one
    layerOneOutput = sigmoid(layerOneOutput)

    # layer two output
    layerTwoOutput = weights[1] * layerOneOutput + bias[1]

    # activation function for layer two
    output = sigmoid(layerTwoOutput)

    return output

def backward(input, actual):

    # define learn learnRate
    learnRate = 0.1

    # layer one pass
    layerOneOutput = weights[0] * input + bias[0]

    # activation function for layer one
    layerTwoInput = sigmoid(layerOneOutput)

    # layer two output
    layerTwoOutput = weights[1] * layerTwoInput + bias[1]

    # activation function for layer two
    output = sigmoid(layerTwoOutput)

    # gradient calculations layer two
    biasGradient = sigmoidPrime(output) * 2 * (output - actual)
    weightGradient = biasGradient * layerTwoInput

    # applying the gradient layer two
    weights[1] = weights[1] - learnRate * weightGradient
    bias[1] = bias[1] - learnRate * biasGradient

    # gradient calculations layer one
    biasGradient = sigmoidPrime(layerTwoInput) * weights[1] * sigmoidPrime(output) * 2 * (output - actual)
    weightGradient = biasGradient * input

    # applying the gradient layer one
    weights[0] = weights[0] - learnRate * weightGradient
    bias[0] = bias[0] - learnRate * biasGradient

    # calculate cost
    cost = (output - actual)

    return weights, bias, cost

# mathematical activation functions
def sigmoid(input):

    return 1 / (1 + np.exp(-input))

def sigmoidPrime(input):

    return sigmoid(input) * (1.0 - sigmoid(input))


if __name__ == "__main__":

    costFunc = []

    for i in range(0, 10000):

        weights, bias, cost = backward(1, 0)
        weights, bias, cost = backward(0, 1)
        costFunc.append(cost)

    axis = []

    for num in range(0, len(costFunc)):
        axis.append(num)

    plt.plot(axis, costFunc)
    plt.show()

    print(forward(1))
    print(forward(0))
