from mainwindow import MainWindow, StatusBar
from simulation import Simulation
from ant import Ant
from resource import Resource


ants = []
num_resource = 1
num_ants = 2

simu = Simulation(500,550,num_resource,num_ants)
main = MainWindow(simu)

Simulation.canvas = main.canvas
id = main.canvas.find_closest(0,0)

main.status_bar.update(Ant.num_ants, Resource.num_resource)
    
main.mainloop()