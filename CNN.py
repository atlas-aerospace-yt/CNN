import torch
import torch.nn as nn

X = torch.tensor([1, 2, 3, 4], dtype=torch.float32)
Y = torch.tensor([2, 4, 6, 8], dtype=torch.float32)

w = torch.tensor(0.0, dtype=torch.float32, requires_grad=True)

def forward(x):
    return w * x

def loss(y, y_predicted):
    return((y_predicted - y) ** 2).mean()

print(f'Prediction before training: f(5) = {forward(4):.3f}')

learning_rate = 0.01
n_iters = 100

for epoch in range(n_iters):

    y_pred = forward(X)
    l = loss(Y, y_pred)
    l.backward()

    with torch.no_grad():
        w -= learning_rate * w.grad
    w.grad.zero_()

print(f'Prediction after training: f(5) = {forward(4):.3f}')
