"""
Filename : GameEngine.py
Authors : 
Date :
Description :
"""

class Score(object):
    """Scoreboard of the game."""

    def __init__(self):
        """Both player's score is 2 at game's start."""
        self.black_score, self.white_score = 2, 2
        

    def update_score(self, black, white):
        """
        Update player's score.
        :param black: New value of black score.
        :param white: New value of white score.
        """
        self.black_score, self.white_score = black, white

    def display_score(self):
        """Print the scoreboard, which include both player's score."""
        print "~~~~ ScoreBoard ~~~~"
        print "Black Score (X): " + str(self.black_score)
        print "White Score (O): " + str(self.white_score)
        print "~~~~~~~~~~~~~~~~~~~~"
    
class Turn(object):
    """
    Keep track of game's turn number and player.
    """

    def __init__(self):
        """First player to play is Black (X)."""
        self.player = "X"
        self.turn = 1
    
    def __str__(self):
        return "Player's disk: " + self.player +"\nTurn: " + str(self.turn)

    def change_player(self):
        """Next player to play"""
        self.player = "X" if self.player=="O" else "O"
    
    def next_turn(self):
        """Next turn number"""
        self.turn += 1


if __name__ == "__main__":
    score = Score()
    score.display_score()
    score.update_score(10, 12)
    score.display_score()
    print
    
    turn = Turn()
    print turn
    turn.change_player()
    turn.next_turn()
    print turn