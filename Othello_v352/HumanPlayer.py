"""
Filename : HumanPlayer.py
Authors : 
Date :
Description :
"""

class HumanPlayer(object):
    """An Othello Player"""

    def __init__(self, disk, name):
        """
        Initialize player's disk and name
        :param disk: either "X" or "O"
        :param name: player's name (str)
        """
        self.disk = disk
        self.name = name

    def __str__(self):
        """Return player's name"""
        return self.name