import tk 
#import importlib
#importlib.import_module("image_transformer")
import cv2 as cv

END = 1

def table(frame, data):
    width, height = len(data), len(data[0])
    for i in range(height): 
        for j in range(width):
            #Entry = single line text box
            e = tk.Entry(frame, width=20, fg='blue', font=('Arial',16,'bold'))
            e.grid(row=i, column=j)
            e.insert(END, data[j][i])#data at the END of the previous data in the entry widget 
            

def createForm(img_name, width, height, XPOS, YPOS, data):
    #getting the image
    img = cv.imread(img_name, 0)

    #window initialization
    window = tk.Tk()
    #elements in the form title and image.

    label = tk.Label(window, text = img_name, fg = "blue", font = ("Arial", 17))
    label.place(width/5, height/5) #text img_name.split('.')[0] check how to do it

    frame = tk.Frame(window, bg = "white")
    #it is a rectangle positioned in (width/6, height/3) and
    #it's large width * 2/3 and high height*1/3
    frame.place(relx = 1/6, rely = 1/3, relwidth = 2/3,relheight = 1/3)

    #I will show the image here
    frame_for_image = tk.Frame(frame, bg='white')
    frame_for_image.place(relx = 1/6, rely = 1/3, relwidth = 1/3,relheight = 1/3)
    #code for the image     
    canvas = tk.Canvas(frame_for_image, width = 300, height = 300)      
    canvas.pack()      
    img = cv.imread(img_name,0) #PhotoImage(file = img_name)      
    canvas.create_image(20,20, anchor=tk.NW, image=img)    

    #I will insert the table here
    frame_for_table = tk.Frame(frame, bg='gray')
    frame_for_table.place(relx = 2/3, rely = 1/3, relwidth = 1/3,relheight = 1/3)
    table(frame_for_table, data)
    
    button = tk.Button(frame, text = "Execute Calculation", bg = "white", fg = "blue")
    #button.pack(side="left", relx = 1/12)
    button.place
    
    
    #window: last settings
    window.title(img_name)
    window.geometry(str(width)+"x"+str(height)+"+"+str(XPOS)+"+"+str(YPOS))
    #activating windows
    window.mainloop()
