import tkinter
import cv2 as cv
from modules.proportion_calculator import *
from modules.image_transformer import *
from PIL import Image, ImageTk


END = 1

def table(frame, data):
    width, height = len(data), len(data[0])
    for i in range(height): 
        for j in range(width):
            #Entry = single line text box
            e = tkinter.Entry(frame, width=20, fg='blue', font=('Arial',16,'bold'))
            e.grid(row=j, column=i)
            e.insert(END, data[j][i])#data at the END of the previous data in the entry widget 
            

def createForm(img_name, width, height, XPOS, YPOS, data):
    img =  Image.open(str(img_name)) #not getting image with opencv because 
    #window initialization
    window = tkinter.Tk()
    #elements in the form title and image.
    nomi = img_name.split('/')
    nome = nomi[len(nomi)-1].split('.')[0]
    frame_for_label = tkinter.Frame(window, bg = "lightgray")
    frame_for_label.place(relx = 1/3, rely = 0, relwidth = 1/3,relheight = 1/8)
    label = tkinter.Label(window, text = nome, fg = "blue", font = ("Arial", 17))
    label.place(relx = width/3, rely =  height/10) #text img_name.split('.')[0] check how to do it

    frame = tkinter.Frame(window, bg = "white")
    #it is a rectangle positioned in (width/6, height/3) and
    #it's large width * 2/3 and high height*1/3
    frame.place(relx = 0, rely = 1/8, relwidth = 1,relheight = 3/4)
   
    
    
    #I will show the image here
    frame_for_image = tkinter.Frame(frame, bg='white')
    frame_for_image.place(relx = 1/3, rely = 0, relwidth = 1/3,relheight = 5/8)
    #code for the image     
    canvas = tkinter.Canvas(frame_for_image, width = 432, height = 700)      
    canvas.pack()
         
    img = ImageTk.PhotoImage(img)
    canvas.create_image(20,20, anchor=tkinter.NW, image=img)

    #I will insert the table here
    frame_for_table = tkinter.Frame(frame, bg='white')
    frame_for_table.place(relx = 0, rely = 3/4, relwidth = 1,relheight = 1/4)
    table(frame_for_table, data)
    
    
    #window: last settings
    window.title(img_name)
    window.geometry(str(width)+"x"+str(height)+"+"+str(XPOS)+"+"+str(YPOS))
    #activating windows
    window.mainloop()