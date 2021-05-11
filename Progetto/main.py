import os
from proportion_calculator import *
from frontend_interface import *

width = 500
height = 500
XPOS = 200
YPOS = 100
data_fake = [
    ['id', 'Picture','Rectangles', 'Trapezoids', 'Cavalieri-Simpson(Parabolas)', 'error_R', 'error_T', 'eror_P', 'time_R','time_T','time_P', 'time-quality-ratio_R',
     'time-quality-ratio_T', 'time-quality-ratio_P'], #tuples with data
    [1, 'Gioconda', 0.055, 0.070, 0.089, 0.006, 0.03, 0.001, 0.04,0.02, 0.01, 0.09, 0.05, 0.06] #tuples with data
    ]

def Process(img_name, width, height, XPOS, YPOS):
    #fill with functions from ProportionCalculator
    return true

if __name__ == "__main__":
    createForm("Gioconda.jpg", width, height, XPOS, YPOS, data_fake)
    #call threshold and erosion 
    #Process("Gioconda.jpg",width, height, XPOS, YPOS, data_fake)
    #Process("SalvatorMundi.jpg",width, height, XPOS, YPOS, data_fake)
    #Process("DamaConErmellino.jpg",width, height, XPOS, YPOS, data_fake)
    os.system("PAUSE")
