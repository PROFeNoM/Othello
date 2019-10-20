"""
Filename : Board.py
Authors : 
Date :
Description :
    Contains everything relative to an
    Othello board and its state.
"""
from Constant import Constant

class Board(object):
    """Othello board information"""

    def __init__(self, SIZE):
        """
        The board is caracterized by his size
        :param SIZE: Board's size"""
        self.SIZE = SIZE
        self.c = Constant(SIZE)
        self.board = {"d" : SIZE, "grille": ['.']*(SIZE**2)}
        
    def __str__(self):
        """Affiche l'etat du plateau de jeu"""
        return "~~~~ Plateau de Jeu ~~~~\n\n" + "    "+ " ".join(self.c.COL) + "\n" +"\n".join([(" "+str(row+1)+"  "+" ".join(self.board["grille"][i:i+self.SIZE])) if row+1<10 else str(row+1)+"  "+" ".join(self.board["grille"][i:i+self.SIZE]) for row, i in enumerate([n*self.SIZE for n in range(self.SIZE)])])

    def spot(self, column, row):
        """
        Return '.', 'O' ou 'X' according to square's disk
        :param column: Column of the position
        :param row: Row of the position
        :param board: Board we want to get position's disk
        """
        return self.board["grille"][self.c.POSITION[column+row]] 
    
    def is_on_board(self, column, row):
        """
        Retoune True si l'emplacement est le plateau, False sinon
        :param column: Column of the position
        :param row: Row of the position
        """
        return (0<=column<=self.SIZE-1 and 1<=row<=self.SIZE) 

    def get_score(self, player):
        """
        Return the number of disk(s) a player has
        :param player: Player we want to know the number of disk(s)
        """
        return self.board["grille"].count(player.disk)

    def place(self, column, row, disk):
        """
        Place/flip a disk ("O" or "X") at the given position
        :param column: Column of the position
        :param row: Row of the position
        :param disk: Disk to put at the position
        :param board: Board we are dealing with
        """
        self.board["grille"][self.c.POSITION[column+row]] = disk

    def starting_board(self):
        print "\nFormat du plateau choisit: {}x{}".format(self.SIZE, self.SIZE)
        for pos, disk in zip([self.c.POSITION[key] for key in (self.c.NUM_COL[self.SIZE/2 - 1] + str(self.SIZE/2), self.c.NUM_COL[self.SIZE/2] + str(self.SIZE/2 + 1), self.c.NUM_COL[self.SIZE/2 - 1] + str(self.SIZE/2 + 1), self.c.NUM_COL[self.SIZE/2] + str(self.SIZE/2))], "OOXX"): # Initial 4 positions
            self.board["grille"][pos] = disk

    def empty_squares(self):
        return self.board["grille"].count(".")

if __name__ == "__main__":
    pass