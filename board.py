class Board_Reversi(object):
    """Plateau de jeu"""
    initialized = False
    def __init__(self, size=10):
        self.size = size
        if not self.initialized:
            self.board = {"d" : size, "grille": ['.']*(size**2)}
            self.POS = {column + str(row) : x+size*y for x, column in enumerate([chr(i) for i in range(ord("A"), ord("A")+27)][:size]) for y, row in enumerate(range(1,size+1))}
            self.POS.update({c : i for i,c in enumerate([chr(i) for i in range(ord("A"), ord("A")+27)][:size])}) # Colonne str -> int
            self.POS.update({i : c for i,c in enumerate([chr(i) for i in range(ord("A"), ord("A")+27)][:size])}) # Colonne int -> str
            self.DISK, self.ENNEMY_DISK = "XO", {"X" : "O", "O" : "X"}
            self.DIRECTIONS = [(x,y) for x in range(-1,2) for y in range(-1,2) if x or y]

            for pos, disk in zip([self.POS[key] for key in (self.POS[size/2 - 1] + str(size/2), self.POS[size/2] + str(size/2 + 1), self.POS[size/2 - 1] + str(size/2 + 1), self.POS[size/2] + str(size/2))], "OOXX"): # Positions initiales
                self.board["grille"][pos] = disk


    def __str__(self):
        """Affiche l'etat du plateau de jeu"""
        return "    "+ " ".join([chr(i) for i in range(ord('A'), ord("A")+27)][:self.size]) + "\n" +"\n".join([(" "+str(row+1)+"  "+" ".join(self.board["grille"][i:i+self.size])) if row+1<10 else str(row+1)+"  "+" ".join(self.board["grille"][i:i+self.size]) for row, i in enumerate([n*self.size for n in range(self.size)])])

    def spot(self, column, row):
        """Retourne '.', 'O' ou 'X' en fonction de la piece sur l'emplacement"""
        return self.board["grille"][self.POS[column+row]]
    
    def is_on_board(self, column, row):
        """Retoune True si l'emplacement est le plateau, False sinon"""
        return (0<=column<=self.size-1 and 1<=row<=self.size) 

    def place(self, column, row, disk):
        """Place un disque ("O" ou "X") a l'emplacement"""
        self.board["grille"][self.POS[column+row]] = disk
