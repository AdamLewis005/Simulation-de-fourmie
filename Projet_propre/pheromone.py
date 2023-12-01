from ant import Ant


class Pheromone:
    idp = 0
    def __init__(self,ant:Ant):
        self.type = ant.state
        self.x = ant.x
        self.y = ant.y
        self.id_pheromone = Pheromone.idp 
        Pheromone.idp += 1 

    def delete_pheromone(self,nb_p_max:int,canvas):
        """ suprime les pherome pour quil y ai que nb_p_max pheromone par fourmis """
        if self.id_pheromone > nb_p_max*Ant.num_ants:
            id = canvas.find_withtag("pheromone")[0]
            canvas.delete(id)
        