# coding: utf-8
 
"""
Filename : GameEngine.py
Authors : 
Date :
Description :
    Contains the scoreboard and the progress of the game.
    Also contains the main engine to play, hence allowing
    to play a turn the good way.
"""

from HumanPlayer import HumanPlayer
from RandomPlayer import RandomPlayer
from Board import Board
from GamePlayer import PlayerEngine


class Score(object):
    """Scoreboard of the game."""

    def __init__(self, player_X, player_O):
        """
        Both player's score is 2 at game's start.
        :param player_X: Player who's playing with X disks
        :param player_O: Player who's playing with O disks"""
        self.black_score, self.white_score = 2, 2
        self.black_name, self.white_name = player_X.name, player_O.name
        

    def update_score(self, black, white):
        """
        Update player's score.
        :param black: New value of black score.
        :param white: New value of white score.
        """
        self.black_score, self.white_score = black, white

    def display_score(self):
        """Print the scoreboard, which include both player's score."""
        print "\n~~~~   ScoreBoard   ~~~~"
        print self.black_name + " (X): " + str(self.black_score)
        print self.white_name + " (O): " + str(self.white_score)
        print "~~~~~~~~~~~~~~~~~~~~~~~~"
    
class Turn(object):
    """Keep track of game's turn number and player."""
    
    def __init__(self, player_X, player_O):
        """
        First player to play is Black (X).
        :param player_X: Player who's playing with X disks
        :param player_O: Player who's playing with O disks
        """
        self.player_X = player_X
        self.player_O = player_O
        self.player = player_X
        self.turn = 1
    
    def change_turn(self, did_play=True):
        """
        Change the actual player and the turn number
        :param did_play: Either True or False. If false, it means the last player wasn't able to play.
        Therefore, we don't increase the turn number, and the final maximum number of turn is size_board**2
        """
        self.player = self.player_X if self.player==self.player_O else self.player_O
        if did_play:
            self.turn += 1

    def get_player(self):
        """Return the player who is playing"""
        return self.player

    def display_turn(self):
        """"Display the turn number a nice way."""
        print "\n~~~~     TOUR %d     ~~~~" % self.turn

class GameEngine(object):
    """An Othello Game"""
    over = 0 # If over is 2, then it means that for two turn in a row no one played. Game over.

    def __init__(self, player_X, player_O, SIZE):
        """
        Define game caracteristics
        :param player_X: Player who's playing with X disks
        :param player_O: Player who's playing with O disks
        :param SIZE: Board's size
        """
        self.player_X = player_X
        self.player_O = player_O
        self.scoreboard = Score(player_X, player_O)
        self.turn = Turn(player_X, player_O)
        self.board = Board(SIZE)
        self.board.starting_board()
        self.player_engine = PlayerEngine(self.board, SIZE)

    def game(self, player):
        """
        A turn logic.
        :param player: Player who's playing this turn.
        """
        if self.over == 2 or not "." in self.board.board["grille"]: # Game Over
            print "\n~~~~ Grille  Finale ~~~~\n"
            print self.board
            return (self.board.get_score(self.player_X), self.board.get_score(self.player_O), self.board.empty_squares())
        self.turn.display_turn()
        print "~~~~ Plateau de Jeu ~~~~\n\n"
        print self.board
        self.scoreboard.display_score()
        valid_moves = self.player_engine.get_moves(player)
        if valid_moves:
            self.over = 0
            if type(player) is HumanPlayer:
                print "\n{}, c'est ton tour! ({})".format(player.name, player.disk)
                user_choice = raw_input("\nQuelle position souhaitez-vous jouer? ").upper().replace(" ", "")
                while user_choice not in valid_moves:
                    print "\nJouez une position legale!"
                    print "~~~~ Plateau de Jeu ~~~~\n\n"
                    print self.board
                    user_choice = raw_input("\nQuelle position souhaitez-vous jouer? (ColonneLigne) ").upper().replace(" ", "")
            else: # AIPlayer
                print "\nC'est le tour de l'ordinateur. ({})".format(player.disk)
                user_choice = player.get_move(valid_moves)
            print "\n{} joue en {}".format(player.name, user_choice)
            self.player_engine.play(user_choice[0], user_choice[1:], player, True)
            self.turn.change_turn()
            self.scoreboard.update_score(self.board.get_score(self.player_X), self.board.get_score(self.player_O))    
        else:
            self.over += 1
            self.turn.change_turn(False)
            print "{} ne peut pas jouer de position legale.".format(player.name)
        return False # Game continues

    def game_loop(self):
        """Main game loop"""
        over = False 
        while not over:
            player = self.turn.get_player()
            over = self.game(player)
        return over

if __name__ == "__main__":
    player_X = HumanPlayer("X", "Marshall Bruce Mathers III")
    player_O = HumanPlayer("O", "Lesane Parish Crooks")
    Score = Score(player_X,player_O)

    print "\nTest de Score.update_score() :"
    
    # Test en changeant le score de X à 42 et celui de O à 65
    Score.update_score(42, 65)
    if Score.black_score == 42 and Score.white_score == 65:
        test = "OK"
    else:
        test = "NOK"
    print "\nScore.update_score({},{}) => Score X : {} // Score O : {} \nResultat attendu = Score X : {} // Score O : {}".format(42, 65, Score.black_score, Score.white_score, 42, 65)
    print " ---> test {}".format(test)
    
    # Test en changeant le score de X à 2 et celui de O à 32
    Score.update_score(2, 32)
    if Score.black_score == 2 and Score.white_score == 32:
        test = "OK"
    else:
        test = "NOK"
    print "\nScore.update_score({},{}) => Score X : {} // Score O : {} \nResultat attendu = Score X : {} // Score O : {}".format(2, 32, Score.black_score, Score.white_score, 2, 32)
    print " ---> test {}".format(test)

    print "\n-----------------------------------------"
    
    Turn = Turn(player_X, player_O)
    
    print "\nTest de Test.change_turn() :"

    # Test au tour 65 ayant pour joueur O
    Turn.turn = 65
    Turn.player = player_O
    Turn.change_turn()
    if Turn.player == player_X and Turn.turn == 66:
        test = "OK"
    else:
        test = "NOK"
    print "\nTurn.change_turn() ==> Joueur du tour {}: {} \nResultat attendu = Joueur du tour {}: {}".format(Turn.turn, Turn.player, 66, player_X)
    print " ---> test {}".format(test)

    # Test au tour 5 ayant pour joueur X MAIS ne pouvant pas jouer (On ne change pas le nombre de tour actuel)
    Turn.turn = 5
    Turn.player = player_X
    Turn.change_turn(False)
    if Turn.player == player_O and Turn.turn == 5:
        test = "OK"
    else:
        test = "NOK"
    print "\nTurn.change_turn() ==> Joueur du tour {}: {} \nResultat attendu = Joueur du tour {}: {}".format(Turn.turn, Turn.player, 5, player_O)
    print " ---> test {}".format(test)

    print "\n-----------------------------------------"

    print "\nTest de Test.get_player() :"
    
    # Test avec pour joueur O
    Turn.player = player_O
    res = Turn.get_player()
    if res == player_O:
        test = "OK"
    else:
        test = "NOK"
    print "\nTurn.get_player() = {} ; Resultat attendu = {}".format(res, player_O)
    print " ---> test {}".format(test)

    # Test avec pour joueur X
    Turn.player = player_X
    res = Turn.get_player()
    if res == player_X:
        test = "OK"
    else:
        test = "NOK"
    print "\nTurn.get_player() = {} ; Resultat attendu = {}".format(res, player_X)
    print " ---> test {}".format(test)

    print "\n-----------------------------------------"

    print "\nPour tester les fonctions de la classe GameEngine, le mieux est de jouer des parties!"

    try:
        input("\n\n<Appuyez sur Enter pour quitter.>")
    except:
        pass