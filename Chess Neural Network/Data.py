import sqlite3

# Database class for chess engine to analyse
# The database is not encrypted as the data is not sensitve
class ChessDatabase():

    # Creates the table if it doesnt already exist
    def __init__(self):
        connection = sqlite3.connect('Data/ChessPositions.db')
        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS Positions(
                          FEN,
                          move
                          )''')

        connection.commit()
        connection.close()

    # Called by Engine.py to add data to database
    def Insert(self, FEN, move):
        connection = sqlite3.connect('Data/ChessPositions.db')
        cursor = connection.cursor()

        cursor.execute(f'INSERT INTO Positions VALUES ({FEN},{move})')

        connection.commit()
        connection.close()

    # Called by Engine.py to read all values in the database
    def ReturnAll(self):

        #cursor = connection.cursor()

        #cursor.execute(f'INSERT INTO Positions VALUES ({FEN},{move})')

        #connection.commit()
        #connection.close()

        pass
