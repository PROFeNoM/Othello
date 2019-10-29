# coding: utf-8

"""
Filename : Heuristic.py
Noms : 
    CHOURA Alexandre
    LEROUX Juliette
    MORTAGNE-CODERCH Anaelle
    WESCHLER Noé
Description :
    Ce fichier est utliser par les algorthmes
    Minimax/AlphaBeta pour évaluer la valeur du
    plateau de jeu pour un joueur à un moment donné.
"""

from Constant import Constant
from GamePlayer import PlayerEngine
from Board import Board

class Heuristic(PlayerEngine):

    def __init__(self, SIZE):
        """Définit l'utilitaire utilisé par evaluation()"""
        self.SIZE = SIZE
        self.c = Constant(SIZE)
        self.engine = PlayerEngine(Board(SIZE), SIZE)

    def evaluation(self, player, ennemy, board):
        """Renvoie un int correspondant au score du plateau pour un joueur"""
        # Corner possesion
        player_corner = (board[self.c.POSITION[self.c.CORNER[0]]]==player.disk) \
                        + (board[self.c.POSITION[self.c.CORNER[1]]]==player.disk) \
                        + (board[self.c.POSITION[self.c.CORNER[2]]]==player.disk) \
                        + (board[self.c.POSITION[self.c.CORNER[3]]]==player.disk)

        ennemy_corner = (board[self.c.POSITION[self.c.CORNER[0]]]==ennemy.disk) \
                        + (board[self.c.POSITION[self.c.CORNER[1]]]==ennemy.disk) \
                        + (board[self.c.POSITION[self.c.CORNER[2]]]==ennemy.disk) \
                        + (board[self.c.POSITION[self.c.CORNER[3]]]==ennemy.disk)

        # X squares possesion
        # C squares possesion
        player_X, ennemy_X = 0, 0
        player_C, ennemy_C = 0, 0
        for c in range(4):
            if board[self.c.POSITION[self.c.CORNER[c]]] == ".":
                player_X += board[self.c.POSITION[self.c.X_SQUARES[c]]] == player.disk
                player_C += board[self.c.POSITION[self.c.C_SQUARES[c][0]]] == player.disk \
                            + board[self.c.POSITION[self.c.C_SQUARES[c][1]]] == player.disk
                ennemy_X += board[self.c.POSITION[self.c.X_SQUARES[c]]] == ennemy.disk
                ennemy_C += board[self.c.POSITION[self.c.C_SQUARES[c][0]]] == ennemy.disk \
                            + board[self.c.POSITION[self.c.C_SQUARES[c][1]]] == ennemy.disk
        
        
        # Disk possesion
        player_disk, ennemy_disk = board.count(player.disk), board.count(ennemy.disk)

        # Possible moves
        player_move, ennemy_move = len(self.engine.get_moves(player, board)), len(self.engine.get_moves(ennemy, board))

        # Total dynamic score

        # End Game
        if board.count(".") == 0:
            if player_disk > ennemy_disk:
                return 1e4
            elif player_disk < ennemy_disk:
                return -1e4
            else:
                return 0
        
        disk_count = player_disk+ennemy_disk
        if disk_count < self.SIZE*self.SIZE-20:
            t = 0
        else:
            t = 1
        score = (self.SIZE*self.SIZE+2-disk_count)*(player_corner-ennemy_corner) \
                + (-self.SIZE*self.SIZE+4+disk_count)*(player_X-ennemy_X) \
                + (-self.SIZE*self.SIZE+1+disk_count)*(player_C-ennemy_C) \
                + t*(player_disk-ennemy_disk) \
                + (player_move-ennemy_move)
        return score