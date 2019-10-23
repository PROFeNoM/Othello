"""
Filename : RandomPlayer.py
Authors : 
Date :
Description :
    Contains an AI returning a random
    position. This type of file is more
    usefull for more complex AI as AlphaBeta.
"""
from random import shuffle

class RandomPlayer(object):
    """A Random AI"""

    def __init__(self, disk, name="L'ordinateur"):
        """
        Initialize player's disk and name
        :param disk: either "X" or "O"
        :param name: player's name (str)
        """
        self.disk = disk
        self.name = name

    def get_move(self, moves):
        """
        Return a random valid position to play
        :param moves: List of every legal moves
        """
        shuffle(moves)
        return moves[0]

if __name__ =="__main__":
    RandomPlayer = RandomPlayer("X")
    if RandomPlayer.disk == "X":
        print "--> Test ok"
