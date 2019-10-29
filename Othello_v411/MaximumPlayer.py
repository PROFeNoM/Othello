# coding: utf-8

"""
Filename : MaximumPlayer.py
Noms : 
    CHOURA Alexandre
    LEROUX Juliette
    MORTAGNE-CODERCH Anaelle
    WESCHLER Noé
Description :
    Ce fichier permet à l'ordinateur
    de jouer le coup retournant le
    maximum de disques ennemis.
"""
from copy import deepcopy
from Constant import Constant
from Board import Board

class MaximumPlayer(Board):

    def __init__(self, disk, name, SIZE):
        self.disk = disk
        self.name = name
        self.c = Constant(SIZE)

    def get_move(self, ennemy, pos, board, turn=None):
        best_score = -1e14 # -inf
        for move in pos:
            board_copy = self.play(move[0], move[1], self, deepcopy(board.board["grille"]))
            diff = board.board["grille"].count(self.disk) - board_copy.count(self.disk)
            if diff > best_score:
                best_score, best_pos = diff, move
        return best_pos

    def play(self, column, row, player, board, swap=True):
        """
        Conséquence d'un coup sur le plateau de jeu.
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
        if swap:
            return board
        return False # No valid moves in any dirrection