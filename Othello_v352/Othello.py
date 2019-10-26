# coding: utf-8
 
"""
Filename : Othello.py
Authors : 
Date :
Description :
    Run this file to play Othello.
"""

from GameEngine import GameEngine
from HumanPlayer import HumanPlayer
from RandomPlayer import RandomPlayer

def ask_number(question, low, high):
    """
    Ask for a number within a range.
    :param question: Sentence to display to the player
    :param low: lowest legal value
    :param high: highest legal value
    """
    res = None
    while res not in range(low,high+1):
        try:
            res = int(input(question))
            if res not in range(low, high+1):
                print "Entrez une valeur entre {} et {}".format(low, high)
        except:
            print "Entrez une reponse correcte."
    return res

def winner(player_X, player_O, score_pX, score_pO, empty, size):
    """
    Determine and display both the winner and loser of the game
    :param player_X: Player who's playing with X disks
    :param player_O: Player who's playing with O disks
    :param score_pX: Score of the player with X disks
    :param score_pO: Score of the player with O disks
    :param empty: Number of empty squares left on the board
    :param size: Board's size
    """
    if empty:
        if score_pX > score_pO:
            score_pX += empty
        elif score_pO > score_pX:
            score_pO += empty
    if score_pX > score_pO:
        print "\n{} gagne avec {} points, contre {} pour {} !".format(player_X.name, score_pX, score_pO, player_O.name)
    elif score_pX < score_pO:
        print "\n{} gagne avec {} points, contre {} pour {} !".format(player_O.name, score_pO, score_pX, player_X.name)
    else:
        print "\nEGALITE! Les deux joueurs ont {} points!".format(size**2/2)

def main():
    """An Othello Game"""
    print "\t\t\t\t\tBienvenue sur Othello!"
    user_choice_size = ask_number("""
                             Combien de lignes (ou colonnes) doit avoir le plateau ?
                             --> """, low = 2, high = 26)
    while user_choice_size % 2 != 0:
        print "Entrez un nombre pair"
        user_choice_size = ask_number("""
                             Combien de lignes (ou colonnes) doit avoir le plateau ?
                             --> """, low = 2, high = 26)

    user_choice_gm = ask_number("""
                             Choissisez un mode de jeu (1 ou 2):
                             1.- Contre l'ordinateur
                             2.- 2 joueurs

                             --> """, low=1, high=2)
    if user_choice_gm == 1:
        name = raw_input("Entrez le nom du joueur: ")
        user_choice_c = ask_number("""
                                 Quelle couleur voulez-vous jouer (1 ou 2):
                                 1.- Noir
                                 2.- Blanc
                                 
                                 --> """, low=1, high=2)
        if user_choice_c == 1:
            player_X = HumanPlayer("X", name)
            player_O = RandomPlayer("O")
        else:
            player_O = HumanPlayer("O", name)
            player_X = RandomPlayer("X")
    else:
        names = list()
        for i in range(user_choice_gm):
            names.append(raw_input("Entrez le nom du joueur {} ({disk}): ".format(i+1, disk="X" if i==0 else "O")))
        player_X = HumanPlayer("X", names[0])
        player_O = HumanPlayer("O", names[1])
    print "\nPour jouer une position, saisissez les coordonnees sous la forme ColonneLigne (A4, B6, ...)"
    print "\nFormat du plateau choisit: {}x{}".format(user_choice_size, user_choice_size)
    game, over = GameEngine(player_X, player_O, user_choice_size), False
    while not over:
        over = game.game_loop()
    winner(player_X, player_O, over[0], over[1], over[2], user_choice_size)

main()

try:
    input("\n\n<Appuyez sur Enter pour quitter.>")
except:
    pass