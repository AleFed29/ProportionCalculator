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
["N","Method Name", "Value", "err","proportion(%)", "time (ms)", "coeff.time-err"],
[1, "Rectangles", 60.5, 0.04,60, 325, 13],
[2, "Trapezoids",55.9, 0.01,56, 340, 3.4],
[3, "Parabolas",55.7, 0.005,55.9, 1000, 5]
]
    


if __name__ == "__main__":
    scelta = int(input("Inserire il quadro di cui si vuole avere la tabella: \n 1 - La Gioconda \n 2 - Salvator Mundi \n 3 - Dama con Ermellino\n Risposta: "))
    if scelta == 1: 
        data_Gioconda = CreateTableData(Gioconda, 90)
        createForm(Gioconda, width, height, XPOS, YPOS, data_Gioconda)
    elif scelta == 2: 
        data_SalvatorMundi = CreateTableData(SalvatorMundi, 20)
        createForm(SalvatorMundi, width, height, XPOS, YPOS, data_SalvatorMundi)
    elif scelta == 3:
        data_DamaconErmellino = CreateTableData(DamaconErmellino, 30)
        createForm(DamaconErmellino, width, height, XPOS, YPOS, data_DamaconErmellino)
    else:
        print("Digitazione errata Data fake")
        createForm(Gioconda, width, height, XPOS, YPOS, data_fake)
     #then try to call data table creation in createForm, using less parameters
    os.system("PAUSE")    
    #call threshold and erosion 
    #Process("Gioconda.jpg",width, height, XPOS, YPOS, data_fake)
    #Process("SalvatorMundi.jpg",width, height, XPOS, YPOS, data_fake)
    #Process("DamaConErmellino.jpg",width, height, XPOS, YPOS, data_fake)
    
