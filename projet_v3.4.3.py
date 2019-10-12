# coding: utf-8
"""
# Branch : feature-AI03
# Description : wip Weak AI (Minimax algorithm) #4 
- Disk differential
- Mobility
- Position weight
- Stability
- Corner possesion
- Frontier Disk
# Version : 3.4.3.2
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
            # -- La section qui suit ne sert qu'à l'AI (cf. computer_pos()) --
            Board_Reversi.WEIGHT_SET = [[8, 85, -40, 10, 210, 520],
                                        [8, 85, -40, 10, 210, 520],
                                        [33, -50, -15, 4, 416, 2153],
                                        [46, -50, -1, 3, 612, 4141],
                                        [51, -50, 62, 3, 595, 3184],
                                        [33, -5, 66, 2, 384, 2777],
                                        [44, 50, 163, 0, 443, 2568],
                                        [13, 50, 66, 0, 121, 986],
                                        [4, 50, 31, 0, 27, 192],
                                        [8, 500, 77, 0, 36, 299]]
            Board_Reversi.TURN_SET = [0]+[i for i in range(self.size**2-9, self.size**2)]
            Board_Reversi.WEIGHT_TIME = {t : [None]*6 for t in range(self.size**2+1)}
            for dc in range(self.size**2+1):
                # détermine quel set utiliser pour un tour donné
                w = 0
                for i in range(len(Board_Reversi.TURN_SET)):
                    if dc <= Board_Reversi.TURN_SET[i]:
                        w = i
                        break
                # First set of weight
                if w == 0:
                    Board_Reversi.WEIGHT_TIME[dc] = Board_Reversi.WEIGHT_SET[0]
                    continue
                
                factor = float((dc-Board_Reversi.TURN_SET[w-1]))/(Board_Reversi.TURN_SET[w]-Board_Reversi.TURN_SET[w-1])
                for i in range(6):
                    Board_Reversi.WEIGHT_TIME[dc][i] = int(factor*Board_Reversi.WEIGHT_SET[w][i]+(1-factor)*Board_Reversi.WEIGHT_SET[w-1][i])
            print Board_Reversi.WEIGHT_TIME
            if self.size == 4:
                Board_Reversi.POSITION_WEIGHT = [100, 8, 8, 100,
                                                 8, -3, -3, 8,
                                                 8, -3, -3, 8,
                                                 100, 8, 8, 100]
            elif self.size == 6:
                Board_Reversi.POSITION_WEIGHT = [100, -10, 8, 8, -10, 100,
                                                 -10, -25, -4, -4, -25, -10,
                                                 8, -4, 0, 0, -4, 8,
                                                 8, -4, 0, 0, -4, 8,
                                                 -10, -25, -4, -4, -25, -10,
                                                 100, -10, 8, 8, -10, 100]
            elif self.size >= 8: # On pourrait tout faire en une ligne, mais ça nuierait à la compréhension; la vitesse d'execution serait plus rapide
                line_1 = [100, -10, 8]+[6]*((self.size-6)/2); line_1 += line_1[::-1]
                line_2 = [-10, -25, -4]+[-4]*((self.size-6)/2); line_2 += line_2[::-1]
                line_3 = [8, -4, 6]+[4]*((self.size-6)/2); line_3 += line_3[::-1]
                line_middle = [6, -4, 4]+[0]*((self.size-6)/2); line_middle += line_middle[::-1]; line_middle += line_middle*((self.size-8)/2)
                Board_Reversi.POSITION_WEIGHT = line_1 + line_2 + line_3 + line_middle; Board_Reversi.POSITION_WEIGHT += Board_Reversi.POSITION_WEIGHT[::-1]
            # -- Fin de la section pour l'AI --
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
        if board: # Minimax algorithm
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
                    while user_choice.upper() not in pos:
                        print "\nJouez une position legale!"
                        print Board_Reversi()
                        user_choice = raw_input("\nQuelle position souhaitez-vous jouer? (ColonneLigne) ")
                    print "\n{} joue en {}!".format(player, user_choice.upper())
                    player.play(user_choice[0].upper(), user_choice[1:], player.disk, True)
                self.change_turn()
                self.turn_n += 1
            else:
                print "\n{}, c'est ton tour! ({})".format(player, player.disk)
                user_choice = raw_input("\nQuelle position souhaitez-vous jouer? ")
                while user_choice.upper() not in pos:
                    print "\nJouez une position legale!"
                    print Board_Reversi()
                    user_choice = raw_input("\nQuelle position souhaitez-vous jouer? (ColonneLigne) ")
                print "\n{} joue en {}!".format(player, user_choice.upper())
                player.play(user_choice[0].upper(), user_choice[1:], player.disk, True)
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

    def play(self, column, row, disk, swap=False, board=None): # (Board is not None) seulement w/ Minimax
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
                if not board: # On change le tour si on utlise pas Minimax
                    self.change_turn()
            else:
                return True # Dans cette direction, un emplacement est donc disponible
        if board and swap: # Pour minimax uniquement, on renvoie l'etat du plateau actuel seulement lorsque l'on change les pieces
            return board
        return False # Dans toutes directions, il n'y a aucun enplacement
        
    def evaluation(self, ennemy, board, depth):
        """Renvoie un int correspondant au score du plateau du joueur"""
        CORNER = ["A1", chr(ord("A")+Board_Reversi().size-1)+"1", "A"+str(Board_Reversi().size), chr(ord("A")+Board_Reversi().size-1)+str(Board_Reversi().size)]
        
        # Mobility
        player_mobi, ennemy_mobi = len(self.can_play(board)), len(ennemy.can_play(board))
        mobi = (100.*(player_mobi-ennemy_mobi))/(player_mobi+ennemy_mobi+1)

        # Poids du joueur : somme des points correspondant à l'emplacement des jetons
        # Frontier disk : Contribue à réduire la mobilité adverse
        player_f, ennemy_f = 0, 0
        weight = 0
        for pos in Board_Reversi.POS:
            if (type(pos) is str) and len(pos)>1:
                weight += Board_Reversi.POSITION_WEIGHT[Board_Reversi.POS[pos]] if self.spot(pos[0], pos[1:], board)==self.disk else -Board_Reversi.POSITION_WEIGHT[Board_Reversi.POS[pos]] if self.spot(pos[0], pos[1:], board)==ennemy.disk else 0
                for dc, dr in Board_Reversi.DIRECTIONS:
                    column, row = Board_Reversi.POS[pos[0]]+dc, int(pos[1:])+dr
                    if self.is_on_board(column, row) and self.spot(Board_Reversi.POS[column], str(row), board) == ".":
                        if self.spot(pos[0], pos[1:], board) == self.disk:
                            player_f += 1
                        else:
                            ennemy_f += 1
        frontier = (100.*(player_f-ennemy_f))/(player_f+ennemy_f+1)

        # Disk Differential
        player_disk, ennemy_disk = board.count(self.disk), board.count(ennemy.disk)
        diff = 100.*(player_disk-ennemy_disk)/(player_disk+ennemy_disk)

        # Parity
        # parity = -1 if (Board_Reversi().size**2-(player_disk+ennemy_disk))%2 == 0 else 1

        # Corner possesion
        if (board[Board_Reversi.POS[CORNER[0]]]==self.disk) or (board[Board_Reversi.POS[CORNER[1]]]==self.disk) or (board[Board_Reversi.POS[CORNER[2]]]==self.disk) or (board[Board_Reversi.POS[CORNER[3]]]==self.disk):
            corner_poss = 100
        else:
            corner_poss = 0
            
        # Stability
        player_stab, ennemy_stab = 0, 0
        for i in range(4):
            if board[Board_Reversi.POS[CORNER[i]]]==self.disk:
                pieces = list()
                for dc, dr in Board_Reversi.DIRECTIONS:
                    column, row = Board_Reversi.POS[CORNER[i][0]]+dc, int(CORNER[i][1:])+dr
                    while self.is_on_board(column, row) and self.spot(Board_Reversi.POS[column], str(row), board) == self.disk:
                        pieces.append(Board_Reversi.POS[column]+str(row))
                        column += dc
                        row += dr
                player_stab += len(set(pieces))
            if board[Board_Reversi.POS[CORNER[i]]]==ennemy.disk:
                pieces = list()
                for dc, dr in Board_Reversi.DIRECTIONS:
                    column, row = Board_Reversi.POS[CORNER[i][0]]+dc, int(CORNER[i][1:])+dr
                    while self.is_on_board(column, row) and self.spot(Board_Reversi.POS[column], str(row), board) == ennemy.disk:
                        pieces.append(Board_Reversi.POS[column]+str(row))
                        column += dc
                        row += dr
                ennemy_stab += len(set(pieces))
        stability = (100.*(player_stab-ennemy_stab))/(player_stab+ennemy_stab+1)

        # Total score
        time = board.count("X")+board.count("O")
        score = Board_Reversi.WEIGHT_TIME[time][0]*mobi + Board_Reversi.WEIGHT_TIME[time][1]*frontier + Board_Reversi.WEIGHT_TIME[time][2]*diff + Board_Reversi.WEIGHT_TIME[time][3]*weight + Board_Reversi.WEIGHT_TIME[time][4]*stability + Board_Reversi.WEIGHT_TIME[time][5]*corner_poss 
        return score
    
    def minimax(self, player, depth, is_maximizing_player, ennemy, board):
        """Minimax algorithm"""
        pos = player.can_play(board)
        if depth == 0 or not pos:
            return player.evaluation(ennemy, board, depth)
        if is_maximizing_player:
            best_score = -1e14 #-inf
            for c in pos:
                board_copy = player.play(c[0], c[1:], player.disk, True, deepcopy(board))
                score = self.minimax(ennemy, depth-1, False, player, board_copy)
                best_score = max(best_score, score)
        else: # Minimize
            best_score = 1e14 # inf
            for c in pos:
                board_copy = player.play(c[0], c[1:], player.disk, True, deepcopy(board))
                score = self.minimax(ennemy, depth-1, True, player, board_copy)
                best_score = min(best_score, score)
        return best_score


    def computer_pos(self, pos, ennemy):
        """Determine une position de jeu pour l'ordinateur"""
        best_score = -1e14 #-inf
        for c in pos:
            board_copy = self.play(c[0], c[1:], self.disk, True, deepcopy(Board_Reversi.board["grille"]))
            if self.turn_n <= ((Board_Reversi().size)**2-4)/3:
                score = self.minimax(ennemy, 3, True, self, board_copy) # Anticipe sur 3 tours
            elif self.turn_n <= 2*((Board_Reversi().size)**2-4)/3:
                score = self.minimax(ennemy, 4, True, self, board_copy) # Anticipe sur 4 tours
            else: 
                score = self.minimax(ennemy, 5, True, self, board_copy) # Anticipe sur 5 tours
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
