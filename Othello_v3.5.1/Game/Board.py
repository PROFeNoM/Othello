"""
Filename : Board.py
Authors : 
Date :
Description :
"""
from Constant import SIZE, POSITION

class Board(object):
    """Othello board information"""

    def __init__(self):
        self.board = {"d" : SIZE, "grille": ['.']*(SIZE**2)}

    def __str__(self):
        """Affiche l'etat du plateau de jeu"""
        return "~~~~ Plateau de Jeu ~~~~\n" + "    "+ " ".join([chr(i) for i in range(ord('A'), ord("A")+27)][:SIZE]) + "\n" +"\n".join([(" "+str(row+1)+"  "+" ".join(self.board["grille"][i:i+SIZE])) if row+1<10 else str(row+1)+"  "+" ".join(self.board["grille"][i:i+SIZE]) for row, i in enumerate([n*SIZE for n in range(SIZE)])]) + "\n~~~~~~~~~~~~~~~~~~~~~~~~"

    def spot(self, column, row, board):
        """
        Return '.', 'O' ou 'X' according to square's disk
        :param column: Column of the position
        :param row: Row of the position
        :param board: Board we want to get position's disk
        """
        return board[POSITION[column+row]] 
    
    def is_on_board(self, column, row):
        """Retoune True si l'emplacement est le plateau, False sinon"""
        return (0<=column<=SIZE-1 and 1<=row<=SIZE) 

    def get_score(self, board):
        pass
    @staticmethod
    def place(column, row, disk, board):
        """
        Place/flip a disk ("O" or "X") at the given position
        :param column: Column of the position
        :param row: Row of the position
        :param disk: Disk to put at the position
        :param board: Board we are dealing with
        """
        board[POSITION[column+row]] = disk

if __name__ == "__main__":
    board = Board()
    print board.board