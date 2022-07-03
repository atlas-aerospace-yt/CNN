import random

E = 2.71828
PI = 3.14159265

class Math():

    def sigmoid(x):
        answer= []
        for value in x:
            answer.append(1 / (1 + E ** (-value)))
        return answer

    def multiply(x, y):
        answer = []
        for height in range(0, len(y)):
            sum = 0
            for width in range(0, len(x)):
                sum += x[width] * y[height][width]
            answer.append(sum)
        return answer

    def add(x, y):
        answer = []
        for i in range(0, len(x)):
            answer.append(float(x[i]) + float(y[i]))
        return answer

    def subtract(x, y):
        answer = []
        for i in range(0, len(x)):
            answer.append(float(x[i]) - float(y[i]))
        return answer

    def sum(x):
        answer=0
        for i in range(0, len(x)):
            answer += x[i]
        return answer

    def random_array(x, y, lower, upper):

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
            return answer[0]
        return answer
