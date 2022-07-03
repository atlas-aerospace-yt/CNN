
#https://towardsdatascience.com/introduction-to-math-behind-neural-networks-e8b60dbbdeba

from Math import Math as math

class Engine():

    def __init__(self):

        self.w = math.random_array(64,5,-1,1)

        self.b = math.random_array(5,1,-1,1)

        self.board_one = [-0.5,-0.3,-0.35,-1,-0.8,-0.35,-0.3,-0.5,
                          -0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,
                          0,0,0,0,0,0,0,0,
                          0,0,0,0,0,0,0,0,
                          0,0,0,0,0,0,0,0,
                          0,0,0,0,0,0,0,0,
                          0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
                          0.5,0.3,0.35,1,0.8,0.35,0.3,0.5]

        self.move_one = [0.5, 0.2, 0.5, 0.4, 0.0]


    def forward_propagation(self):

        z = math.add(math.multiply(self.board_one, self.w), self.b)
        y = math.sigmoid(z)
        return y

    def backward_propagation(self):

        z = math.add(math.multiply(self.board_one, self.w), self.b)
        y = math.sigmoid(z)
        y_hat = self.move_one

        n = len(self.board_one)

        delC_delwi = 2 / n * math.sum(math.subtract(y,y_hat))

        return delC_delwi

    def sigmoid(self, x):

        return 1 / (1 + math.exp(-x))

engine = Engine()
print(engine.forward_propagation())
print(engine.backward_propagation())
