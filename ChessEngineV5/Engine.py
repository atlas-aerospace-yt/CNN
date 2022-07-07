
#https://towardsdatascience.com/introduction-to-math-behind-neural-networks-e8b60dbbdeba

from Math import Math as math

class Engine():

    def __init__(self):

        self.w = math.random_array(64,5,-0.1,0.1)

        self.b = math.random_array(5,1,-0.1,0.1)

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

        for i in range(0, 10000):
            z = math.add(math.multiply(self.board_one, self.w), self.b)
            y = self.move_one
            y_hat = math.sigmoid(z)
            alpha = 0.1
            n = len(self.board_one)

            delC_delwi_matrix = []
            for height in range(0, len(y)):

                delC_delwi_vector = []

                for width in range(0, len(self.w)):
                    delC_delwi = 2 / n * (math.sum(math.subtract(y,y_hat)) * math.sigmoid(z[height]) * (1 - math.sigmoid(z[height])) * self.board_one[width])
                    delC_delwi_vector.append(delC_delwi)

                delC_delwi_matrix.append(delC_delwi_vector)

            delC_delbi_vector = []

            for i in range(0, len(y)):
                delC_delbi = 2 / n * (math.sum(math.subtract(y,y_hat)) * math.sigmoid(z[i]) * (1 - math.sigmoid(z[i])))
                delC_delbi_vector.append(delC_delbi)

            for height in range(0, len(y)):
                for width in range(0, len(self.w)):
                    self.w[height][width] = self.w[height][width] - alpha * delC_delwi_matrix[height][width]

            for i in range(0, len(y)):
                self.b[i] = self.b[i] - alpha * delC_delbi_vector[i]

            print(math.sum(math.subtract(y,y_hat)))

    def sigmoid(self, x):

        return 1 / (1 + math.exp(-x))

engine = Engine()
engine.backward_propagation()
print(engine.forward_propagation())
