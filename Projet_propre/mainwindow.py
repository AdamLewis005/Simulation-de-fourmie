import tkinter as tk
import tkinter.filedialog
import sys
from simulation import Simulation
from ant import Ant
from nest import Nest
from pheromone import Pheromone
from draw import Draw
from resource import Resource
import tkinter.messagebox
class MainWindow:
    def __init__(self, simulation:Simulation):
        self.simulation = simulation
        self.root = tk.Tk()
        self.root.geometry(str(simulation.width)+"x"+str(simulation.height))
        self.root.resizable(width=False, height=False)
        self.root.title("Simulateur de Fourmilières")
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.menu = Menu(self.root,simulation,self.status_bar)
        self.canvas = Canvas(self.root, self.menu, self.status_bar, width=500, height=500)
        self.canvas.pack()
        self.start_button = tk.Button(self.root, text="Démarrer", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause)
        self.pause_button.pack(side=tk.LEFT, padx=10)
        self.reset_button = tk.Button(self.root, text="Réinitialiser", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=10)
        self.quit_button = tk.Button(self.root, text="Quitter", command=self.quit)
        self.quit_button.pack(side=tk.RIGHT, padx=10)

        self.canvas.bind("<Button-1>",self.canvas.draw)

    def start(self):
        # Lance la simulation
        self.go = 1
        self.simulation.run()
        self.status_bar.update(Ant.num_ants,Resource.num_resource)

    def pause(self):
        # Pause la simulation
        self.go = 0
        self.simulation.pause()

    def reset(self):
        # Réinitialise la simulation
        self.canvas.delete("all")
        self.status_bar.update(0,0)
        self.canvas.resource = []
        Nest.num_nest = 0
        Ant.num_ants = 0
        Pheromone.idp = 0
        Resource.num_resource = 0
        self.canvas.resource = []
        self.canvas.ants = []
        self.canvas.nests =[]

    def quit(self):
        """
        Boîte de dialogue du protocole de fermeture de la fenêtre principale
        """
        if tk.messagebox.askokcancel("Quitter", "Quitter le logiciel ?\n"):
            self.root.destroy()
            sys.exit(0)

    def mainloop(self):
        self.root.mainloop()

class Canvas(tk.Canvas):
    def __init__(self, parent, menu, status_bar, **kwargs):
        super().__init__(parent, **kwargs)
        self.status_bar = status_bar
        self.menu = menu
        self.resource = []
        self.ants = []
        self.nests =[]


    def draw(self,event):
        if self.menu.mode.get() == 1:
            pass

        elif self.menu.mode.get() == 2:
            nest = Nest(event.x,event.y,10)
            self.status_bar.update(Ant.num_ants,Resource.num_resource)
            self.draw_nest(nest)
            self.nests+=[nest]
            nest.update_nest_id(nest)

        elif self.menu.mode.get() == 3:
            res = Resource(event.x,event.y,100)
            self.status_bar.update(Ant.num_ants,Resource.num_resource)
            self.resource += [res]
            self.draw_resource(res)

    def draw_ant(self, ant:Ant):
        # Dessine une fourmi à la position donnée
        self.create_oval(ant.x,ant.y,ant.x+2,ant.y+2,tags="ant")
        self.status_bar.update(Ant.num_ants,Resource.num_resource)

    def draw_nest(self, nest):
        # Dessine un nid à la position donnée
        self.create_oval(nest.x-5,nest.y-5,nest.x+5,nest.y+5,fill = "#FF4500",outline = "#DF362D",tags ="nest")

    def draw_resource(self, resource):
        # Dessine une ressource à la position donnée
        self.create_oval(resource.x - 5,resource.y - 5,resource.x+5,resource.y+5,fill = "#2e8bc0",outline = "#145DA0",tags ="resource")
        self.status_bar.update(Ant.num_ants,Resource.num_resource)

    def draw_pheromone(self,pheromone):
        #dessine les pheromones selon leur type
        
        if pheromone.type == "searching" :
            self.create_rectangle(pheromone.x,pheromone.y,pheromone.x+1,pheromone.y+1,fill = '#2FF3E0',tags = ("pheromone","searching",pheromone.id_pheromone),outline = "")
        if pheromone.type == "collect" or pheromone.type =="return_holded_resources": #fourmis qui ramene de la nouriture au nid
            self.create_rectangle(pheromone.x,pheromone.y,pheromone.x+2,pheromone.y+2,fill = '#FADCD9',tags = ("pheromone","carrying",pheromone.id_pheromone),outline = "")

class StatusBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.num_ants_label = tk.Label(self, text="Fourmis : 0")
        self.num_ants_label.pack(side=tk.LEFT)
        self.num_resources_label = tk.Label(self, text="Ressources : 0")
        self.num_resources_label.pack(side=tk.LEFT)
        self.file_label = tk.Label(self,text="Fichier : Non enregistré")
        self.file_label.pack(side=tk.LEFT)

    def update(self, num_ants:int, num_resources:int):
        self.num_ants_label.config(text="Fourmis : {}".format(num_ants))
        self.num_resources_label.config(text="Ressources : {}".format(num_resources))

class Menu:
    def __init__(self, parent, simulation:Simulation, status_bar:StatusBar):
        self.parent = parent
        self.simulation = simulation
        self.menu_bar = tk.Menu(parent)
        parent.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Nouveau Monde",accelerator="CTRL+N", command=lambda:self.new())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Importer un monde",accelerator="CTRL+O", command=lambda:self.open())
        self.file_menu.add_command(label="Exporter le monde",accelerator="CTRL+S", command=lambda:self.save(status_bar)) #,state="disabled"
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quitter", command=self.quit)
        self.menu_bar.add_cascade(label="Fichier", menu=self.file_menu)
        parent.bind_all("<Control-n>", lambda x: self.new())
        parent.bind_all("<Control-o>", lambda x: self.import_file())
        parent.bind_all("<Control-s>", lambda x: self.export_file())

        self.mode = tk.IntVar(parent,1)
        self.mode_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.mode_menu.add_radiobutton(label="Mode normal",state="active",value=1,variable=self.mode,command=lambda:self.mode_normal())
        self.mode_menu.add_radiobutton(label="Mode pose de nid",value=2,variable=self.mode,command=lambda:self.mode_place_nest())
        self.mode_menu.add_radiobutton(label="Mode pose de ressource",value=3,variable=self.mode,command=lambda:self.mode_place_resource())
        self.menu_bar.add_cascade(label="Mode",menu=self.mode_menu)

    def getMode(self)->int:
        return self.mode

    def new(self):
        # Crée un nouveau monde
        Draw()

    def open(self):
        """
        Ouverture boîte dialogue choix fichier (Ouvrir)
        """
        coords_canv = []
        self.fileopened = tkinter.filedialog.askopenfilename(title="Ouvrir un fichier", filetypes=[('MAP files','.map')])
        if self.fileopened:
            self.simulation.canvas.delete("all")
            with open(self.fileopened,"r") as file:
                for ligne in file:
                    coords = ligne[1:-2].split(',') # Le slicing permet d'éliminer des caractères
                    # On recrée les différents points
                    self.simulation.canvas.create_line((coords[0], coords[1], coords[2], coords[3]),tags=("ligne"))
                    # On recharge les différents points à la liste de coords (pour povoir réenregistrer par la suite les modifs)
                    coords_canv += [(int(coords[0]),int(coords[1]),int(coords[2]),int(coords[3]))]
                file.close

    def save(self, status_bar:StatusBar):
        # Enregistre le monde actuelle
        self.file_name = tkinter.filedialog.asksaveasfilename(title="Enregistrer le monde sous ...", filetypes=[('Fichiers MAP','.map')])
        if self.file_name:
            with open(self.file_name,"w") as file:
                file.write("OK")
                file.close()
                self.saveas = "..."+str(self.file_name)[-25:]+""
                status_bar.file_label.config(text="Fichier : {}".format(self.saveas))


    def quit(self):
        """
        Boîte de dialogue du protocole de fermeture de la fenêtre principale
        """
        if tk.messagebox.askokcancel("Quitter", "Quitter le logiciel ?\n"):
            self.parent.destroy()
            sys.exit(0)

    def help(self):
        # Affiche l'aide
        pass

    def about(self):
        # Affiche des informations sur l'application
        pass

    def mode_normal(self):
        print("mode",self.mode.get())

    def mode_place_nest(self):
        print("mode",self.mode.get())

    def mode_place_resource(self):
        print("mode",self.mode.get())
