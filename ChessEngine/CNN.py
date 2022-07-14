from Math import Vector as v

def backward_propagation(x, y, w, b):

    #forward propagation math
    z = x * w + b
    y_hat = v.sigmoid(z)

    n = len(x)

    #gradient calculation
    w_grad = []
    for i in range(0, n):
        w_grad.append((v.sigmoid(z) * v([1 - v.sigmoid(z)[0]]) * v([x[i]]) * (2/n) * v.sum(y-y_hat))[0])

    w = w + v(w_grad) * 0.1

    b_grad = v.sigmoid(z) * v([1 - v.sigmoid(z)[0]]) * (2/n) * v.sum(y-y_hat)
    b = b + b_grad * 0.1

    return w, b

if __name__ == "__main__":

    #defining necesary variables
    w = v.random_array(3,1)
    b = v.random_array(1,1)

    #for loop for training iterations
    for i in range(0, 10000):

        if i % 2 == 0:
            x = v([0.1,0.1,0.5])
            y = v([0])
        else:
            x = v([0.1,1,0.5])
            y = v([1])

        w, b = backward_propagation(x, y, w, b)

    x = v([0.1,0.1,0.5])
    z = x * w + b
    print(v.sigmoid(z))

    x = v([1,0.1,1])
    z = x * w + b
    print(v.sigmoid(z))
