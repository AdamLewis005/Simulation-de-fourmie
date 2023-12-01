from ant import Ant
from nest import Nest
from resource import Resource
from pheromone import Pheromone
import tkinter.messagebox
class Simulation:
    canvas = None
    flag = 0
    ant = None
    id_ant = None
    num_resource = 1
    num_ants = 2
    number_resource_for_spawn_ant = 50

    def __init__(self, width:int, height:int, num_resources:int, num_ants:int):
        self.width = width
        self.height = height
        self.resources = []
        self.ants = []
        self.time = 25
        self.num_ants = num_ants
        self.num_resource = num_resources

    def step(self):
        # Exécute une itération de la simulation
        self.flag = 1
        i = 0
        
        for nest in self.canvas.nests:
            
            if self.number_resource_for_spawn_ant <= nest.resources:
                nest.pop_ant(1)
                self.canvas.draw_ant(nest.ants[-1])
                self.ants = self.canvas.find_withtag("ant")
                nest.resources -= self.number_resource_for_spawn_ant
            
            for ant in nest.ants:
                ant.move(self.ants[i],self.canvas)
                pheromone = Pheromone(ant)
                self.canvas.draw_pheromone(pheromone)
                pheromone.delete_pheromone(200,self.canvas)
                i+=1

        self.canvas.after(self.time,self.loop)

    def spawn_ants(self, nest):      
        nest.pop_ant(5)

        for ant in nest.ants:
            self.canvas.draw_ant(ant)
        self.ants = self.canvas.find_withtag("ant")


    def run(self):
        for nest in self.canvas.nests:
            self.spawn_ants(nest)
        self.step()

    def loop(self):
        if Resource.total_quantity == 0:
            self.flag = 0
            tkinter.messagebox.showinfo(title = "Fin de la simulation", message = "Plus aucune ressource disponible, la simulation est donc terminée.")
        if self.flag:
            self.step()

    def pause(self):
        self.flag = 0
