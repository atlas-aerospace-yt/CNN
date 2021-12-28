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

matplotlib       (pip install matplotlib)

image_slicer     (pip install image-slicer)

numpy            (pip install numpy)

pillow           (pip install Pillow)

# Maths

The code currently generates its own model dimensions and does backwards propagation on small images.

The formula for the model is standard forwards and backwards propagation:


z = wx + b

a = sigmoid(z)


w is the weight

x is the input

b is the bias

a is the layer output


The way a Neural Network works, is it takes the input and passes it through forward propagation. Then,
to train the model you use the chain rule to calculate the gradient of the weights and biases with respect 
to the cost. The cost is simply the (output predicted - the wanted output) squared. The formula to calcule the gradient
with a single layer is:


dC/db = sigmoidPrime(a) * 2 * (y - yHat)

dC/dw = x * sigmoidPrime(a) * 2 * (y - yHat)


y is the output  of model

yHat is the wanted output


Then, this gradient is used to calculate the change to be applied to the network using the simple equation:


w = w - (l * dC/dw)

b = b - (l * dC/db)


l is the learn rate usually 1 or less
