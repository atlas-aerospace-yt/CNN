import random
from dataclasses import dataclass

E = 2.71828
PI = 3.14159265

@dataclass
class Vector():
    def __init__(self, vector):

        self.vector = vector

    def __sub__(self, other):
        answer = []
        if isinstance(other, Vector):
            for i in range(0, len(self)):
                answer.append(float(self[i]) - float(other[i]))
            return Vector(answer)
        elif isinstance(other, int) or isinstance(other, float):
            for i in range(0, len(self)):
                answer.append(float(self[i]) - other)
            return Vector(answer)

    def __add__(self, other):

        answer = []
        if isinstance(other, Vector):
            for i in range(0, len(self)):
                answer.append(float(self[i]) + float(other[i]))
            return Vector(answer)
        elif isinstance(other, int) or isinstance(other, float):
            for i in range(0, len(self)):
                answer.append(float(self[i]) + other)
            return Vector(answer)

    def __mul__(self, other):
        answer = []
        if isinstance(other, float) or isinstance(other, int):
            for item in self:
                answer.append(item * other)
        else:
            sum = 0
            for width in range(0, len(self)):
                sum += self[width] * other[width]
            answer = [float(sum)]
        return Vector(answer)

    def __getitem__(self, indx):
        return self.vector[indx]

    def __len__(self):
        return len(self.vector)

    def __str__(self):
        return f"{self.vector}"

    def random_array(x, y, lower=-0.1, upper=0.1):

        # Generates list of random values
        #        x
        #    ----------
        #   |
        # y |
        #   |

        answer = []
        for height in range(0,y):
            list  = []
            for width in range(0,x):
                num = random.uniform(lower, upper)
                list.append(num)
            answer.append(list)
        if y == 1:
            return Vector(answer[0])
        return Vector(answer)

    def sigmoid(x):

        if isinstance(x, Vector):
            output = []
            for item in x:
                output.append(1 / (1 + E ** (-item)))
            return Vector(output)
        elif isinstance(x, float) or isinstance(x, int):

            return 1 / (1 + E ** (-x))

    def sum(x):
        sum = 0
        for item in x:
            sum += item
        return sum
