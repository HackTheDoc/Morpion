import tkinter as tk

class TicTacToe:
    """
    Classe représentant un jeu de Tic-Tac Toe.

    Attributs :
        _GRID_SIZE              : constante donnant la taille du plateau
        _APP_COLOR              : constante donnant la couleur de fond de l'application
        _CASE_COLOR             : constante donnant la couleur des cases
        _SYMBOL_COLOR           : constante donnant la couleur des symboles que vont jouer les joueurs
        _PLAYER                 : constante dictionnaire permettant de savoir quel symbol correspond à quel joueur
        _NUMBER_OF_CASE_TO_WIN  : constante donnant le nombre de cases alignées necessaire pour gagner
        root                    : fenetre tkinter de l'application
        boardFrame              : frame du plateau de jeu
        board                   : tableau contenant les cases du plateau
        currentPlayer           : donne le numero (str) du joueur qui doit jouer
        disabledCaseCounter     : nombre de cases désactivées (et donc jouées), max 9
    
    Méthodes :
        createBoard         : permet la création du plateau
        playOnCase          : permet à un joueur de jouer sur une case
        isWinner            : regarde s'il y a ou non un gagnant et si oui l'affiche
        run                 : lance l'application
    """

    _GRID_SIZE = 3
    _APP_COLOR = "#e6e6e6"
    _CASE_COLOR = "#404040"
    _SYMBOL_COLOR = "#f2f2f2"
    _PLAYER = {"1": "X", "2": "O"}
    _NUMBER_OF_CASE_TO_WIN = 3

    def __init__(self, title="Application", size="480x320", resizable=True) -> None:
        """Création et lancement de l'application et ses éléments"""

        # Configuration du root de l'application
        self.root = tk.Tk()
        self.root.title(title.title())
        self.root.geometry(size)
        self.root.resizable(resizable, resizable)
        self.root.configure(background= self._APP_COLOR)

        # Configuration de la frame et création du plateau
        self.boardFrame = tk.Frame(master= self.root, background= self._APP_COLOR)
        self.board = self.createBoard()

        ## Joueur qui joue actuellement (par défaut le joueur 1)
        self.currentPlayer = "1"
        ## Nombre de cases désactivé après avoir été jouée (max : 9)
        self.disabledCaseCounter = 0

        # Lancement de l'application
        self.run()
    

    def createBoard(self):
        """Creation du plateau (composee de boutons)"""

        # Creation d'un plateau vide
        board = [ [tk.Button]*self._GRID_SIZE for _ in range(self._GRID_SIZE) ]

        for r in range(self._GRID_SIZE): # pour chaque ligne (row)
            for c in range(self._GRID_SIZE): # pour chaque colonne (column)
                
                # Creation d'une case (sous forme de bouton)
                case = tk.Button(
                    master= self.boardFrame,
                    text= "",
                    relief= "sunken",
                    font= (None, 24),
                    background= self._CASE_COLOR,
                    disabledforeground= self._SYMBOL_COLOR,
                    command= lambda row=r, column=c: self.playOnCase(row, column),
                    width= 3,
                )
                
                # Assigne la case dans la grille
                board[r][c] = case

                # On définit où afficher la case
                case.grid(row=r+1, column=c+1, padx= 4, pady= 4)

        # retourne la grille pour pouvoir la modifier/reutiliser
        return board
    

    def playOnCase(self, row, column):
        """Affiche le coup sur une case de coordonnées données"""

        # On récupère la case concernée
        case = self.board[row][column]
        # et on la désactive
        case.configure(state= "disable")
        self.disabledCaseCounter += 1
    
        # On change la couleur de la case en fonction de quel joueur joue
        if self.currentPlayer == "1":
            # on affiche le coup du joueur 1
            case.configure(text= self._PLAYER["1"])
            # On regarde s'il y a un gagnant
            self.isWinner()
            # et on change le joueur qui joue
            self.currentPlayer = "2"

        elif self.currentPlayer == "2":
            # on affiche le coup du joueur 2
            case.configure(text= self._PLAYER["2"])
            # On regarde s'il y a un gagnant
            self.isWinner()
            # et on change le joueur qui joue
            self.currentPlayer = "1"
        

    def isWinner(self):
        """regarde si quelqu'un a gagner ou non"""

        def disableBoard():
            """Désactive tout le plateau"""

            # On désactive la grille (on NE peut PAS sélectionner une case)
            for row in range(self._GRID_SIZE):
                for column in range(self._GRID_SIZE):

                    # On récupère la case concernée
                    case = self.board[row][column]
                    
                    # On désactive la case
                    case.configure(state= "disable")

        def finalBox(text):
            """Fin du JEU : affichage du gagnant"""

            # Configuration de la fenetre du gagnant
            victoryWindow = tk.Toplevel(self.root)
            victoryWindow.geometry("240x160")
            victoryWindow.title("Tic-Tac Toe")
            victoryWindow.resizable(False, False)

            # Création des components de la fenetre
            ## message du vainqueur
            lbl = tk.Label(
                master= victoryWindow,
                text= text,
                font= (None, 16),
                relief= 'ridge',
                bd= 5,
                height= 2
            )
            ## bouton quitter
            btn = tk.Button(
                master= victoryWindow,
                text= "QUITTER",
                font= (None, 22),
                command= self.root.destroy
            )

            # Affichage des components
            lbl.pack(fill= 'both', expand= True, padx= 5, pady= 5)
            btn.pack(fill='both', expand=True, padx= 5, pady= 5)

        def verticalCheck():
            """regarde verticalement sur 4 cases vers le bas, à partir d'une case d'origine incluse"""
            
            flag = False

            for row in range(self._GRID_SIZE):
                win = True

                # On regarde toute les cases de la ligne
                for column in range(self._GRID_SIZE):
                    # Si le symbole de la case est différent de celui du joueur actuel
                    if self.board[row][column]["text"] != self._PLAYER[self.currentPlayer]:
                        win = False
                
                # Si il y a victoire si la ligne regardée
                if win:
                    flag = True
            
            return flag

        def horizontalCheck():
            """regarde horizontalement sur 4 cases vers la droite, à partir d'une case d'origine incluse"""
            flag = False

            for column in range(self._GRID_SIZE):
                win = True

                # On regarde toute les cases de la colonne
                for row in range(self._GRID_SIZE):
                    # Si le symbole de la case est différent de celui du joueur actuel
                    if self.board[row][column]["text"] != self._PLAYER[self.currentPlayer]:
                        win = False
                
                # Si il y a victoire si la ligne regardée
                if win:
                    flag = True
            
            return flag

        def diagonalsCheck():
            """regarde diagonalement sur 4 cases sur l'axe Nord-Ouest / Sud-Est, à partir d'une case d'origine incluse"""

            # PREMIER axe diagonale
            win = True
            for i in range(self._GRID_SIZE):
                # Si le symbole de la case est différent de celui du joueur actuel
                if self.board[i][i]["text"] != self._PLAYER[self.currentPlayer]:
                    win = False

            # DEUXIEME axe diagonale
            if not win:
                win = True
                for i in range(self._GRID_SIZE):
                    # Si le symbole de la case est différent de celui du joueur actuel
                    if self.board[i][ self._GRID_SIZE-1-i ]["text"] != self._PLAYER[self.currentPlayer]:
                        win = False

            # Il y a eu une victoire sur une des deux diagonales
                flag = True if win else False
            else:
                flag = True
            
                       
            return flag

        # On regarde sur les différents axes
        flagV = verticalCheck()
        flagH = horizontalCheck()
        flagD = diagonalsCheck()
        
        # Si il y a une victoire
        if True in (flagV, flagH, flagD):
            disableBoard()
            finalBox("Le gagnant est :\nJOUEUR " + self.currentPlayer)
        # si il n'y a aucun vainqueur :
        elif self.disabledCaseCounter == 9:
            finalBox("Il n'y a aucun\ngagnant !")
    

    def run(self):
        """Charge les elements de l'application avant de la lancer"""

        # Affichage du plateau
        self.boardFrame.grid(row=1, column=0, padx=8, pady=8)
        
        # Lance l'application
        self.root.mainloop()


# Creation de l'application
## Taille de la fenetre : 540x440
app = TicTacToe(title="Tic-Tac Toe", size="240x230", resizable=False)
