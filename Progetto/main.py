import os
from modules.proportion_calculator import *
from modules.frontend_interface import *

Gioconda = "./assets/Gioconda.jpg"
SalvatorMundi = "./assets/SalvatorMundi.jpg"
DamaconErmellino = "./assets/DamaConErmellino.jpg"
width = 500
height = 500
XPOS = 200
YPOS = 100
data_fake = [
    ['id', 'Picture','Rectangles', 'Trapezoids', 'Cavalieri-Simpson(Parabolas)', 'error_R', 'error_T', 'eror_P', 'time_R','time_T','time_P', 'time-quality-ratio_R',
     'time-quality-ratio_T', 'time-quality-ratio_P'], #tuples with data
    [1, 'Gioconda', 0.055, 0.070, 0.089, 0.006, 0.03, 0.001, 0.04,0.02, 0.01, 0.09, 0.05, 0.06] #tuples with data
    ] 
#image transforming and collecting data
xkernel = 3
ykernel = 3
iterations_number = 5
data_SalvatorMundi = CreateTableData(SalvatorMundi, 20, xkernel, ykernel, iterations_number)
data_Gioconda = CreateTableData(Gioconda, 150, xkernel, ykernel, iterations_number)

data_DamaconErmellino = CreateTableData(DamaconErmellino, 5, xkernel, ykernel, iterations_number)

#def Process(img_name, width, height, XPOS, YPOS):
    #fill with functions from ProportionCalculator
#    return True

if __name__ == "__main__":
    createForm(Gioconda, width, height, XPOS, YPOS, data_fake)
    createForm(Gioconda, width, height, XPOS, YPOS, data_Gioconda) #then try to call data table creation in createForm, using less parameters
    createForm(SalvatorMundi, width, height, XPOS, YPOS, data_SalvatorMundi)
    createForm(DamaconErmellino, width, height, XPOS, YPOS, data_DamaconErmellino)
    #call threshold and erosion 
    #Process("Gioconda.jpg",width, height, XPOS, YPOS, data_fake)
    #Process("SalvatorMundi.jpg",width, height, XPOS, YPOS, data_fake)
    #Process("DamaConErmellino.jpg",width, height, XPOS, YPOS, data_fake)
    os.system("PAUSE")
