# coding: utf-8

"""
Filename : HumanPlayer.py
Authors : 
Date :
Description :
    This is simply a human player and 
    its caracteristics.
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

if __name__ == "__main__":

    print "Test de HumanPlayer.__str__() :"
    player_X = HumanPlayer("X", "Marshall Bruce Mathers III")
    player_O = HumanPlayer("O", "Lesane Parish Crooks")

    # Pour le nom de X
    res = player_X.__str__()
    if res == "Marshall Bruce Mathers III":
        test = "OK"
    else:
        test = "NOK"
    print "\nplayer_X.__str__() = {} ; Resultat attendu = {}".format(player_X, "Marshall Bruce Mathers III")
    print " ---> test {}".format(test)

    # Pour le nom de O
    res = player_O.__str__()
    if res == "Lesane Parish Crooks":
        test = "OK"
    else:
        test = "NOK"
    print "\nplayer_X.__str__() = {} ; Resultat attendu = {}".format(player_O, "Lesane Parish Crooks")
    print " ---> test {}".format(test)

    try:
        input("\n\n<Appuyez sur Enter pour quitter.>")
    except:
        pass