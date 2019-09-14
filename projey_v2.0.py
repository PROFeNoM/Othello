# coding: utf-8
# Version 2.0: Risk Regions implemented to AI

class Board_Reversi(object):
    """Plateau de jeu"""
    board = {"d" : 8, "grille": ['.']*64}
    POS = {column + row : x+8*y for x, column in enumerate("ABCDEFGH") for y, row in enumerate("12345678")}
    DISK = "XO"
    ENNEMY_DISK = {"X" : "O", "O" : "X"}
    COLUMN_NUM = {c : i for i,c in enumerate("ABCDEFGH")}
    NUM_COLUMN = {i : c for i,c in enumerate("ABCDEFGH")}
    DIRECTIONS = [(x,y) for x in range(-1,2) for y in range(-1,2) if x or y]
    
    for pos, disk in zip([POS[key] for key in ("D4", "E5", "E4", "D5")], "OOXX"): # Positions initiales
        board["grille"][pos] = disk 

    def __str__(self):
        """Affiche l'etat du plateau de jeu"""
        return "    A B C D E F G H\n"+"\n".join(" "+str(row+1)+"  "+" ".join(self.board["grille"][i:i+8]) for row, i in enumerate([n*8 for n in range(8)]))

    def spot(self, column, row):
        """Retourne '.', 'O' ou 'X' en fonction de la piece sur l'emplacement"""
        return self.board["grille"][self.POS[column+row]]
    
    def is_on_board(self, column, row):
        """Retoune True si l'emplacement est le plateau, False sinon"""
        return (0<=column<=7 and 1<=row<=8) 

    def place(self, column, row, disk):
        """Place un disque ("O" ou "X") a l'emplacement"""
        self.board["grille"][self.POS[column+row]] = disk
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Game_Reversi(Board_Reversi):
    """Permet d'appliquer les regles du jeu"""
    turn = "X"
    turn_n = 1
    count = 0 # Si cette variable = 2, alors cela signifie que 2 tours d'affile personne n'a joue. La partie est fini
    def __init__(self, names):
        self.players = []
        for name, disk in zip(names, self.DISK):
            self.players.append(Player_Reversi(disk, name))

    def change_turn(self):
        """Permet de savoir quel joueur va jouer"""
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"

    def is_legal(self, column, row, disk):
        """Determine si un coup est legal ou non"""
        if self.spot(column, row) is not ".": # L'emplacement est deja occupe
            return False
        
        for dc, dr in self.DIRECTIONS:
            # On se deplace dans une direction donnee
            # On verifie si on peut encercler
            c, r = self.COLUMN_NUM[column] + dc, int(row) + dr
            amount = 0 # on verifie s'il y a un disque ennemi dans la direction
            while self.is_on_board(c, r) and self.spot(self.NUM_COLUMN[c], str(r)) == self.ENNEMY_DISK[disk]:
                c += dc
                r += dr
                amount += 1
            
            if not self.is_on_board(c, r) or amount == 0 or not self.spot(self.NUM_COLUMN[c], str(r)) == disk:
                # On ne peut pas enclercler car soit il n'y a pas de disque ennemi dans la direction ou ce n'est pas un de nos disque au bout
                continue
            
            return True # Dans cette direction, un emplacement est donc disponible
        return False # Dans toutes directions, il n'y a aucun enplacement

        
        # Sinon on joue la position qui retourne le plus de pîeces
    def game(self):
        """Deroulement de la partie en 1v1"""
        if self.count == 2 or not "." in Board_Reversi.board["grille"]:
            return True
        player = self.players[self.DISK.index(self.turn)]
        print "\n\t~~Tour {}~~\n\n".format(self.turn_n), Board_Reversi()
        print "\n(X: {} // O: {})".format(Board_Reversi.board["grille"].count("X"), Board_Reversi.board["grille"].count("O"))
        pos = player.can_play()
        if pos:
            self.count = 0
            print "\n{}, c'est ton tour!".format(player)
            user_choice = raw_input("\nQuelle position souhaitez-vous jouer? ")
            while user_choice.upper() not in pos:
                print "\nJouez une position legale!"
                print Board_Reversi()
                user_choice = raw_input("\nQuelle position souhaitez-vous jouer? (ColonneLigne) ")
            print "\n{} joue en {}!".format(player, user_choice.upper())
            player.play(user_choice[0].upper(), user_choice[1])
            self.change_turn()
            self.turn_n += 1
        else:
            self.count += 1
            self.change_turn()
            print "{} ne peut pas jouer de position legale.".format(player)
        return False

    def game_computer(self):
        """Deroulement de la partie contre l'ordinateur"""
        if self.count == 2 or not "." in Board_Reversi.board["grille"]:
            return True
        player = self.players[self.DISK.index(self.turn)]
        print "\n\t~~Tour {}~~\n\n".format(self.turn_n), Board_Reversi()
        print "\n(X: {} // O: {})".format(Board_Reversi.board["grille"].count("X"), Board_Reversi.board["grille"].count("O"))
        pos = player.can_play()
        if pos:
            self.count = 0
            if player.name == "L'ordinateur":
                print "\nC'est le tour de l'ordinateur."
                c, r = player.computer_pos(pos)
                print "\nL'ordinateur joue en {}{}".format(c,r)
                player.play(c,r)
            else:
                print "\n{}, c'est ton tour!".format(player)
                user_choice = raw_input("\nQuelle position souhaitez-vous jouer? ")
                while user_choice.upper() not in pos:
                    print "\nJouez une position legale!"
                    print Board_Reversi()
                    user_choice = raw_input("\nQuelle position souhaitez-vous jouer? (ColonneLigne) ")
                print "\n{} joue en {}!".format(player, user_choice.upper())
                player.play(user_choice[0].upper(), user_choice[1])
            self.change_turn()
            self.turn_n += 1
        else:
            self.count += 1
            self.change_turn()
            print "{} ne peut pas jouer de position legale.".format(player)
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Player_Reversi(Game_Reversi):
    """Joueur"""
    def __init__(self, disk, name):
        self.disk = disk
        self.name = name
    
    def __str__(self):
        return "{}".format(self.name)

    def play(self, column, row):
        """Joue un coup parmis ceux legaux, on retourne les disques"""
        if Board_Reversi().spot(column, row) is not ".": # L'emplacement est deja occupe
            return False      
        for dc, dr in Board_Reversi().DIRECTIONS:
            # On se deplace dans une direction donnee
            # On verifie si on peut encercler
            c, r = Board_Reversi().COLUMN_NUM[column] + dc, int(row) + dr
            amount = 0 # on verifie s'il y a un disque ennemi dans la direction
            while self.is_on_board(c, r) and Board_Reversi().spot(Board_Reversi().NUM_COLUMN[c], str(r)) == Board_Reversi().ENNEMY_DISK[self.disk]:
                c += dc
                r += dr
                amount += 1
            
            if not self.is_on_board(c, r) or amount == 0 or not Board_Reversi().spot(Board_Reversi().NUM_COLUMN[c], str(r)) == self.disk:
                # On ne peut pas enclercler car soit il n'y a pas de disque ennemi dans la direction ou ce n'est pas un de nos disque au bout
                continue

            # On peut alors retourner tous les disques dans cette direction 
            c_swap, r_swap = Board_Reversi().COLUMN_NUM[column], int(row)
            while (c_swap, r_swap) != (c,r):
                Board_Reversi().place(Board_Reversi().NUM_COLUMN[c_swap], str(r_swap), self.disk)
                c_swap += dc
                r_swap += dr
        self.change_turn()
        

    def can_play(self):
        """Determine si un joueur a la possibilite de jouer ou non"""
        places = list()
        
        for column in "ABCDEFGH":
            for row in "12345678":
                if self.is_legal(column, row, self.disk):
                    places.append(column+row)
        return places

    def best_pos(self, pos):
        best_point = int()
        for c,r in pos:
            board_duplicate = Board_Reversi.board["grille"][:]
            self.play(c, r)
            point = Board_Reversi.board["grille"].count(self.disk)
            if point > best_point:
                best_point, best_pos = point, c+r
            Board_Reversi.board["grille"] = board_duplicate[:]
        return best_pos

    def computer_pos(self, pos):
        """Determine une position de jeu pour l'ordinateur"""
        print pos
        # Area 1 : On prend les coins si possible
        for c, r in pos:
            if (c == "A" and r in "18") or (c == "H" and r == "18"):
                return c+r
        # Area 2
        area_2_pos = [c+r for c,r in pos if (c in "AH" and r in "3456") or (c in "CDEF" and r in "18")]
        print area_2_pos
        if area_2_pos:
            return self.best_pos(area_2_pos)
        # Area 3
        area_3_pos = [c+r for c,r in pos if (c in "CDEF" and r in "3456")]
        if area_3_pos:
            return self.best_pos(area_3_pos)
        # Area 4 
        area_4_pos = [c+r for c,r in pos if (c in "BG" and r in "3456") or (c in "CDEF" and r in "27")]
        if area_4_pos:
            return self.best_pos(area_4_pos)
        # Area 5 : Pire zone, donne acces aux coins
        return self.best_pos(pos)
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
            over = game.game_computer()
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