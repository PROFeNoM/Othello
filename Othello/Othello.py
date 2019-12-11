# coding: utf-8
 
"""
Filename : Othello.py
Noms : 
    CHOURA Alexandre
    LEROUX Juliette
    MORTAGNE-CODERCH Anaelle
    WESCHLER Noé
Description :
    Exécuter ce fichier pour lancer une partie d'Othello.
    Ce fichier permet de lancer une partie correspondant
    aux choix du/des joueur(s).
"""

from GameEngine import GameEngine
from HumanPlayer import HumanPlayer
from RandomPlayer import RandomPlayer
from AlphaBetaPlayer import AlphaBetaPlayer
from MaximumPlayer import MaximumPlayer
from MinimaxPlayer import MinimaxPlayer

def ask_number(question, low, high):
    """
    Demande un nombre entier compris entre deux autres.
    :param question: Phrase à afficher au joueur.
    :param low: Valeur légale la plus faible.
    :param high: Valeur légale la plus haute.
    """
    res = None
    while res not in range(low,high+1):
        try:
            res = input(question)
            if res not in range(low, high+1) or type(res) is not int:
                print "Entrez une valeur entiere entre {} et {}".format(low, high)
        except:
            print "Entrez une reponse correcte."
    return res

def winner(player_X, player_O, score_pX, score_pO, empty, size):
    """
    Détermine et affiche le gagnant et perdant de la partie.
    :param player_X: Joueur jouant les disques X.
    :param player_O: Joueur jouant les disque O.
    :param score_pX: Score du joueur jouant les disques X.
    :param score_pO: Score du joueur jouant les disques O.
    :param empty: Nombre de cases vides sur le plateau de jeu.
    :param size: Taille d'un côté du plateau de jeu.
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
    """Une partie d'Othello."""
    print "\t\t\t\t\tBienvenue sur Othello!"
    user_choice_size = ask_number("""
                             Combien de lignes (ou colonnes) doit avoir le plateau ? (entre 2 et 26)
                             --> """, low = 2, high = 26)
    while user_choice_size % 2 != 0:
        print "Entrez un nombre pair"
        user_choice_size = ask_number("""
                             Combien de lignes (ou colonnes) doit avoir le plateau ?
                             --> """, low = 2, high = 26)

    user_choice_gm = ask_number("""
                             Choissisez un mode de jeu (1,2 ou 3):
                             1.- Contre l'ordinateur
                             2.- 2 joueurs
                             3.- IA Maximum vs IA Minimax
                             --> """, low=1, high=3)
    if user_choice_gm == 1:
        name = raw_input("Entrez le nom du joueur: ")
        user_choice_c = ask_number("""
                            Quelle couleur voulez-vous jouer (1 ou 2):
                             1.- Noir
                             2.- Blanc
                                 
                             --> """, low=1, high=2)
        user_choice_AI = ask_number("""
                             Contre quelle AI souhaitez-vous jouer?:
                             1.- Random
                             2.- Maximum
                             3.- Minimax
                             4.- AlphaBeta Pruning

                             ---> """, low=1, high=4)
        if user_choice_c == 1:
            player_X = HumanPlayer("X", name)
            if user_choice_AI == 1:
                player_O = RandomPlayer("O")
            elif user_choice_AI == 2:
                player_O = MaximumPlayer("O", "L'ordinateur", user_choice_size)
            elif user_choice_AI == 3:
                player_O = MinimaxPlayer("O", "L'ordinateur", user_choice_size)
            else:
                player_O = AlphaBetaPlayer("O", "L'ordinateur", user_choice_size)
        else:
            player_O = HumanPlayer("O", name)
            if user_choice_AI == 1:
                player_X = RandomPlayer("X")
            elif user_choice_AI == 2:
                player_X = MaximumPlayer("X", "L'ordinateur", user_choice_size)
            elif user_choice_AI == 3:
                player_X = MinimaxPlayer("X", "L'ordinateur", user_choice_size)
            else:
                player_X = AlphaBetaPlayer("X", "L'ordinateur", user_choice_size)
    if user_choice_gm == 2:
        names = list()
        for i in range(user_choice_gm):
            names.append(raw_input("Entrez le nom du joueur {} ({disk}): ".format(i+1, disk="X" if i==0 else "O")))
        player_X = HumanPlayer("X", names[0])
        player_O = HumanPlayer("O", names[1])
    else:
        player_X = MaximumPlayer("X", "IA_Maximum", user_choice_size)
        player_O = AlphaBetaPlayer("O", "IA_Minimax", user_choice_size)
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