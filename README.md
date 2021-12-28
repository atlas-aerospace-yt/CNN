# Abstract

This is an ongoing project to create an easy to use Neural Network in python.

The goal is to be able to enter inputs and outputs then have the entire model calculated and trained with no fuss.

Currently, the code is able to recognise patterns in an input with a single output.

The code now works on 21x21 pixel images to recognise shapes.

To change the input dimensions you need to change the input = np.zeros((21 , 21)) to the image size.
In the future this will be done automatically and you can just input a data set or image.

Eventually the code will be able to recognise patters in any data sets e.g. Images or arrays.

# Dependencies

To run this library you will need to have installed:

matplotlib       pip install matplotlib

image_slicer     pip install image-slicer

numpy            pip install numpy

pillow           pip install Pillow

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
