
# Chess engine class
class Engine():

    def __init__(self):
        pass

    # returns list of pieces in the shape of a board
    def fen_to_matrix(self, fen):
        position = fen.split(" ")[0].split("/")

        pawn = 0.1
        knight = 0.3
        bishop = 0.3
        rook = 0.5
        queen = 0.9
        king = 1.0

        position_matrix = []
        for row in position:
            pieces_in_row  = []
            for character in row:
                if character.isnumeric():
                    for i in range(0, int(character)):
                        pieces_in_row.append(0)
                elif character.lower() == "p":
                    if character.isupper():
                        pieces_in_row.append(pawn)
                    else:
                        pieces_in_row.append(-pawn)
                elif character.lower() == "n":
                    if character.isupper():
                        pieces_in_row.append(knight)
                    else:
                        pieces_in_row.append(-knight)
                elif character.lower() == "b":
                    if character.isupper():
                        pieces_in_row.append(bishop)
                    else:
                        pieces_in_row.append(-bishop)
                elif character.lower() == "r":
                    if character.isupper():
                        pieces_in_row.append(rook)
                    else:
                        pieces_in_row.append(-rook)
                elif character.lower() == "q":
                    if character.isupper():
                        pieces_in_row.append(queen)
                    else:
                        pieces_in_row.append(-queen)
                elif character.lower() == "k":
                    if character.isupper():
                        pieces_in_row.append(king)
                    else:
                        pieces_in_row.append(-king)

            position_matrix.append(pieces_in_row)

        return position_matrix

    def make_move(self, position, move,, turn):
        colums = ["a","b","c","d","e","f","g","h",]

        if move[0] in columns and move[1].isnumeric():
            if turn == white:
                for row in range(0, 8):
                    
            co_ordinates_before =

        #elif move[0] in columns and move[1] == "x":

    def count_material(self):
        pass

    def cluster(self):
        pass

    def learn(self):
        pass


# Function called from Main.py for chess
def engine(legal_moves, fen):

    print(legal_moves)
    position = processor.fen_to_matrix(fen)
    turn = fen.split(" ")[1]

    return legal_moves[0]

processor = Engine()

"""
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
from mpl_toolkits import mplot3d
import matplotlib.patches as mpatches
import pandas as pd
import random

class K_Means:

    def __init__(self, k=3, max_iterations = 500):
        self.k = k
        self.max_iterations = max_iterations

    def euclidean_distance(self, point1, point2):
        #return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)   #sqrt((x1-x2)^2 + (y1-y2)^2)
        return np.linalg.norm(point1-point2, axis=0)

    def fit(self, data):

        #let the first K points from the dataset be the initial centroids
        self.centroids = {}
        for i in range(self.k):
            self.centroids[i] = data[i]

        print(self.centroids)
        #start K-Mean clustering
        for i in range(self.max_iterations):
            #create classifications the size of K
            self.classes = {}
            for j in range(self.k):
                self.classes[j] = []#empty them

            #find the distance between the points and the centroids
            for point in data:
                distances = []
                for index in self.centroids:
                    distances.append(self.euclidean_distance(point,self.centroids[index]))

                #find which cluster the datapoint belongs to by finding the minimum
                #ex: if distances are 2.03,1.04,5.6,1.05 then point belongs to cluster 1 (zero index)
                cluster_index = distances.index(min(distances))
                self.classes[cluster_index].append(point)

            #now that we have classified the datapoints into clusters, we need to again
            #find new centroid by taking the centroid of the points in the cluster class
            for cluster_index in self.classes:
                self.centroids[cluster_index] = np.average(self.classes[cluster_index], axis = 0)


def main():

    #generate dummy cluster datasets
    K = 2
    points = []
    for i in range(0, 100):
        points.append([random.random(),random.random()])
    X = np.array(points)

    k_means = K_Means(K,max_iterations=1000)
    k_means.fit(X)


    print(k_means.centroids)

    # Plotting starts here

    fig = plt.figure()
    ax0 = fig.add_subplot(projection="3d")

    colors = 10*["r", "g", "c", "b", "k"]

    for centroid in k_means.centroids:
        ax0.plot(k_means.centroids[centroid][0], k_means.centroids[centroid][1], 5, marker = "x")

    for cluster_index in k_means.classes:
        color = colors[cluster_index]
        for features in k_means.classes[cluster_index]:
            ax0.plot(features[0], features[1], 5, color = color, marker = "o")

    plt.show()

if __name__ == "__main__":
    main()
"""
