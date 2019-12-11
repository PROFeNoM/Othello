# coding: utf-8

"""
Filename : MinimaxPlayer.py
Noms : 
    CHOURA Alexandre
    LEROUX Juliette
    MORTAGNE-CODERCH Anaelle
    WESCHLER Noé
Description :
    Ce fichier permet d'utiliser l'algorithme Minimax
    afin de permettre à l'ordinateur de jouer son coup.
Nota: 
    Les résultats peuvent varier avec l'élagage AlphaBeta
    en raison de profondeur de recherche différentes.

    Pour avoir une barre de progrès lors de la recherche
    enlevez les commentaires ligne 65 et 75 (ne fonctionne pas si lancé avec IDLE).
"""

from copy import copy
from Heuristic import Heuristic
from Board import Board
from Constant import Constant
import sys

class MinimaxPlayer(Board):
    """Minimax Pruning algorithm"""

    def __init__(self, disk, name, SIZE):
        """
        Initialize le nom du joueur, son disque et les outils nécéssaire au fonctionnement
        de l'algorithme Minimax.
        :param disk: Soit "X" ou "O".
        :param name: Nom du joueur (str).
        :param SIZE: taille du plateau.
        """
        self.disk = disk
        self.name = name
        self.SIZE = SIZE
        self.eval = Heuristic(SIZE)
        self.c = Constant(SIZE)

    def progress(self, progress):
        """
        Permet de mettre une barre de progrès lors de la recherche d'un coup.
        !! NE FONCTIONNE PAS SUR IDLE !!
        :param progress: Progrès de la barre, entre 0 et 100.
        """
        sys.stdout.write("\r[{}{}] {}%".format("#"*(int(progress/10)), " "*(10-int(progress/10)),round(progress, 1)))
        sys.stdout.flush()

    def get_move(self, ennemy, pos, board, turn):
        """
        Détermine une position de jeu pour l'ordinateur.
        La profondeur de recherche évolue au cours de la partie pour réduire
        le temps de calcul.
        :param ennemy: Joueur adversaire de celui définit précédement.
        :param pos: Position de jeu possible de player sur le plateau en cours.
        :param board: Plateau actuel.
        :param turn: Nombre de tour de jeu.
        """
        best_score = -1e14 # -inf
        for move in pos:
            #self.progress(pos.index(move)/float(len(pos))*100)
            board_copy = self.play(move[0], move[1:], self, copy(board.board["grille"]), True)
            if turn <= 2*(self.SIZE**2-4)/3:
                score = self.minimax(ennemy, 3, False, self, board_copy) # Anticipe sur 3 tours
            elif turn >= self.SIZE**2-10:
                score = self.minimax(ennemy, 11, False, self, board_copy) # Anticipe jusqu'à la fin du jeu
            else:
                score = self.minimax(ennemy, 3, False, self, board_copy) # Anticipe sur 3 tours
            if score > best_score:
                best_score, best_pos = score, move
        #self.progress(100)
        return best_pos

    def minimax(self, player, depth, is_maximizing_player, ennemy, board):
        """
        L'élagage AlphaBeta.
        :param player: Joueur du noeud dans l'arbre.
        :param depth: Profondeur de recherche suivant le noeud.
        :param is_maximizing_player: Booléen caractérisant le caractère min ou max de player.
        :param ennemy: Joueur adversaire à player.
        :param board: Etat du plateau de jeu à un noeud donné.
        """
        pos = self.get_moves(player, board)
        if depth == 0 or not pos:
            return self.eval.evaluation(player, ennemy, board)
        if is_maximizing_player:
            best_score = -1e14 #-inf
            for c in pos:
                board_copy = self.play(c[0], c[1:], player, copy(board), True)
                best_score = max(best_score, self.minimax(ennemy, depth-1, False, player, board_copy))
            return best_score
        else: #Minimize
            best_score = 1e14 #inf
            for c in pos:
                board_copy = self.play(c[0], c[1:], player, copy(board), True)
                best_score = min(best_score, self.minimax(ennemy, depth-1, True, player, board_copy))
            return best_score

    def play(self, column, row, player, board, swap=False):
        """
        Conséquence d'un coup sur le plateau de jeu.
        Renvoie le plateau de jeu après les changements engendrés par 
        un coup pour les algorithmes Minimax/AB.
        :param column: Colonne jouée.
        :param row: Ligne jouée.
        :param player: Joueur qui a joué le coup.
        :param board: Plateau utilisé au cours de l'algorithme AlphaBeta/Minimax.
        :param swap: Si False, ne change pas l'état actuel du plateau. 
        Utilisé pour déterminer les coups légaux d'un joueur.
        """
        if self.spot(column, row, board) is not ".": # Spot is already filled
            return False
        for dc, dr in self.c.DIRECTIONS:
            c, r = self.c.COL_NUM[column] + dc, int(row) + dr
            amount = None # Check if there's an ennemy disk in the given direction
            while self.is_on_board(c, r) and self.spot(self.c.NUM_COL[c], str(r), board) == self.c.ENNEMY_DISK[player.disk]:
                c += dc
                r += dr
                amount = True
            if not self.is_on_board(c, r) or amount is None or not self.spot(self.c.NUM_COL[c], str(r), board) == player.disk:
                continue 
                # We can't surround the ennemy 
                # OR there isn't ennemy disk in the direction 
                # OR the last disk isn't part of player's one
            if swap: # We change the board
                c_swap, r_swap = self.c.COL_NUM[column], int(row)
                while (c_swap, r_swap) != (c,r):
                    self.place(self.c.NUM_COL[c_swap], str(r_swap), player.disk, board)
                    c_swap += dc
                    r_swap += dr
            else:
                return True # In this direction, we can play
        if board and swap:
            # Used exclusively for AlphaBeta Pruning algorithm/Minimax
            # Return the state of the board after we returned disks
            return board
        return False # No valid moves in any dirrection

    def get_moves(self, player, board):
        """
        Retourne les coups légaux possibles pour un joueur.
        :param player: Joueur pour lequel on veut connaître les coups légaux possibles.
        :param board: Plateau utilisé au cours de l'algorithme AlphaBeta/Minimax.
        """
        return [c+str(r) for c in self.c.COL for r in self.c.RW if self.play(c, str(r), player, board, False)]

if __name__ == "__main__":
    import time
    AB = MinimaxPlayer("X", "oui", 8)
    for prog in range(101):
        time.sleep(0.1)
        #AB.progress(prog)
