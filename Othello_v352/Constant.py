# coding: utf-8

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
    print "\t\tTest de la classe Constant()"

    print "\n\tPour un plateau 2x2 :"
    constant_2 = Constant(2)
    
    # Test de POSITION
    expected = {"A1" : 0, "B1" : 1, "A2" : 2, "B2" : 3}
    res = constant_2.POSITION
    if res == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nconstant_2.POSITION = {} ; Resultat attendu = {}".format(res, expected)
    print " ---> test {}".format(test)

    # Test de COL_NUM
    expected = {'A': 0, 'B': 1}
    res = constant_2.COL_NUM
    if res == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nconstant_2.COL_NUM = {} ; Resultat attendu = {}".format(res, expected)
    print " ---> test {}".format(test)

    # Test de NUM_COL
    expected = {0: 'A', 1: 'B'}
    res = constant_2.NUM_COL
    if res == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nconstant_2.NUM_COL = {} ; Resultat attendu = {}".format(res, expected)
    print " ---> test {}".format(test)

    # Test de DIRECTIONS (commun quelque soit la taille choisi)
    expected = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    res = constant_2.DIRECTIONS
    if set(res) == set(expected):
        test = "OK"
    else:
        test = "NOK"
    print "\nconstant_2.DIRECTIONS = {} ; Resultat attendu = {}".format(res, expected)
    print " ---> test {}".format(test)

    print "\n\tPour un plateau 8x8 :"
    constant_8 = Constant(8)

    # Test de POSITION
    expected = {"A1" : 0, "B1" : 1, "C1" : 2, "D1" : 3, "E1" : 4, "F1" : 5, "G1" : 6, "H1" : 7, "A2" : 8, "B2" : 9, "C2" : 10, "D2" : 11, "E2" : 12, "F2" : 13, "G2" : 14, "H2" : 15, "A3" : 16, "B3" : 17, "C3" : 18, "D3" : 19, "E3" : 20, "F3" : 21, "G3" : 22, "H3" : 23, "A4" : 24, "B4" : 25, "C4" : 26, "D4" : 27, "E4" : 28, "F4" : 29, "G4" : 30, "H4" : 31, "A5" : 32, "B5" : 33, "C5" : 34, "D5" : 35, "E5" : 36, "F5" : 37, "G5" : 38, "H5" : 39, "A6" : 40, "B6" : 41, "C6" : 42, "D6" : 43, "E6" : 44, "F6" : 45, "G6" : 46, "H6" : 47, "A7" : 48, "B7" : 49, "C7" : 50, "D7" : 51, "E7" : 52, "F7" : 53, "G7" : 54, "H7" : 55, "A8" : 56, "B8" : 57, "C8" : 58, "D8" : 59, "E8" : 60, "F8" : 61, "G8" : 62, "H8" : 63}
    res = constant_8.POSITION
    if res == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nconstant_8.POSITION = {} \nResultat attendu = {}".format(res, expected)
    print " ---> test {}".format(test)

    # Test de COL
    expected = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    res = constant_8.COL
    if res == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nconstant_8.COL = {} \nResultat attendu = {}".format(res, expected)
    print " ---> test {}".format(test)

    # Test de COL_NUM
    expected = {'A': 0, 'B' : 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    res = constant_8.COL_NUM
    if res == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nconstant_8.COL_NUM = {} \nResultat attendu = {}".format(res, expected)
    print " ---> test {}".format(test)

    # Test de NUM_COL
    expected = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
    res = constant_8.NUM_COL
    if res == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nconstant_8.NUM_COL = {} \nResultat attendu = {}".format(res, expected)
    print " ---> test {}".format(test)