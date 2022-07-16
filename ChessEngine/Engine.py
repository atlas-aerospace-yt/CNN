#
#   16/07/2022
#
#   Chess Engine using K-means clustering algorithm
#   SQL Database to save positions to analyse
#   Unsupervised learning
#
#   ## TODO: make all class and function names camelCase
#   ## TODO: create the data base features to be used by the engine
#   ## TODO: fix the database insert function: currently throws error
#
#   Written by:
#   Alexander Armitage
#

from Data import ChessDatabase
import random

# Chess engine class
class Engine():

    # Initialises classes variables
    def __init__(self):
        self.columns = ["a","b","c","d","e","f","g","h",]

    # Returns list of pieces in the shape of a board
    def fen_to_matrix(self, fen):
        position = fen.split(" ")[0].split("/")

        pawn = 0.1
        knight = 0.3
        bishop = 0.35
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

    # Updates position matrix if move is a pawn push
    def pawn_push(self, position, move, turn):
        row = 0
        current_before_row = 0
        if turn == "w":
            pawn_value = 0.1
            if "=" in move:
                promotion = move.split("=")[1]
                if promotion == "Q":
                    pawn_value = 0.9
                elif promotion == "R":
                    pawn_value = 0.5
                elif promotion == "B":
                    pawn_value = 0.35
                else:
                    pawn_value = 0.3
            for row in range(0, 8):
                if position[row][self.columns.index(move[0])] == 0.1 and row > current_before_row:
                    current_before_row = row
        else:
            pawn_value = -0.1
            if "=" in move:
                promotion = move.split("=")[1]
                if promotion == "Q":
                    pawn_value = -0.9
                elif promotion == "R":
                    pawn_value = -0.5
                elif promotion == "B":
                    pawn_value = -0.35
                else:
                    pawn_value = -0.3
            for row in range(0, 8):
                if position[row][self.columns.index(move[0])] == -0.1 and row > current_before_row:
                    current_before_row = row

        co_ordinates_before = [self.columns.index(move[0]), current_before_row]
        co_ordinates_after = [self.columns.index(move[0]), 8 - int(move[1])]

        position[co_ordinates_before[1]][co_ordinates_before[0]] = 0
        position[co_ordinates_after[1]][co_ordinates_after[0]] = pawn_value

        return position

    # Updates position if move is a pawn taking a piece
    def pawn_take(self, position, move, turn):
        row = 0
        current_before_row = 0
        if turn == "w":
            pawn_value = 0.1
            if "=" in move:
                promotion = move.split("=")[1]
                if promotion == "Q":
                    pawn_value = 0.9
                elif promotion == "R":
                    pawn_value = 0.5
                elif promotion == "B":
                    pawn_value = 0.35
                else:
                    pawn_value = 0.3
            for row in range(0, 8):
                if position[row][self.columns.index(move[0])] == 0.1 and row > current_before_row:
                    current_before_row = row

        else:
            pawn_value = -0.1
            if "=" in move:
                promotion = move.split("=")[1]
                if promotion == "Q":
                    pawn_value = -0.9
                elif promotion == "R":
                    pawn_value = -0.5
                elif promotion == "B":
                    pawn_value = -0.35
                else:
                    pawn_value = -0.3
            for row in range(0, 8):
                if position[row][self.columns.index(move[0])] == -0.1 and row > current_before_row:
                    current_before_row = row

        co_ordinates_before = [self.columns.index(move[0]), current_before_row]
        co_ordinates_after = [self.columns.index(move[2]), 8 - int(move[3])]

        position[co_ordinates_before[1]][co_ordinates_before[0]] = 0
        position[co_ordinates_after[1]][co_ordinates_after[0]] = pawn_value

        return position

    # Updates position if move is just a normal piece
    def piece_move(self, position, move, turn):
        if turn == "w":
            piece = move[0]
            if piece == "K":
                piece_value = 1
            elif piece == "Q":
                piece_value = 0.9
            elif piece == "R":
                piece_value = 0.5
            elif piece == "B":
                piece_value = 0.35
            else:
                piece_value = 0.3
            co_ordinates_before = [self.columns.index(move[1]), 8 - int(move[2])]
            if "x" not in move:
                co_ordinates_after = [self.columns.index(move[3]), 8 - int(move[4])]
            else:
                co_ordinates_after = [self.columns.index(move[4]), 8 - int(move[5])]

        else:
            piece = move[0]
            if piece == "K":
                piece_value = -1
            elif piece == "Q":
                piece_value = -0.9
            elif piece == "R":
                piece_value = -0.5
            elif piece == "B":
                piece_value = -0.35
            else:
                piece_value = -0.3
            co_ordinates_before = [self.columns.index(move[1]), 8 - int(move[2])]
            if "x" not in move:
                co_ordinates_after = [self.columns.index(move[3]), 8 - int(move[4])]
            else:
                co_ordinates_after = [self.columns.index(move[4]), 8 - int(move[5])]

        position[co_ordinates_before[1]][co_ordinates_before[0]] = 0
        position[co_ordinates_after[1]][co_ordinates_after[0]] = piece_value

        return position

    # Checks which type of move the move is and then calls the function accordingly
    # Also updates position for castling
    def make_move(self, position, move, turn):

        if move[0] in self.columns and move[1].isnumeric():
            return self.pawn_push(position, move, turn)

        elif move[0] in self.columns and move[1] == "x":
            return self.pawn_take(position, move, turn)

        elif move[1] in self.columns and move[2].isnumeric():
            return self.piece_move(position, move, turn)

        elif move == "O-O":
            if turn == "w":
                position[7][0] = 0
                position[7][3] = 0
                position[7][2] = 0.5
                position[7][1] = 1
            else:
                position[0][0] = 0
                position[0][3] = 0
                position[0][2] = 0.5
                position[0][1] = 1
            return position

        elif move == "O-O-O":
            if turn == "w":
                position[7][7] = 0
                position[7][3] = 0
                position[7][4] = 0.5
                position[7][5] = 1
            else:
                position[0][7] = 0
                position[0][3] = 0
                position[0][4] = 0.5
                position[0][5] = 1
            return position
        else:
            print(f'Move not recognised: {move}')
            return 0

    # Counts total count_material
    # Positive material means white is winning
    # Negative material means black is winning
    def count_material(self, position):
        material = 0
        for rank in range(0, 8):
            for file in range(0, 8):
                material += position[rank][file]
        return material

    def cluster(self):
        pass

    def learn(self):
        pass


    def evaluate(self, legal_moves, fen):

        position = self.fen_to_matrix(fen)
        turn = fen.split(" ")[1]

        if "O-O" in legal_moves:
            move = "O-O"
        else:
            move = legal_moves[random.randint(0, len(legal_moves)-1)]

        position = self.make_move(position, move, turn)

        #print(move, *position, sep="\n")
        print(round(self.count_material(position), 2))

        data.Insert(fen, move)

        return move

# Function called from Main.py for chess
def engine(legal_moves, fen):
    return processor.evaluate(legal_moves, fen)

# Initialises the Engine class
processor = Engine()
data = ChessDatabase()

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
