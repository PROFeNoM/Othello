"""
Filename : Constant.py
Authors : 
Date :
Description :
    Contains information, allowing not to lose time
    computing these varaibles. This file primary goal
    is to increase AI's computing time.
"""

class Constant(object):
    """Constant repository"""

    def __init__(self, SIZE):
        """
        Creates constant relative to a specific board size
        :param SIZE: Board's size 
        """
        self.SIZE = 8 

        # List of column letter
        self.COL = [chr(i) for i in range(ord("A"), ord("A")+SIZE)]

        # List of row numbers
        self.RW = range(1,SIZE+1)

        # Return an int corresponding the position of a given position in the dict of a board
        self.POSITION = {column + str(row) : x+SIZE*y for x, column in enumerate([chr(i) for i in range(ord("A"), ord("A")+SIZE)]) for y, row in enumerate(range(1,SIZE+1))}

        # Return an int corresponding to a given str column
        self.COL_NUM = {c : i for i,c in enumerate([chr(i) for i in range(ord("A"), ord("A")+SIZE)])}

        # Return a str correspong to a given int column
        self.NUM_COL = {i : c for i,c in enumerate([chr(i) for i in range(ord("A"), ord("A")+SIZE)])}

        # List of every direction possible
        self.DIRECTIONS = [(x,y) for x in range(-1,2) for y in range(-1,2) if x or y]

        # Return the ennemy disk
        self.ENNEMY_DISK = {"X" : "O", "O" : "X"}

        # -- AI UTILITY BEGINS --
        # Position of every corner
        #self.CORNER = ["A1", chr(ord("A")+SIZE-1)+"1", "A"+str(SIZE), chr(ord("A")+SIZE-1)+str(SIZE)]

        # Position of X squares
        #self.X_SQUARES = ["B2", chr(ord("A")+SIZE-2)+"2", "B"+str(SIZE-1), chr(ord("A")+SIZE-2)+str(SIZE-1)]

        # Position of C squares
        #self.C_SQUARES = [["A2", "B1"], [chr(ord("A")+SIZE-2)+"1", chr(ord("A")+SIZE-1)+"2"], ["A"+str(SIZE-1), "B"+str(SIZE)], [chr(ord("A")+SIZE-2)+str(SIZE), chr(ord("A")+SIZE-1)+str(SIZE-1)]]
        # -- AI UTILITY ENDS --



if __name__ == "__main__":
    constant = Constant(4)
    print constant.POSITION