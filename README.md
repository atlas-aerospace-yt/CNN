# Python CNN

This is a Neural Network built in python designed to recognise shapes in a 21x21 grid of black and white pixels.

## What is this code

This code contains a single layer Neural Network which takes a 21x21 image as a 441 element Vector to detect wether the shape is a triangle, circle or square. The training data is a very small data set and the accuracy of this network will be small as it is only a single layer with few examples.</br>
The code will go through every file in "TestingData" that is a .png and will attempt to identify its shape.

## Directory Structure

```
CNN
|
|-- ANN             # Has the Weights and biases of the neural network
|   
|-- TestingData     # Contains the unknown 21x21 black and white images
|
|-- TrainingData    # Contains all labeled data in the form of "shape"_"number".png
|
|-- CNN.py          # The Neural Network libary created with Numpy 
|-- Main.py         # The main file to be run, currently set to train=False
```

## Dependencies

```
pip install PIL
pip install matplotlib
pip install numpy
```
