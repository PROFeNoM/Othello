# coding: utf-8
"""
# Branch : feature-AI03
# Description : wip Weak AI (alphabeta algorithm) #4
- AlphaBeta Pruning
# Version : 3.4.4
"""
from copy import deepcopy

class Board_Reversi(object):
    """Plateau de jeu"""
    initialized, size = False, 8 
    def __init__(self):
        if not self.initialized:
            print "\nFormat du plateau choisit: {}x{}".format(self.size, self.size)
            Board_Reversi.board = {"d" : self.size, "grille": ['.']*(self.size**2)}
            Board_Reversi.POS = {column + str(row) : x+self.size*y for x, column in enumerate([chr(i) for i in range(ord("A"), ord("A")+self.size)]) for y, row in enumerate(range(1,self.size+1))}
            Board_Reversi.POS.update({c : i for i,c in enumerate([chr(i) for i in range(ord("A"), ord("A")+self.size)])}) # Colonne str -> int
            Board_Reversi.POS.update({i : c for i,c in enumerate([chr(i) for i in range(ord("A"), ord("A")+self.size)])}) # Colonne int -> str
            Board_Reversi.DISK, Board_Reversi.ENNEMY_DISK = "XO", {"X" : "O", "O" : "X"}
            Board_Reversi.DIRECTIONS = [(x,y) for x in range(-1,2) for y in range(-1,2) if x or y]
            for pos, disk in zip([Board_Reversi.POS[key] for key in (Board_Reversi.POS[self.size/2 - 1] + str(self.size/2), Board_Reversi.POS[self.size/2] + str(self.size/2 + 1), Board_Reversi.POS[self.size/2 - 1] + str(self.size/2 + 1), Board_Reversi.POS[self.size/2] + str(self.size/2))], "OOXX"): # Positions initiales
                Board_Reversi.board["grille"][pos] = disk
            Board_Reversi.initialized = True
            
    def __str__(self):
        """Affiche l'etat du plateau de jeu"""
        return "    "+ " ".join([chr(i) for i in range(ord('A'), ord("A")+27)][:self.size]) + "\n" +"\n".join([(" "+str(row+1)+"  "+" ".join(self.board["grille"][i:i+self.size])) if row+1<10 else str(row+1)+"  "+" ".join(self.board["grille"][i:i+self.size]) for row, i in enumerate([n*self.size for n in range(self.size)])])

    def spot(self, column, row, board=None):
        """Retourne '.', 'O' ou 'X' en fonction de la piece sur l'emplacement"""
        if board:
            return board[self.POS[column+row]] 
        else:
            return self.board["grille"][self.POS[column+row]]
    
    def is_on_board(self, column, row):
        """Retoune True si l'emplacement est le plateau, False sinon"""
        return (0<=column<=self.size-1 and 1<=row<=self.size) 

    @staticmethod
    def place(column, row, disk, board=None):
        """Place un disque ("O" ou "X") a l'emplacement"""
        if board: # alphabeta algorithm
            board[Board_Reversi.POS[column+row]] = disk
        else:
            Board_Reversi.board["grille"][Board_Reversi.POS[column+row]] = disk

class Game_Reversi(Board_Reversi):
    """Permet d'appliquer les regles du jeu"""
    turn, turn_n, count = "X", 1, 0 # Si count = 2, alors deux tours d'affilé personne n'a joue. La partie est fini

    def __init__(self, names):
        """Initialise les joueurs de la partie"""
        self.players = [Player_Reversi(disk, name) for name, disk in zip(names, Board_Reversi().DISK)]

    def change_turn(self):
        """Permet de savoir quel joueur va jouer"""
        self.turn = "O" if self.turn == "X" else "X"
    
    def game(self, computer=False):
        """Deroulement de la partie"""
        if self.count == 2 or not "." in Board_Reversi.board["grille"]: # La partie est ternminé
            return True
        player = self.players[self.DISK.index(self.turn)]
        print "\n\t~~Tour {}~~\n\n".format(self.turn_n), Board_Reversi()
        print "\n(X: {} // O: {})".format(Board_Reversi.board["grille"].count("X"), Board_Reversi.board["grille"].count("O"))
        pos = player.can_play()
        if pos:
            self.count = 0
            if computer:
                if player.name == "L'ordinateur":
                    print "\nC'est le tour de l'ordinateur. ({})".format(player.disk)
                    c = player.computer_pos(pos, self.players[self.DISK.index(Board_Reversi.ENNEMY_DISK[self.turn])])
                    print "\nL'ordinateur joue en {}".format(c)
                    player.play(c[0],c[1:], player.disk, True)
                else:
                    print "\n{}, c'est ton tour! ({})".format(player, player.disk)
                    user_choice = raw_input("\nQuelle position souhaitez-vous jouer? ")
                    while user_choice.upper().replace(" ", "") not in pos:
                        print "\nJouez une position legale!"
                        print Board_Reversi()
                        user_choice = raw_input("\nQuelle position souhaitez-vous jouer? (ColonneLigne) ")
                    print "\n{} joue en {}!".format(player, user_choice.upper().replace(" ", ""))
                    player.play(user_choice.upper().replace(" ", "")[0], user_choice.upper().replace(" ", "")[1:], player.disk, True)
                self.change_turn()
                self.turn_n += 1
            else:
                print "\n{}, c'est ton tour! ({})".format(player, player.disk)
                user_choice = raw_input("\nQuelle position souhaitez-vous jouer? ")
                while user_choice.upper(). replace(" ", "") not in pos:
                    print "\nJouez une position legale!"
                    print Board_Reversi()
                    user_choice = raw_input("\nQuelle position souhaitez-vous jouer? (ColonneLigne) ")
                print "\n{} joue en {}!".format(player, user_choice.upper().replace(" ", ""))
                player.play(user_choice.upper().replace(" ", "")[0], user_choice.upper().replace(" ", "")[1:], player.disk, True)
                self.change_turn()
                self.turn_n += 1
        else:
            self.count += 1
            self.change_turn()
            print "{} ne peut pas jouer de position legale.".format(player)
        return False # La partie continue
    
class Player_Reversi(Game_Reversi):
    """Joueur"""
    def __init__(self, disk, name):
        """Caractérisation du joueur"""
        self.disk, self.name = disk, name
    
    def __str__(self):
        """Renvoie le nom du joueur"""
        return self.name
    
    def can_play(self, board=None):
        """Renvoie la liste des positions légales de jeu pour le joueur"""
        return [c+str(r) for c in [chr(i) for i in range(ord("A"), ord("A")+Board_Reversi().size)] for r in range(1,Board_Reversi().size+1) if self.play(c, str(r), self.disk, False, board)]

    def play(self, column, row, disk, swap=False, board=None): # (Board is not None) seulement w/ alphabeta
        """Determine si un coup est legal ou non"""
        if self.spot(column, row, board) is not ".": # L'emplacement est deja occupe
            return False
        for dc, dr in self.DIRECTIONS: # On se deplace dans une direction donnee et on verifie si on peut encercler
            c, r = self.POS[column] + dc, int(row) + dr
            amount = None # on verifie s'il y a un disque ennemi dans la direction
            while Board_Reversi().is_on_board(c, r) and self.spot(self.POS[c], str(r), board) == self.ENNEMY_DISK[disk]:
                c += dc
                r += dr
                amount = True
            if not Board_Reversi().is_on_board(c, r) or amount is None or not self.spot(self.POS[c], str(r), board) == disk: # PEUT ETRE PAS OBLIGE DE DEFINIR DISK DANS PLAY ==>self.disk
                continue # On ne peut pas enclercler car soit il n'y a pas de disque ennemi dans la direction ou ce n'est pas un de nos disque au bout
            if swap:
                c_swap, r_swap = self.POS[column], int(row)
                while (c_swap, r_swap) != (c,r):
                    self.place(self.POS[c_swap], str(r_swap), self.disk, board)
                    c_swap += dc
                    r_swap += dr
                if not board: # On change le tour si on utlise pas alphabeta
                    self.change_turn()
            else:
                return True # Dans cette direction, un emplacement est donc disponible
        if board and swap: # Pour alphabeta uniquement, on renvoie l'etat du plateau actuel seulement lorsque l'on change les pieces
            return board
        return False # Dans toutes directions, il n'y a aucun enplacement
        
    def evaluation(self, ennemy, board, depth):
        """Renvoie un int correspondant au score du plateau du joueur"""
        CORNER = ["A1", chr(ord("A")+Board_Reversi().size-1)+"1", "A"+str(Board_Reversi().size), chr(ord("A")+Board_Reversi().size-1)+str(Board_Reversi().size)]
        X_SQUARES = ["B2", chr(ord("A")+Board_Reversi().size-2)+"2", "B"+str(Board_Reversi().size-1), chr(ord("A")+Board_Reversi().size-2)+str(Board_Reversi().size-1)]
        C_SQUARES = [["A2", "B1"], [chr(ord("A")+Board_Reversi().size-2)+"1", chr(ord("A")+Board_Reversi().size-1)+"2"], ["A"+str(Board_Reversi().size-1), "B"+str(Board_Reversi().size)], [chr(ord("A")+Board_Reversi().size-2)+str(Board_Reversi().size), chr(ord("A")+Board_Reversi().size-1)+str(Board_Reversi().size-1)]]
        
        # Corner possesion
        player_corner = (board[Board_Reversi.POS[CORNER[0]]]==self.disk) + (board[Board_Reversi.POS[CORNER[1]]]==self.disk) + (board[Board_Reversi.POS[CORNER[2]]]==self.disk) + (board[Board_Reversi.POS[CORNER[3]]]==self.disk)
        ennemy_corner = (board[Board_Reversi.POS[CORNER[0]]]==ennemy.disk) + (board[Board_Reversi.POS[CORNER[1]]]==ennemy.disk) + (board[Board_Reversi.POS[CORNER[2]]]==ennemy.disk) + (board[Board_Reversi.POS[CORNER[3]]]==ennemy.disk)
        
        # X Squares possesion
        # C Squares possesion
        player_X, ennemy_X = 0, 0
        player_C, ennemy_C = 0, 0
        for c in range(4):
            if board[Board_Reversi.POS[CORNER[c]]]==".":
                player_X += board[Board_Reversi.POS[X_SQUARES[c]]]==self.disk
                player_C += board[Board_Reversi.POS[C_SQUARES[c][0]]]==self.disk + board[Board_Reversi.POS[C_SQUARES[c][1]]]==self.disk
            elif board[Board_Reversi.POS[CORNER[c]]]==".":
                ennemy_X += board[Board_Reversi.POS[X_SQUARES[c]]]==ennemy.disk
                ennemy_C += board[Board_Reversi.POS[C_SQUARES[c][0]]]==ennemy.disk + board[Board_Reversi.POS[C_SQUARES[c][1]]]==ennemy.disk

        # Disk possesion
        player_disk, ennemy_disk = board.count(self.disk), board.count(ennemy.disk)

        # Possible moves
        player_move, ennemy_move = len(self.can_play(board)), len(ennemy.can_play(board))

        # Total dynamic score
        
        # End Game
        if board.count(".")==0:
            if player_disk>ennemy_disk:
                return 1e4
            elif player_disk<ennemy_disk:
                return -1e4
            else:
                return 0

        disk_count = player_disk+ennemy_disk
        if disk_count < Board_Reversi().size**2-20:
            t = 0
        else:
            t = 1
        return (Board_Reversi().size**2+2-disk_count)*(player_corner-ennemy_corner) + (-Board_Reversi().size**2+4+disk_count)*(player_X-ennemy_X) + (-Board_Reversi().size**2+1+disk_count)*(player_C-ennemy_C) + t*(player_disk-ennemy_disk) + (player_move-ennemy_move)

    def alphabeta(self, player, depth, is_maximizing_player, ennemy, board, alpha, beta):
        """AlphaBeta Pruning algorithm"""
        pos = player.can_play(board)
        if depth == 0 or not pos:
            return player.evaluation(ennemy, board, depth)
        if is_maximizing_player:
            best_score = -1e14 #-inf
            for c in pos:
                board_copy = player.play(c[0], c[1:], player.disk, True, deepcopy(board))
                best_score = max(best_score, self.alphabeta(ennemy, depth-1, False, player, board_copy, alpha, beta))
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break # Beta cutoff
            return best_score
        else: # Minimize
            best_score = 1e14 # inf
            for c in pos:
                board_copy = player.play(c[0], c[1:], player.disk, True, deepcopy(board))
                best_score = min(best_score, self.alphabeta(ennemy, depth-1, True, player, board_copy, alpha, beta))
                beta = min(beta, best_score)
                if beta <= alpha:
                    break # Alpha cutoff
            return best_score


    def computer_pos(self, pos, ennemy):
        """Determine une position de jeu pour l'ordinateur"""
        best_score = -1e14 #-inf
        for c in pos:
            board_copy = self.play(c[0], c[1:], self.disk, True, deepcopy(Board_Reversi.board["grille"]))
            if self.turn_n <= ((Board_Reversi().size)**2-4)/3:
                score = self.alphabeta(ennemy, 3, False, self, board_copy, -1e14, 1e14) # Anticipe sur 3 tours
            elif self.turn_n <= 2*((Board_Reversi().size)**2-4)/3:
                score = self.alphabeta(ennemy, 5, False, self, board_copy, -1e14, 1e14) # Anticipe sur 5 tours
            elif self.turn_n >= Board_Reversi().size**2-20: 
                score = self.alphabeta(ennemy, 19, False, self, board_copy, -1e14, 1e14) # Anticipe jusqu'à la fin du jeu
            else: 
                score = self.alphabeta(ennemy, 7, False, self, board_copy, -1e14, 1e14) # Anticipe sur 7 tours
            if score > best_score:
                best_score, best_pos = score, c
        return best_pos

def ask_number(question, low, high):
    """Ask for a number within a range."""
    res = None
    while res not in range(low,high+1):
        try:
            res = int(input(question))
            if res not in range(low, high+1):
                print "Entrez une valeur entre {} et {}".format(low, high)
        except:
            print "Entrez une reponse correcte."
    return res

def winner(player_1, player_2, size):
    """Détermine et affiche le gagnant/perdant de la partie"""
    print "\n\tGrille finale:\n", Board_Reversi()
    score_p1, score_p2 = Board_Reversi.board["grille"].count("X"), Board_Reversi.board["grille"].count("O")
    if "." in Board_Reversi.board["grille"]:
        if score_p1 > score_p2:
            score_p1 += Board_Reversi.board["grille"].count(".")
        elif score_p2 > score_p1:
            score_p2 += Board_Reversi.board["grille"].count(".")
    if score_p1 > score_p2:
        print "\n{} gagne avec {} points, contre {} pour {} !".format(player_1, score_p1, score_p2, player_2)
    elif score_p1 < score_p2:
        print "\n{} gagne avec {} points, contre {} pour {} !".format(player_2, score_p2, score_p1, player_1)
    else:
        print "\nEGALITE! Les deux joueurs ont {} points!".format(size**2/2)
            
def main():
    """Déroulement d'une partie d'Othello"""
    print "\t\t\t\t\tBienvenue sur Othello!"
    names = []
    user_choice_size = ask_number("""
                             Combien de lignes (ou colonnes) doit avoir le plateau ?
                             --> """, low = 2, high = 26)
    Board_Reversi.size = user_choice_size
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
        names = [name, "L'ordinateur"] if user_choice_c == 1 else ["L'ordinateur", name]
        print "\nPour jouer une position, saisissez les coordonnees sous la forme ColonneLigne (A4, B6, ...)"
        game, over = Game_Reversi(names), False
        while not over:
            over = game.game(True)
        winner(names[0], names[1], user_choice_size)
    
    else:
        for i in range(user_choice_gm):
            names.append(raw_input("Entrez le nom du joueur {} ({disk}): ".format(i+1, disk="X" if i==0 else "O")))
        print 
        print "Pour jouer une position, saisissez les coordonnees sous la forme ColonneLigne (A4, B6, ...)"
        game = Game_Reversi(names)
        over = False
        while not over:
            over = game.game()
        winner(names[0], names[1], user_choice_size)

    print "\nLa partie est termine! A bientot."

main()

try:
    input("\n\n<Appuyez sur Enter pour quitter.>")
except:
    pass
