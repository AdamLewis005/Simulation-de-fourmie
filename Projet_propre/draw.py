import tkinter as tk
import tkinter.filedialog
import sys

class Draw:
    """
    Affichage d'une fenêtre permettant de créer des dessins
    """
    def __init__(self):
        """
        Initialisation de la fenêtre principale "Dessin"
        """
        self.root = tk.Tk()
        self.root.title("Dessiner un Monde")
        self.root.minsize(500,610)
        self.root.maxsize(500,610)
        
        self.create_menu()
        
        self.canv = tk.Canvas(self.root,width=500,height=550,relief="sunken",bd=5)
        self.frame = tk.Frame(self.root)
        self.labelStatut = tk.Label(self.frame,text="Non sauvé")
        
        self.coords_canv = []
        
        self.canv.pack()
        self.frame.pack(side="bottom",fill="x")
        self.labelStatut.pack(side="left")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def create_menu(self):
        """
        Création de la barre de menu
        """
        menuBar = tk.Menu(self.root)
        
        self.menuFile = tk.Menu(menuBar,tearoff=0)
        
        
        self.menuFile.add_command(label="Nouveau",accelerator="CTRL+N",command=lambda:self.erase())
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Ouvrir",accelerator="CTRL+O",command=lambda:self.openfile())
        self.menuFile.add_command(label="Sauver",state="disabled",accelerator="CTRL+S",command=lambda:self.savefile())
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Quitter",accelerator="CTRL+Q",command=lambda:self.on_closing())
        menuBar.add_cascade(label="Fichier",menu=self.menuFile)
        
        self.root.bind_all("<Control-n>", lambda x: self.erase())
        self.root.bind_all("<Control-o>", lambda x: self.openfile())
        self.root.bind_all("<Control-s>", lambda x: self.savefile())
        self.root.bind_all("<Control-q>", lambda x: self.on_closing())
        
        self.root.bind("<Button-1>",self.initPos)
        self.root.bind("<B1-Motion>", self.drawing)
        
        self.root.config(menu=menuBar)
        
    def initPos(self,event):
        """
        Récupération de la postion initiale du pointeur (Ctrl+Clique)
        """
        self.menuFile.entryconfigure(3,state="normal")
        self.labelStatut.config(text="Non sauvé")
        self.lastx = event.x
        self.lasty = event.y
        
    def drawing(self,event):
        """
        Dessine suivant les positions actuelle et initiale (Mouvement souris)
        """
        self.canv.create_line((self.lastx, self.lasty, event.x, event.y),tags=("ligne"))
        self.coords_canv += [(self.lastx,self.lasty,event.x,event.y)]
        self.initPos(event)
        
    def erase(self):
        """
        Efface tout le contenu du canvas de dessin (Nouveau)
        """
        self.canv.delete("all")
        self.labelStatut.config(text="Non sauvé")
        self.coords_canv = []
        self.menuFile.entryconfigure(3,state="disabled")
    
    def openfile(self):
        """
        Ouverture boîte dialogue choix fichier (Ouvrir)
        """
        self.coords_canv = []
        self.fileopened = tkinter.filedialog.askopenfilename(title="Ouvrir un fichier", filetypes=[('MAP files','.map')])
        if self.fileopened:
            self.erase()
            with open(self.fileopened,"r") as file:
                for ligne in file:
                    coords = ligne[1:-2].split(',') # Le slicing permet d'éliminer des caractères
                    # On recrée les différents points
                    self.canv.create_line((coords[0], coords[1], coords[2], coords[3]),tags=("ligne"))
                    # On recharge les différents points à la liste de coords (pour povoir réenregistrer par la suite les modifs)
                    self.coords_canv += [(int(coords[0]),int(coords[1]),int(coords[2]),int(coords[3]))]
                file.close
                self.labelStatut.config(text=self.fileopened)
        
    def savefile(self):
        """
        Ouverture boîte dialogue sauvegarde dessin (Sauver)
        """
        self.filesaved = tkinter.filedialog.asksaveasfilename(title="Enregistrer sous ...", filetypes=[('MAP files','.map')])
        if self.filesaved:
            with open(self.filesaved,"w") as file:
                for x in self.coords_canv:
                    file.write(str(x)+"\n")
                file.close()
                self.saveas = "Sauvegardé sous '"+str(self.filesaved)+"'"
                self.labelStatut.config(text=self.saveas)
        
    def on_closing(self):
        """
        Boîte de dialogue du protocole de fermeture de la fenêtre principale
        """
        if tk.messagebox.askokcancel("Quitter", "Quitter le logiciel ?\n Tout dessin non sauvé\n sera perdu !"):
            self.root.destroy()
        
        
        
        
if (__name__ == "__main__"):
    Draw()
    sys.exit(0)