"""
Filename : GameEngine.py
Authors : 
Date :
Description :
"""
from Constant import Constant

class PlayerEngine(object):
    """Everything a Player is able to do to interact with the board"""

    def __init__(self, board, SIZE):
        self.board = board
        self.c = Constant(SIZE)
        
    def play(self, column, row, player, swap=False):
        """
        Consequence of a move on the board
        :param column: Column played
        :param row: Row played
        :param player: Player who initiated the move
        :param swap: If True, doesn't change the actual state of the board. 
        Used to determine valid moves.
        """
        if self.board.spot(column, row) is not ".": # Spot is already filled
            return False
        for dc, dr in self.c.DIRECTIONS:
            c, r = self.c.COL_NUM[column] + dc, int(row) + dr
            amount = None # Check if there's an ennemy disk in the given direction
            while self.board.is_on_board(c, r) and self.board.spot(self.c.NUM_COL[c], str(r)) == self.c.ENNEMY_DISK[player.disk]:
                c += dc
                r += dr
                amount = True
            if not self.board.is_on_board(c, r) or amount is None or not self.board.spot(self.c.NUM_COL[c], str(r)) == player.disk:
                continue 
                # We can't surround the ennemy 
                # OR there isn't ennemy disk in the direction 
                # OR the last disk isn't part of player's one
            if swap: # We change the board
                c_swap, r_swap = self.c.COL_NUM[column], int(row)
                while (c_swap, r_swap) != (c,r):
                    self.board.place(self.c.NUM_COL[c_swap], str(r_swap), player.disk)
                    c_swap += dc
                    r_swap += dr
            else:
                return True # In this direction, we can play
        return False # No valid moves in any dirrection

    def get_moves(self, player):
        """
        Return the list of every valid moves for a player
        :param player: Player we are looking legal moves
        """
        return [c+str(r) for c in self.c.COL for r in self.c.RW if self.play(c, str(r), player, False)]

if __name__ == "__main__":
    pass
