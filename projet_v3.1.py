# coding: utf-8
class Board_Reversi(object):
    """Plateau de jeu"""
    initialized = False
    size = 8
    def __init__(self):
        if not self.initialized:
            print "\nFormat du plateau choisit: {}x{}".format(self.size, self.size)
            Board_Reversi.board = {"d" : self.size, "grille": ['.']*(self.size**2)}
            Board_Reversi.POS = {column + str(row) : x+self.size*y for x, column in enumerate([chr(i) for i in range(ord("A"), ord("A")+27)][:self.size]) for y, row in enumerate(range(1,self.size+1))}
            Board_Reversi.POS.update({c : i for i,c in enumerate([chr(i) for i in range(ord("A"), ord("A")+27)][:self.size])}) # Colonne str -> int
            Board_Reversi.POS.update({i : c for i,c in enumerate([chr(i) for i in range(ord("A"), ord("A")+27)][:self.size])}) # Colonne int -> str
            Board_Reversi.DISK, Board_Reversi.ENNEMY_DISK = "XO", {"X" : "O", "O" : "X"}
            Board_Reversi.DIRECTIONS = [(x,y) for x in range(-1,2) for y in range(-1,2) if x or y]
            for pos, disk in zip([Board_Reversi.POS[key] for key in (Board_Reversi.POS[self.size/2 - 1] + str(self.size/2), Board_Reversi.POS[self.size/2] + str(self.size/2 + 1), Board_Reversi.POS[self.size/2 - 1] + str(self.size/2 + 1), Board_Reversi.POS[self.size/2] + str(self.size/2))], "OOXX"): # Positions initiales
                Board_Reversi.board["grille"][pos] = disk
            Board_Reversi.initialized = True
            
    def __str__(self):
        """Affiche l'etat du plateau de jeu"""
        return "    "+ " ".join([chr(i) for i in range(ord('A'), ord("A")+27)][:self.size]) + "\n" +"\n".join([(" "+str(row+1)+"  "+" ".join(self.board["grille"][i:i+self.size])) if row+1<10 else str(row+1)+"  "+" ".join(self.board["grille"][i:i+self.size]) for row, i in enumerate([n*self.size for n in range(self.size)])])

    def spot(self, column, row):
        """Retourne '.', 'O' ou 'X' en fonction de la piece sur l'emplacement"""
        return self.board["grille"][self.POS[column+row]]
    
    def is_on_board(self, column, row):
        """Retoune True si l'emplacement est le plateau, False sinon"""
        return (0<=column<=self.size-1 and 1<=row<=self.size) 

    @staticmethod
    def place(column, row, disk):
        """Place un disque ("O" ou "X") a l'emplacement"""
        Board_Reversi.board["grille"][Board_Reversi.POS[column+row]] = disk

class Game_Reversi(Board_Reversi):
    """Permet d'appliquer les regles du jeu"""
    turn, turn_n, count = "X", 1, 0 # Si count = 2, alors deux tours d'affilé personne n'a joue. La partie est fini

    def __init__(self, names):
        self.players = [Player_Reversi(disk, name) for name, disk in zip(names, Board_Reversi().DISK)]

    def change_turn(self):
        """Permet de savoir quel joueur va jouer"""
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"
    
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
                    print "\nC'est le tour de l'ordinateur."
                    c, r = player.computer_pos(pos, self.players[self.DISK.index(Board_Reversi.ENNEMY_DISK[self.turn])])
                    print "\nL'ordinateur joue en {}{}".format(c,r)
                    player.play(c,r, player.disk, True)
                else:
                    print "\n{}, c'est ton tour!".format(player)
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
                print "\n{}, c'est ton tour!".format(player)
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
        return False
    
class Player_Reversi(Game_Reversi):
    """Joueur"""
    def __init__(self, disk, name):
        self.disk, self.name = disk, name
    
    def __str__(self):
        return self.name
    
    def can_play(self):
        """Determine si un joueur a la possibilite de jouer ou non"""
        print [c+str(r) for c in [chr(i) for i in range(ord("A"), ord("A")+27)][:Board_Reversi().size] for r in range(1,Board_Reversi().size+1) if self.play(c, str(r), self.disk)]
        return [c+str(r) for c in [chr(i) for i in range(ord("A"), ord("A")+27)][:Board_Reversi().size] for r in range(1,Board_Reversi().size+1) if self.play(c, str(r), self.disk)]

    def play(self, column, row, disk, swap=False):
        """Determine si un coup est legal ou non"""
        if self.spot(column, row) is not ".": # L'emplacement est deja occupe
            return False
        for dc, dr in self.DIRECTIONS: # On se deplace dans une direction donnee et on verifie si on peut encercler
            c, r = self.POS[column] + dc, int(row) + dr
            amount = 0 # on verifie s'il y a un disque ennemi dans la direction
            while Board_Reversi().is_on_board(c, r) and self.spot(self.POS[c], str(r)) == self.ENNEMY_DISK[disk]:
                c += dc
                r += dr
                amount += 1
            if not Board_Reversi().is_on_board(c, r) or amount == 0 or not self.spot(self.POS[c], str(r)) == disk:
                continue # On ne peut pas enclercler car soit il n'y a pas de disque ennemi dans la direction ou ce n'est pas un de nos disque au bout
            if swap:
                c_swap, r_swap = self.POS[column], int(row)
                while (c_swap, r_swap) != (c,r):
                    self.place(self.POS[c_swap], str(r_swap), self.disk)
                    c_swap += dc
                    r_swap += dr
                self.change_turn()
            else:
                return True # Dans cette direction, un emplacement est donc disponible
        return False # Dans toutes directions, il n'y a aucun enplacement

    def computer_pos(self, pos, ennemy):
        """Determine une position de jeu pour l'ordinateur"""
        return pos[0][0], pos[0][1:]

def ask_number(question, low, high):
    """Ask for a number within a range."""
    res = None
    while res not in range(low,high+1):
        try:
            res = int(input(question))
        except:
            print "Entrez une reponse correcte."
    return res

def main():
    print "\t\t\t\t\tBienvenue sur Othello!"
    names = []
    user_choice_size = ask_number("""
                             Combien de lignes (ou colonnes) doit avoir le plateau ?
                             --> """, low = 4, high = 26)
    Board_Reversi.size = user_choice_size
    user_choice_gm = ask_number("""
                             Choissisez un mode de jeu (1 ou 2):
                             1.- Contre l'ordinateur
                             2.- 2 joueurs

                             --> """, low=1, high=2)
    if user_choice_gm == 1:
        name = [raw_input("Entrez le nom du joueur: ")]
        user_choice_c = ask_number("""
                                 Quelle couleur voulez-vous jouer (1 ou 2):
                                 1.- Noir
                                 2.- Blanc
                                 
                                 --> """, low=1, high=2)
        if user_choice_c == 1:
            names = name + ["L'ordinateur"]
        else:
            names = ["L'ordinateur"] + name
        
        print "\nPour jouer une position, saisissez les coordonnees sous la forme ColonneLigne (A4, B6, ...)"
        game = Game_Reversi(names)
        over = False
        while not over:
            over = game.game(True)
        print
        print Board_Reversi()
        p_1_point, p_2_point = Board_Reversi.board["grille"].count("X"), Board_Reversi.board["grille"].count("O")

        if "." in Board_Reversi.board["grille"]:
            if p_1_point > p_2_point:
                p_1_point += Board_Reversi.board["grille"].count(".")
            elif p_2_point > p_1_point:
                p_2_point += Board_Reversi.board["grille"].count(".")

        if p_1_point > p_2_point:
            print "{} gagne avec {} points, contre {} pour {} !".format(names[0], p_1_point, p_2_point, names[1])
        elif p_1_point < p_2_point:
            print "{} gagne avec {} points, contre {} pour {} !".format(names[1], p_2_point, p_1_point, names[0])
        else:
            print "EGALITE! Les deux joueurs ont 32 points!"
    
    else:
        for i in range(user_choice_gm):
            names.append(raw_input("Entrez le nom du joueur {}: ".format(i+1)))
        print 
        print "Pour jouer une position, saisissez les coordonnees sous la forme ColonneLigne (A4, B6, ...)"
        game = Game_Reversi(names)
        over = False
        while not over:
            over = game.game()
        print
        print Board_Reversi()
        p_1_point, p_2_point = Board_Reversi.board["grille"].count("X"), Board_Reversi.board["grille"].count("O")

        if "." in Board_Reversi.board["grille"]:
            if p_1_point > p_2_point:
                p_1_point += Board_Reversi.board["grille"].count(".")
            else:
                p_2_point += Board_Reversi.board["grille"].count(".")

        if p_1_point > p_2_point:
            print "{} gagne avec {} points, contre {} pour {} !".format(names[0], p_1_point, p_2_point, names[1])
        elif p_1_point < p_2_point:
            print "{} gagne avec {} points, contre {} pour {} !".format(names[1], p_2_point, p_1_point, names[0])
        else:
            print "EGALITE! Les deux joueurs ont 32 points!"

    print "La partie est termine! A bientot."

    

main()

try:
    input("\n\n<Appuyez sur Enter pour quitter.>")
except:
    pass
