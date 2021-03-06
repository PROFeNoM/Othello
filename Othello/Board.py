# coding: utf-8

"""
Filename : Board.py
Noms : 
    CHOURA Alexandre
    LEROUX Juliette
    MORTAGNE-CODERCH Anaelle
    WESCHLER Noé
Description :
    Contient tout ce qui correspond à un plateau de jeu
    d'Othello et son état au cours de la partie.
"""
from Constant import Constant

class Board(object):
    """Othello board information"""

    def __init__(self, SIZE):
        """
        Le plateau de jeu est caractérisé par sa taille.
        :param SIZE: Taille du plateau de jeu (côté).
        """
        self.SIZE = SIZE
        self.c = Constant(SIZE)
        self.board = {"d" : SIZE, "grille": ['.']*(SIZE**2)}
        
    def __str__(self):
        """Affiche l'etat du plateau de jeu."""
        return "    "+ " ".join(self.c.COL) + "\n" +"\n".join([(" "+str(row+1)+"  "+" ".join(self.board["grille"][i:i+self.SIZE])) if row+1<10 else str(row+1)+"  "+" ".join(self.board["grille"][i:i+self.SIZE]) for row, i in enumerate([n*self.SIZE for n in range(self.SIZE)])])

    def spot(self, column, row, board=None):
        """
        Retourne '.', 'O' ou 'X' en fonction de l'information contenant la case du plateau.
        :param column: Colonne de la position de la case.
        :param row: Ligne de la position de la case.
        :param board: Plateau de jeu pour lequel on veut connaître l'information d'une case.
        """
        if board: # AB/Minimax
            return board[self.c.POSITION[column+row]] 
        else:
            return self.board["grille"][self.c.POSITION[column+row]]
    
    def is_on_board(self, column, row):
        """
        Retoune True si l'emplacement est dans le plateau, False sinon.
        :param column: Colonne de la position.
        :param row: Ligne de la position.
        """
        return (0<=column<=self.SIZE-1 and 1<=row<=self.SIZE) 

    def get_score(self, player, board=None):
        """
        Retourne le nombre de disques qu'un joueur a sur le plateau.
        :param player: Joueur dont l'on veut connaître le nombre de disques.
        """
        if board: # AB/Minimax
            return board.count(player.disk)
        else:
            return self.board["grille"].count(player.disk)

    def place(self, column, row, disk, board=None):
        """
        Place/flip un disque ("O" or "X") à une position donnée.
        :param column: Colonne de la position.
        :param row: Ligne de la position.
        :param disk: Disque que l'on souhaite mettre à cette position.
        :param board: Plateau de jeu sur lequel on agit.
        """
        if board: # AB/Minimax
            board[self.c.POSITION[column+row]] = disk
        else:
            self.board["grille"][self.c.POSITION[column+row]] = disk

    def starting_board(self):
        """Place les quatres disques initiaux de jeu d'une partie d'Othello."""
        for pos, disk in zip([self.c.POSITION[key] for key in (self.c.NUM_COL[self.SIZE/2 - 1] + str(self.SIZE/2), self.c.NUM_COL[self.SIZE/2] + str(self.SIZE/2 + 1), self.c.NUM_COL[self.SIZE/2 - 1] + str(self.SIZE/2 + 1), self.c.NUM_COL[self.SIZE/2] + str(self.SIZE/2))], "OOXX"): # Initial 4 positions
            self.board["grille"][pos] = disk

    def empty_squares(self):
        """Détermine le nombre de case vides sur le plateau."""
        return self.board["grille"].count(".")

if __name__ == "__main__":
    print "Test de la fonction d'affichage du plateau Board.__str__() :"

    # Test avec un plateau entièrement vide de taille 12x12
    SIZE = 12
    c = Constant(SIZE)
    board_12 = Board(SIZE)
    empty_board = ["."]*(SIZE**2)
    if board_12.__str__() == "    "+ " ".join(c.COL) + "\n" +"\n".join([(" "+str(row+1)+"  "+" ".join(empty_board[i:i+SIZE])) if row+1<10 else str(row+1)+"  "+" ".join(empty_board[i:i+SIZE]) for row, i in enumerate([n*SIZE for n in range(SIZE)])]):
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_12.__str__() = \n{} \nResultat attendu = \n{}".format(board_12, "    "+ " ".join(c.COL) + "\n" +"\n".join([(" "+str(row+1)+"  "+" ".join(empty_board[i:i+SIZE])) if row+1<10 else str(row+1)+"  "+" ".join(empty_board[i:i+SIZE]) for row, i in enumerate([n*SIZE for n in range(SIZE)])]))
    print " ---> test {}".format(test)

    # Test avec un plateau plein 2x2 (positions initiales)
    SIZE = 2
    c = Constant(SIZE)
    board_2 = Board(SIZE)
    board_2.board["grille"] = ["O", "X", "X", "O"]
    filled_board = ["O", "X", "X", "O"]
    if board_2.__str__() == "    "+ " ".join(c.COL) + "\n" +"\n".join([(" "+str(row+1)+"  "+" ".join(filled_board[i:i+SIZE])) if row+1<10 else str(row+1)+"  "+" ".join(filled_board[i:i+SIZE]) for row, i in enumerate([n*SIZE for n in range(SIZE)])]):
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_2.__str__() = \n{} \nResultat attendu = \n{}".format(board_2, "    "+ " ".join(c.COL) + "\n" +"\n".join([(" "+str(row+1)+"  "+" ".join(filled_board[i:i+SIZE])) if row+1<10 else str(row+1)+"  "+" ".join(filled_board[i:i+SIZE]) for row, i in enumerate([n*SIZE for n in range(SIZE)])]))
    print " ---> test {}".format(test)
    
    
    # Test avec un plateau aléatoire 8x8
    SIZE = 8
    c = Constant(SIZE)
    board_8 = Board(SIZE)
    board_8.board["grille"] = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'X']
    board_state = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'X']
    if board_8.__str__() == "    "+ " ".join(c.COL) + "\n" +"\n".join([(" "+str(row+1)+"  "+" ".join(board_state[i:i+SIZE])) if row+1<10 else str(row+1)+"  "+" ".join(board_state[i:i+SIZE]) for row, i in enumerate([n*SIZE for n in range(SIZE)])]):
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_8.__str__() = \n{} \nResultat attendu = \n{}".format(board_8, "    "+ " ".join(c.COL) + "\n" +"\n".join([(" "+str(row+1)+"  "+" ".join(board_state[i:i+SIZE])) if row+1<10 else str(row+1)+"  "+" ".join(board_state[i:i+SIZE]) for row, i in enumerate([n*SIZE for n in range(SIZE)])]))
    print " ---> test {}".format(test)
    
    print "\n-----------------------------------------"

    print "\nTest de Board.spot() :"

    # Test avec le plateau entièrement vide de taille 12x12 à la position A1
    res = board_12.spot("A", "1", board_12.board["grille"])
    if res == ".":
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_12.spot({},{}) = {} ; Resultat attendu = {}".format("A", "1", res, ".")
    print " ---> test {}".format(test)

    # Test avec le plateau plein 2x2 (positions initiales) à la positon B2
    res = board_2.spot("B", "2", board_2.board["grille"])
    if res == "O":
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_2.spot({},{}) = {} ; Resultat attendu = {}".format("B", "2", res, "O")
    print " ---> test {}".format(test)

    # Test avec le plateau aléatoire 8x8 à la position D4
    res = board_8.spot("D", "4", board_8.board["grille"])
    if res == "O":
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_8.spot({},{}) = {} ; Resultat attendu = {}".format("D", "4", res, "O")
    print " ---> test {}".format(test)

    # Test avec le plateau aléatoire 8x8 à la position H8
    res = board_8.spot("H", "8", board_8.board["grille"])
    if res == "X":
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_8.spot({},{}) = {} ; Resultat attendu = {}".format("H", "8", res, "X")
    print " ---> test {}".format(test)

    print "\n-----------------------------------------"

    print "\nTest de Board.is_on_board() :"
    
    # Test avec le plateau entièrement vide de taille 12x12 à la position A1
    res = board_12.is_on_board(0, 1)
    if res is True:
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_12.is_on_board({},{}) = {} ; Resultat attendu = {}".format(0, 1, res, True)
    print " ---> test {}".format(test)

    # Test avec le plateau entièrement vide de taille 12x12 à la position B14
    res = board_12.is_on_board(1, 14)
    if res is False:
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_12.is_on_board({},{}) = {} ; Resultat attendu = {}".format(1, 14, res, False)
    print " ---> test {}".format(test)

    # Test avec le plateau plein 2x2 (positions initiales) à la positon B2
    res = board_2.is_on_board(1, 2)
    if res is True:
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_2.is_on_board({},{}) = {} ; Resultat attendu = {}".format(1, 2, res, True)
    print " ---> test {}".format(test)

    print "\n-----------------------------------------"

    print "\nTest de Board.get_score() :"
    from HumanPlayer import HumanPlayer
    player_X = HumanPlayer("X", "X")
    player_O = HumanPlayer("O", "O")

    # Test avec le plateau entièrement vide de taille 12x12 pour X
    res = board_12.get_score(player_X, board_12.board["grille"])
    if res == 0:
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_12.get_score({}) = {} ; Resultat attendu = {}".format(player_X, res, 0)
    print " ---> test {}".format(test)

    # Test avec le plateau plein 2x2 (positions initiales) pour O
    res = board_2.get_score(player_O, board_2.board["grille"])
    if res == 2:
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_2.get_score({}) = {} ; Resultat attendu = {}".format(player_X, res, 2)
    print " ---> test {}".format(test)

    # Test avec le plateau aléatoire 8x8 pour X
    res = board_8.get_score(player_X, board_8.board["grille"])
    if res == 16:
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_8.get_score({}) = {} ; Resultat attendu = {}".format(player_X, res, 16)
    print " ---> test {}".format(test)

    # Test avec le plateau aléatoire 8x8 pour O
    res = board_8.get_score(player_O, board_8.board["grille"])
    if res == 15:
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_8.get_score({}) = {} ; Resultat attendu = {}".format(player_O, res, 15)
    print " ---> test {}".format(test)

    print "\n-----------------------------------------"

    print "\nTest de Board.place() :"

    # Test avec le plateau entièrement vide de taille 12x12 à la position A1 pour X
    expected = ["X"] + ["."]*143
    board_12.place("A", "1", player_X.disk, board_12.board["grille"])
    if board_12.board["grille"] == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_12.place({},{},{}) => {} \nResultat attendu = {}".format("A","1",player_X.disk, board_12.board["grille"], expected)
    print " ---> test {}".format(test)

    # Test avec le plateau aléatoire 8x8 à la position G8 pour O
    expected = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'O', 'X']
    board_8.place("G","8",player_O.disk, board_8.board["grille"])
    if board_8.board["grille"] == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_8.place({},{},{}) => {} \nResultat attendu = {}".format("G","8",player_O.disk, board_8.board["grille"], expected)
    print " ---> test {}".format(test)

    # Test avec le plateau plein 2x2 à la position A1 pour O
    expected = ["O", "X", "X", "O"]
    board_2.place("A", "1", player_O.disk, board_2.board["grille"])
    if board_2.board["grille"] == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_2.place({},{},{}) => {} \nResultat attendu = {}".format("A","1",player_O.disk, board_2.board["grille"], expected)
    print " ---> test {}".format(test)

    print "\n-----------------------------------------"

    print "\nTest de Board.starting_board() :"

    # Test avec un plateau 6x6
    board_6 = Board(6)
    board_6.starting_board()
    expected = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'O', 'X', '.', '.', '.', '.', 'X', 'O', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
    if board_6.board["grille"] == expected:
        test = "OK"
    else:
        test = "NOK"
    print "board_6.starting_board() ==> {} \nResultat attendu = {}".format(board_6.board["grille"], expected)
    print " ---> test {}".format(test)

    # Test avec un plateau 26x26
    board_26 = Board(26)
    board_26.starting_board()
    expected = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'O', 'X', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'X', 'O', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
    if board_26.board["grille"] == expected:
        test = "OK"
    else:
        test = "NOK"
    print "board_26.starting_board() ==> {} \nResultat attendu = {}".format(board_26.board["grille"], expected)
    print " ---> test {}".format(test)

    print "\n-----------------------------------------"

    print "\nTest de Board.empty_squares() :"

    # Test pour le plateau 26x26
    res = board_26.empty_squares()
    if res == 672: #26*26-4
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_26.empty_squares() = {} ; Resultat attendu = {}".format(res, 672)
    print " ---> test {}".format(test)

    # Test pour le plateau 2x2 plein
    res = board_2.empty_squares()
    if res == 0:
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_2.empty_squares() = {} ; Resultat attendu = {}".format(res, 0)
    print " ---> test {}".format(test)

    # Test pour le plateau 8x8 non fini (Ne pas oublier que l'on a ajouter une pièce précédement par rapport au plateau affiché)
    res = board_8.empty_squares()
    if res == 32:
        test = "OK"
    else:
        test = "NOK"
    print "\nboard_8.empty_squares() = {} ; Resultat attendu = {}".format(res, 32)
    print " ---> test {}".format(test)

    try:
        input("\n\n<Appuyez sur Enter pour quitter.>")
    except:
        pass