from random import randint

class Resource:
    num_resource = 0
    total_quantity = 0
    def __init__(self, x:int, y:int, quantity:int):
        self.x = x
        self.y = y
        self.quantity = quantity
        Resource.num_resource += 1
        Resource.total_quantity += quantity
    
    def collect(self):
        """
        Retourne la quantité de ressource collectée par une fourmi
        """
        quantity_recolted = randint(2,51)
        if quantity_recolted < self.quantity:
            self.quantity -= quantity_recolted
            Resource.total_quantity -= quantity_recolted
        else :
            quantity_recolted = self.quantity
            self.quantity -= quantity_recolted
            Resource.total_quantity -= quantity_recolted


        return quantity_recolted
