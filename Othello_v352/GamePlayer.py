# coding: utf-8

"""
Filename : GamePlayer.py
Authors : 
Date :
Description :
    Contains what the game engine needs to see whether
    or not a player can play, where and change the board
    according to player's decision.
"""
from Constant import Constant

class PlayerEngine(object):
    """Everything a Player is able to do to interact with the board"""

    def __init__(self, board, SIZE):
        """
        Utility of PlayerEngine
        :param board: The board (class) we are playing with
        :param SIZE: board's size
        """
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
    from Board import Board
    from HumanPlayer import HumanPlayer

    print "Test de PlayerEngine.get_moves() :"

    # Pour un plateau 2x2 plein, aucun coups n'est possible
    SIZE = 2
    board_2 = Board(SIZE)
    player_X = HumanPlayer("X", "Marshall Bruce Mathers III")
    player_O = HumanPlayer("O", "Lesane Parish Crooks")
    engine_2 = PlayerEngine(board_2, SIZE)
    res = engine_2.get_moves(player_X)
    if res == []:
        test = "OK"
    else:
        test = "NOK"
    print "\nengine_2.get_moves({}) = {} ; Resultat attendu = {}".format(player_X, res, [])
    print " ---> test {}".format(test)

    # Pour un plateau 4x4, avec 1 coup possible pour X
    SIZE = 4
    board_4 = Board(SIZE)
    board_4.board["grille"] = ["X","O","O","X","O","O","O","X","X","X","O","O","X","X","O","."]
    engine_4 = PlayerEngine(board_4, SIZE)
    res = engine_4.get_moves(player_X)
    if res == ["D4"]:
        test = "OK"
    else:
        test = "NOK"
    print "\nengine_4.get_moves({}) = {} ; Resultat attendu = {}".format(player_X, res, ["D4"])
    print " ---> test {}".format(test)

    # Pour un plateau 4x4 plein, avec 0 coup possible pour O
    res = engine_4.get_moves(player_O)
    if res == []:
        test = "OK"
    else:
        test = "NOK"
    print "\nengine_4.get_moves({}) = {} ; Resultat attendu = {}".format(player_O, res, [])
    print " ---> test {}".format(test)

    # Test pour un plateau 12x12 "en cours", pour le joueur O
    SIZE = 12
    board_12 = Board(SIZE)
    board_12.board["grille"] = ["."]*(12*2+6)+["O"]+["."]*7+["X","O",".",".","O"]+["."]*8+["X","O","X","X","O"]+["."]*8+["O","X","X",".","O"]+["."]*7+["X"]+["O"]*3+["."]*7+["X","O",".","X"]+["."]*9+["O"]+["."]*(7+12*3)
    engine_12 = PlayerEngine(board_12, SIZE)
    res = engine_12.get_moves(player_O)
    if res == ['B3', 'B4', 'C5', 'C7', 'C8', 'D6', 'D7', 'E4', 'F4', 'F9', 'G9', 'H6', 'H9']:
        test = "OK"
    else:
        test = "NOK"
    print "\nengine_12.get_moves({}) = {} ; Resultat attendu = {}".format(player_O, res, ['B3', 'B4', 'C5', 'C7', 'C8', 'D6', 'D7', 'E4', 'F4', 'F9', 'G9', 'H6', 'H9'])
    print " ---> test {}".format(test)

    # Test pour le plateau 12x12 "en cours", pour le joueur X
    res = engine_12.get_moves(player_X)
    if res == ['C3', 'D3', 'D6', 'D7', 'D9', 'E4', 'E10', 'F8', 'F10', 'G2', 'H3', 'H8', 'I4', 'I5', 'I7', 'I8', 'J5']:
        test = "OK"
    else:
        test = "NOK"
    print "\nengine_12.get_moves({}) = {} ; Resultat attendu = {}".format(player_X, res, ['C3', 'D3', 'D6', 'D7', 'D9', 'E4', 'E10', 'F8', 'F10', 'G2', 'H3', 'H8', 'I4', 'I5', 'I7', 'I8', 'J5'])
    print " ---> test {}".format(test)


    # Test pour le plateau 8x8 initial, pour le joueur X
    SIZE = 8
    board_8 = Board(SIZE)
    board_8.starting_board()
    engine_8 = PlayerEngine(board_8, SIZE)
    res = engine_8.get_moves(player_X)
    if res == ['C4', 'D3', 'E6', 'F5']:
        test = "OK"
    else:
        test = "NOK"
    print "\nengine_8.get_moves({}) = {} ; Resultat attendu = {}".format(player_X, res, ['C4', 'D3', 'E6', 'F5'])
    print " ---> test {}".format(test)

    # Test pour le plateau 8x8 initial, pour le joueur O
    res = engine_8.get_moves(player_O)
    if res == ['C5', 'D6', 'E3', 'F4']:
        test = "OK"
    else:
        test = "NOK"
    print "\nengine_8.get_moves({}) = {} ; Resultat attendu = {}".format(player_O, res, ['C5', 'D6', 'E3', 'F4'])
    print " ---> test {}".format(test)

    print "\n-----------------------------------------"

    print "\nTest de PlayerEngine.play() :"

    # Test avec le plateau 12x12, le joueur O jouant en B3
    engine_12.play("B", "3", player_O, True)
    res = board_12.board["grille"]
    expected = ["."]*(12*2+1)+["O"]+["."]*4+["O"]+["."]*7+["O","O",".",".","O"]+["."]*8+["O","O","X","X","O"]+["."]*8+["O","X","X",".","O"]+["."]*7+["X"]+["O"]*3+["."]*7+["X","O",".","X"]+["."]*9+["O"]+["."]*(7+12*3)
    if res == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nengine_12.play({},{},{},{}) = {} \nResultat attendu = {}".format("B", "3", player_O,True,res,expected)
    print " ---> test {}".format(test)

    # Test avec le plateau 12x12, le joueur X jouant en E10
    engine_12.play("E", "10", player_X, True)
    res = board_12.board["grille"]
    expected = ["."]*(12*2+1)+["O"]+["."]*4+["O"]+["."]*7+["O","O",".",".","O"]+["."]*8+["O","O","X","X","O"]+["."]*8+["O","X","X",".","O"]+["."]*7+["X"]+["O"]*3+["."]*7+["X","X",".","X"]+["."]*9+["X"]+["."]*11+["X"]+["."]*(12*2+7)
    if res == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nengine_12.play({},{},{},{}) = {} \nResultat attendu = {}".format("E", "10", player_X,True,res,expected)
    print " ---> test {}".format(test)

    # Test avec le plateau 8x8 initial, le joueur X jouant en C4
    engine_8.play("C", "4", player_X, True)
    res = board_8.board["grille"]
    expected = ["."]*26+["X"]*3+["."]*6+["X","O"]+["."]*27
    if res == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nengine_8.play({},{},{},{}) = {} \nResultat attendu = {}".format("C", "4", player_X,True,res,expected)
    print " ---> test {}".format(test)

    # Test avec le plateau 8x8, le joueur O jouant en C3
    engine_8.play("C", "3", player_O, True)
    res = board_8.board["grille"]
    expected = ["."]*(8*2+2)+["O"]+["."]*7+["X","O","X"]+["."]*6+["X","O"]+["."]*27
    if res == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nengine_8.play({},{},{},{}) = {} \nResultat attendu = {}".format("C", "3", player_O,True,res,expected)
    print " ---> test {}".format(test)

    # Test avec le plateau 4x4, le joueur X jouant en D4
    engine_4.play("D", "4", player_X, True)
    res = board_4.board["grille"]
    expected = ["X","O","O","X"]+["O","X"]*2+["X"]*8
    if res == expected:
        test = "OK"
    else:
        test = "NOK"
    print "\nengine_4.play({},{},{},{}) = {} \nResultat attendu = {}".format("D","4",player_X,True,res,expected)
    print " ---> test {}".format(test)

    try:
        input("\n\n<Appuyez sur Enter pour quitter.>")
    except:
        pass