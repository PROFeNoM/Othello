# coding: utf-8

"""
Filename : RandomPlayer.py
Noms : 
    CHOURA Alexandre
    LEROUX Juliette
    MORTAGNE-CODERCH Anaelle
    WESCHLER Noé
Description :
    Ce fichier permet de définir un joueur qui joue tout seul.
    L'ordinateur choisira aléatoirement une position
    parmi tous les coups valides possibles.
"""
from random import choice

class RandomPlayer(object):
    """A Random AI."""

    def __init__(self, disk, name="L'ordinateur"):
        """
        Initialize le nom du joueur et son disque.
        :param disk: Soit "X" ou "O".
        :param name: Nom du joueur (str).
        """
        self.disk = disk
        self.name = name

    def get_move(self, moves):
        """
        Retourne une position légale aléatoire à jouer par l'ordinateur.
        :param moves: Liste des coups légaux possible pour le joueur.
        Nota Bene : le paramètre moves ne sera jamais la liste vide.
        """
        return choice(moves)

if __name__ =="__main__":
    player = RandomPlayer("X")

    print "Test de RandomPlayer.get_move() :"
    # Pour info, le paramètre moves ne sera jamais [] en raison d'une condition en amont
    # à la ligne 115 de GameEngine.py

    # Test à partir d'un plateau 8x8 initial
    from GamePlayer import PlayerEngine
    from Board import Board
    board_4 = Board(4)
    board_4.starting_board()
    engine_4 = PlayerEngine(board_4, 4)
    legal_move = engine_4.get_moves(player)
    res = player.get_move(legal_move)
    if res in legal_move:
        test = "OK"
    else:
        test = "NOK"
    print "player.get_move({}) = {} ; Resultat attendu doit etre dans {}".format(legal_move, res, legal_move)
    print " ---> test {}".format(test)

    # Test à partir d'un plateau 6x6
    board_4 = Board(4)
    board_4.board["grille"] = ["X","O","O","X","O","O","O","X","X","X","O","O","X","X","O","."]
    engine_4 = PlayerEngine(board_4, 4)
    legal_move = engine_4.get_moves(player)
    res = player.get_move(legal_move)
    if res == "D4":
        test = "OK"
    else:
        test = "NOK"
    print "\nplayer.get_move({}) = {} ; Resultat attendu doit etre {}".format(legal_move, res, "D4")
    print " ---> test {}".format(test)

    try:
        input("\n\n<Appuyez sur Enter pour quitter.>")
    except:
        pass