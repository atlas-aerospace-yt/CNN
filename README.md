# Abstract

This is an ongoing project to create an easy to use Neural Network in python.

The goal is to be able to enter inputs and outputs then have the entire model calculated and trained with no fuss.

Currently, the code generates the model with random weights and can do forward propagation with the random weights.

Eventually the code will be able to recognise patters in any data sets e.g. Images or arrays.


# Maths

The code is designed to calculate the weight matrix size, bias matrix size and output matrix based off an:
input
number of outputs
number of layers

The forwards propagation is simply : Z = sigmoid(x * w + b)

The backwards propagation is still in progress and taking longer than expected
# Note:

The code doesn't fully work yet, the forwards propagation works however I'm still working on the backwards propagation.
If you have any ideas how to fix the backwards propagation please fork.
