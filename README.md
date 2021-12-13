# Abstract

This is an ongoing project to create an easy to use Neural Network in python.

The goal is to be able to enter inputs and outputs then have the entire model calculated and trained with no fuss.

Currently, the code is able to recognise patterns in an input with a single output.

The code is being tested on an 8x8 bit image that is printed with PIL.

Eventually the code will be able to recognise patters in any data sets e.g. Images or arrays.


# Maths

The code is designed to calculate the weight matrix size, bias matrix size and output matrix based off an:
input
number of outputs
number of layers

The forwards propagation is simply :

Z = sigmoid(x * w + b)

The backwards propagation is still in progress but is currently only an input output layer:

dCdb = sigmoid'(Z) * 2 * (Y - YHat)
dCdw = dCdb * x

# Note:

The code doesn't fully work yet, the forwards propagation works however I'm still working on the backwards propagation.
If you have any ideas how to fix the backwards propagation please fork.
