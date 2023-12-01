import random
import math
import tkinter as tk
from resource import Resource
class Ant:
    num_ants = 0
    def __init__(self, x_ant:int, y_ant:int, x_nest:int, y_nest:int, nest_id):
        self.x = x_ant
        self.y = y_ant
        self.nest = (x_nest,y_nest,nest_id)
        self.direction = random.randint(1,8) #1 :Haut #2 :Haut Droite #3 :Droite #4 :Bas Droite #5 :Bas #6 :Bas Gauche 7# :Gauche 8# :Haut Gauche
        self.distance_detection = 20
        self.state = "searching"
        self.number_steps = 1
        self.number_steps_before_random = random.randint(15,35)
        self.holded_resources = 0
        Ant.num_ants += 1


    def move(self,id:int, canvas:tk.Canvas):
        """
        Permet le deplacement de a fourmi avec en entre son ID et le canvas
        """
        # Déplace la fourmi dans sa direction actuelle
        canvas_height = canvas['height']
        canvas_width = canvas['width']

        ########################


        bool_detection_resource,x_resource,y_resource,resource_id = self.distance_ant_resource(id, canvas)

        if bool_detection_resource and self.holded_resources == 0:
            self.state = "collect"
            

        ######################

        #Verifie si la fourmi est en "searching" ou "colect"
        if self.state == "searching":

            # Verifie le nombre de pas pour le changement de direction
            if ((self.number_steps % self.number_steps_before_random) == 0):
                self.direction = random.randint(1,8)

            if (self.direction == 1 and ((self.y - 2) >= 0)):
                """
                Le pixel qui correspond à la fourmi se deplace de 1 vers le haut
                """
                old_x = self.x
                old_y = self.y
                self.y -= 1
                canvas.move(id,self.x - old_x, self.y - old_y)  # Soustraction des coords car déplacement de tant pixels et non positionnement à tel pixels
                self.number_steps += 1

            elif (self.direction == 2 and (((self.y - 2) >= 0) and ((self.x + 2) <= int(canvas_width)-1) )):
                """
                Le pixel qui correspond à la fourmi se deplace de 1 vers le haut puis de 1 vers la droite etc ...
                """
                old_x = self.x
                old_y = self.y
                self.y -= 1
                self.x += 1
                canvas.move(id,self.x - old_x, self.y - old_y)
                self.number_steps += 1

            elif ((self.direction) == 3 and ((self.x + 2) <= int(canvas_width)-1)) :
                """
                Le pixel qui correspond à la fourmi se deplace de 1 vers la droite
                """
                old_x = self.x
                old_y = self.y
                self.x += 1
                canvas.move(id,self.x - old_x, self.y - old_y)
                self.number_steps += 1

            elif (self.direction == 4 and ((self.y + 2) <= int(canvas_height)-1) and ((self.x + 2) <= int(canvas_width)-1)):
                """
                Le pixel qui correspond à la fourmi se deplace de 1 vers la droite puis de 1 vers le bas etc ...
                """
                old_x = self.x
                old_y = self.y
                self.y += 1
                self.x += 1
                canvas.move(id,self.x - old_x, self.y - old_y)
                self.number_steps += 1


            elif (self.direction == 5 and ((self.y + 2) <= int(canvas_height)-1)):
                """
                Le pixel qui correspond à la fourmi se deplace de 1 vers le bas
                """
                old_x = self.x
                old_y = self.y
                self.y += 1
                canvas.move(id,self.x - old_x, self.y - old_y)
                self.number_steps += 1

            elif (self.direction == 6 and ((self.y + 2) <= int(canvas_height)-1) and ((self.x - 2) >= 0)):
                """
                Le pixel qui correspond à la fourmi se deplace de 1 vers le bas puis de 1 vers la gauche etc ...
                """
                old_x = self.x
                old_y = self.y
                self.y += 1
                self.x -= 1
                canvas.move(id,self.x - old_x, self.y - old_y)
                self.number_steps += 1

            elif (self.direction == 7 and ((self.x - 2) >= 0)):
                """
                Le pixel qui correspond à la fourmi se deplace de 1 vers la gauche
                """
                old_x = self.x
                old_y = self.y
                self.x -= 1
                canvas.move(id,self.x - old_x, self.y - old_y)
                self.number_steps += 1

            elif (self.direction == 8 and ((self.y - 2) >= 0) and ((self.x - 2) >= 0)):
                """
                Le pixel qui correspond à la fourmi se deplace de 1 vers le bas puis de 1 vers la droite etc ...
                """
                old_x = self.x
                old_y = self.y
                self.y -= 1
                self.x -= 1
                canvas.move(id,self.x - old_x, self.y - old_y)
                self.number_steps += 1
            else:
                """
                Si la fourmi est bloqué contre un mur chage la direction
                """
                self.direction = random.randint(1,8)


        elif (self.state == "collect"):
            radius = 6
            # Calculer la distance entre le point fixe et le point qui bouge
            distance = math.sqrt((self.x - x_resource) ** 2 + (self.y - y_resource) ** 2)
            if distance <= radius:
                if resource_id.quantity > 0:
                    self.holded_resources = resource_id.collect()
                    self.state = "return_holded_resources"
                else:
                    self.state = "searching"
            else:
                old_x = self.x
                old_y = self.y

                # Calculer la différence entre les coordonnées des deux points
                diff_x = x_resource - self.x
                diff_y = y_resource - self.y
                if abs(diff_x) >= 1 :
                    if diff_x > 0 :
                        self.x +=1
                    else:
                        self.x -= 1


                if abs(diff_y) >= 1 :
                    if diff_y > 0 :
                        self.y += 1
                    else:
                        self.y -= 1
                
                #Ajout du deplacement au coords
                canvas.move(id,self.x - old_x, self.y - old_y)

        elif (self.state == "return_holded_resources"):
            radius = 6
            x_nest = self.nest[0]
            y_nest = self.nest[1]
            # Calculer la distance entre le point fixe et le point qui bouge            
            distance = math.sqrt((self.x - x_nest) ** 2 + (self.y - y_nest) ** 2)
            
            if distance <= radius:
                self.nest[2].store_resource(self.holded_resources)
                self.holded_resources = 0
                self.state = "searching"

            else:
                old_x = self.x
                old_y = self.y

                # Calculer la différence entre les coordonnées des deux points
                diff_x = x_nest - self.x
                diff_y = y_nest - self.y
                if abs(diff_x) >= 1 :
                    if diff_x > 0 :
                        self.x +=1
                    else:
                        self.x -= 1


                if abs(diff_y) >= 1 :
                    if diff_y > 0 :
                        self.y += 1
                    else:
                        self.y -= 1
                canvas.move(id,self.x - old_x, self.y - old_y)


        else:
            pass


    #New func
    def distance_ant_resource(self, id:int, canvas:tk.Canvas):
        """
        Fonction qui retourne un booleen pour savoir si oui ou non une fourmi peut detecter une resource
        grace a sa distance_detection
        """
        #Position des ressources
        i = 0
        l_res = canvas.find_withtag("resource")

        for res in canvas.resource:
            x_resource = res.x
            y_resource = res.y
            distance = math.sqrt((self.x - x_resource)**2 + (self.y - y_resource)**2)
            
            if distance <= self.distance_detection and res.quantity > 0:
                return True, x_resource, y_resource, res
            elif res.quantity == 0 :
                canvas.itemconfig(l_res[i], fill = "gray")
            i += 1
        return False , 0, 0, 0

    #New func
    def reconcile_points(self, x_resource, y_resource, x_ant, y_ant):
        """
        """
        # Distance maximale pour être dans le rayon
        radius = 10

        # Calculer la distance entre le point fixe et le point qui bouge
        distance = math.sqrt((x_ant - x_resource) ** 2 + (y_ant - y_resource) ** 2)

        # Calculer la différence entre les coordonnées des deux points
        diff_x = x_resource - x_ant
        diff_y = y_resource - y_ant

        # Calculer le rapport de la distance entre les deux points et la distance maximale pour être dans le rayon
        ratio = radius / distance

        # Ajuster les coordonnées du point qui bouge en fonction du rapport
        moving_x = diff_x * ratio
        moving_y = diff_y * ratio


        # Retourner les nouvelles coordonnées du point qui bouge
        return moving_x, moving_y
