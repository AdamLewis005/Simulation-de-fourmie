from ant import Ant
from resource import Resource
class Nest:
    num_nest = 0
    def __init__(self, x:int, y:int, capacity:int):
        self.x = x
        self.y = y
        self.capacity = capacity
        self.resources = 0
        self.ants = []
        self.nest_id = 0
        Nest.num_nest += 1

    def add_ant(self, ant:Ant):
        # Ajoute une fourmi au nid
        self.ants += [ant]
        self.capacity -= 1

    def remove_ant(self, ant:Ant):
        # Retire une fourmi du nid
        self.ants.remove(ant)
        self.capacity += 1

    def store_resource(self, resource:int):
        # Stocke la ressource donnée dans le nid
        self.resources += resource

    def pop_ant(self, nb_ant:int):
        #spawn fourmis
        for x in range(nb_ant):
            self.add_ant(Ant(self.x,self.y,self.x,self.y,self.nest_id))

    def update_nest_id(self, nest_id):
        self.nest_id = nest_id