import os
import cv2 as cv
import modules.image_transformer as transformer
from datetime import datetime

global KEYVAL
global xKERNEL
global yKERNEL
global ITERATIONS_NUMBER

#creates the image with the name composed by the methods, then it returns the name
def iswhite(pixelRGB):
    return(pixelRGB == 255)
    #return int(pixelRGB[0]) == 255 and int(pixelRGB[1]) == 255 and int(pixelRGB[2]) == 255

def isblack(pixelRGB):
    return pixelRGB == 0
    #return pixelRGB[0] == 0 and pixelRGB[1] == 0 and pixelRGB[2] == 0
   

def FunctionsFromArea(img_name, keyval):
    img = cv.imread(str(transformer.ThresholdedPictureName(img_name, keyval)), 0)
    # get dimensions of image
    dimensions = img.shape
    # height, width, number of channels in image
    height = dimensions[0]-1
    img_width = dimensions[1]-1 
    print(img_width,'x',height)
    dxfunc = DxFunc(img, ystart=height, width=img_width)
    sxfunc = SxFunc(img, ystart=height, width=img_width)
    return sxfunc, dxfunc

#immaginare l'immagine ruotata di 90 gradi verso sistra
def DxFunc(img, ystart, width):#function on the right
    function_dx = dict() #f
    xstart = int(width/2)
    x = abs(int(ystart)-1)
    lastvalue = 20
    while lastvalue > 1: #quando non trova punti bianchi, la figura è finita
        for i in range(int(width/2)):
            y = abs(xstart - i) #y parte da width/2 e scende, x fissa 
            xrel = int(abs(ystart-x)) #xrel parte da 1 e va avanti dopo ogni ciclo for
            yrel = abs(y + int(width/2))
            #print(xrel, yrel)
            #yrel,x eppure a quanto pare l'asse 0 è l'altezza
            if img[x,yrel] > 200: #coord pixel, se il pixel è bianco (non nero, per sfumature)
                break
        punti =  list(function_dx.keys())   
        y = 2 if y < 2 and len(punti) < (ystart*10/11) else y  #se almeno 500 punti e un pixel arriva ad uno, allora esce.      
        function_dx[xrel] = y #f(xrel) = y
        lastvalue = y #ordinata dell'ultimo pixel bianco trovato
        x = x - 1 #punto alla nuova x
        y = xstart #ritorna su   
    return function_dx    

#immaginare l'immagine ruotata di 90 gradi verso destra
def SxFunc(img, ystart, width):#function on the left
    function_sx = dict() #f
    #xstart = 0
    x = abs(int(ystart)) - 1 #metti for per spostare le x
    lastvalue = 20
    while lastvalue > 1: #quando non trova punti bianchi, la figura è finita
        for i in range(int(width/2)):
            #y = i #y parte da 0 e sale, x fissa 
            xrel =  int(abs(abs(x)-abs(ystart))) #xrel parte da 1 e va avanti dopo ogni ciclo for
            yrel = int(abs(width/2 - i)) #da width/2 a scendere, perché parti sempre dall'alto
            #pixel i,x -> punto xrel,yrel ma loro usano assi invertiti
            if img[x,i] > 200: #coord pixel, se il pixel è bianco (non nero, per sfumature)
                break    
        punti =  list(function_sx.keys()) 
        yrel = 2 if yrel < 2 and len(punti) < (ystart*10/11) else yrel  #se almeno (ystart*10/11) punti e un pixel arriva ad uno, allora esce. 
        function_sx[xrel] = yrel #f(xrel) = yrel
        lastvalue = yrel #ordinata dell'ultimo pixel bianco trovato
        x = x - 1
        #y = 0 #xstart   
    return function_sx

            
def GetValueFrom(x, dictionary):
    return dictionary[x] if x in dictionary else 0

#img_name = ThresholdedPictureName()
def Xs(start, end, n):
    h = (end - start)/n
    xs = list()
    for i in range(n+1):
        xs.append(start + i*h)
    return xs    

def Rectangles(f, start, end, n):
    sum = 0
    xs = Xs(start, end, n)
    for x in xs:
        y = GetValueFrom(int(x),f)
        sum = sum + y
    h = abs(end - start)/n
    errmax = derMax(f)*h*(end-start)/2
    return [h*sum, errmax]

def Trapezoids(f, start, end, n):
    sum = 0
    xs = Xs(start, end, n)
    i = 0
    h = abs(end - start)/n 
    for x in xs:
        if i == 0 or i == n:
            sum = sum + GetValueFrom(int(x),f)
        else:
            sum = sum + 2 * GetValueFrom(int(x),f)
        i = i + 1
    errmax = derIIMax(f) * h*h*(end-start)/12        
    return [h*sum/2, errmax]        

def Parabolas(f, start, end, n):
    sum = 0
    xs = Xs(start, end, n)
    i = 0
    h = abs(end - start)/n 
    for x in xs:
        if i == 0 or i == n:
            sum = sum + GetValueFrom(int(x),f)
        elif i % 2 == 0:
            sum = sum + 2 * GetValueFrom(int(x),f)
        else:
            sum = sum + 4 * GetValueFrom(int(x),f)
        i = i + 1
        errmax = derIVMax(f)*(h**4)*(end-start)/2880
    return [h*sum/3, errmax] 

def TestRectangles(f,err):
    data_keys = list(f.keys())
    kmin = data_keys[0]
    kmax = data_keys[len(data_keys)-1] #they are already ordered
    i = 1
    J2 = Rectangles(f, kmin, kmax, i)
    while True:
        J1 = Rectangles(f,kmin, kmax, 2*i)
        diff = abs(float(J1[0]) - float(J2[0]))
        if diff < err:
            return J1
        J2 = J1
        i = 2*i


def TestTrapezoids(f, err):
    data_keys = list(f.keys())
    kmin = data_keys[0]
    kmax = data_keys[len(data_keys)-1] #they are already ordered
    i = 1
    J2 = Trapezoids(f, kmin, kmax, i)
    while True:
        J1 = Trapezoids(f, kmin, kmax, 2*i)
        diff = abs(float(J1[0]) - float(J2[0]))/3
        if diff < err:
            return J1
        J2 = J1
        i = 2*i  

def TestParabolas(f,err):
    data_keys = list(f.keys())
    kmin = data_keys[0]
    kmax = data_keys[len(data_keys)-1] #they are already ordered
    i = 1 
    J2 = Parabolas(f, kmin, kmax, i)
    while True:
        J1 = Parabolas(f, kmin, kmax, 2*i)[0]
        diff = abs(float(J1[0]) - float(J2[0]))/15
        if diff < err:
            return J1
        J2 = J1
        i = 2*i  
           

def derMax(f):
    max = 0
    yprev = GetValueFrom(0,f) #f(0)
    for x in f:
        if x<1: continue
        ysucc = GetValueFrom(x,f) #f(1), f(2),...
        if yprev != 0 and ysucc != 0:
            yo = abs(ysucc - yprev) #|f'(x)|
            if max < yo:
                max = yo
        yprev = ysucc #f(0), #f(1),...
    return max

def derIIMax(f):
    max = 0
    yprev = GetValueFrom(1,f)#f(1), f(2), ...
    intprev = yprev - GetValueFrom(0,f) #f'(0)
    for x in f:
        if x < 2: continue
        ysucc = GetValueFrom(x,f) #f(2), f(3), ...
        if yprev != 0 and ysucc != 0:
            intsucc = ysucc - yprev #f'(1), #f'(2)
            yo = abs(intsucc - intprev) #|f''(0)|, |f''(1)|, ...
            if max < yo:
                max = yo
        else:
            yo = 0
        yprev = ysucc
        intprev = intsucc #f'(0), f'(1), ...
    return max

def derIVMax(f):
    ys = GetValueFrom(0,f) #y start
    ym = GetValueFrom(1,f) #y in the middle
    yf = GetValueFrom(2,f) #y at the end
    intIIprev = (yf-ym)-(ym - ys)  #f''(0)

    ys = ym
    ym = yf
    yf = GetValueFrom(3,f)
    intIIsucc = (yf-ym)-(ym - ys)  #f''(1) 
    
    intIVprev = intIIsucc - intIIprev #f'''(0)
    intIIprev = intIIsucc

    ys = ym
    ym = yf
    yf = GetValueFrom(4,f)
    intIIsucc = (yf-ym)-(ym - ys) #f''(2)

    intIVsucc = intIIsucc - intIIprev #f'''(1)
    max = abs(intIVsucc - intIVprev) #|f(IV)(0)|
    intIVprev = intIVsucc #f'''(1), f'''(2),...
    intIIprev = intIIsucc #f''(2), f''(3), ...
    precnum = 3 #calculate f''(3), f''(4),...
    for x in f:
        if x < precnum: continue
        ys = GetValueFrom(x,f) #y start
        ym = GetValueFrom(x+1,f) #y in the middle
        yf = GetValueFrom(x+2,f) #y at the end
        if ys != 0 and ym != 0 and yf != 0: continue
        intIIsucc = (yf-ym)-(ym - ys) #f''(3), f''(4),...
        intIVsucc = intIIsucc - intIIprev #f'''(2)
        yo = abs(intIVsucc - intIVprev)#|f(IV)(1)|
        if max < yo:
            max = yo
        intIIprev = intIIsucc
        intIVprev = intIVsucc
    return max

def CreateTableData(img_name,KEYVAL):
    FUNCTION_1, FUNCTION_2 = FunctionsFromArea(img_name, KEYVAL) #method to have the function
    
    img = cv.imread(img_name,1)
    # get dimensions of image
    dimensions = img.shape
    # height, width, number of channels in image
    #area = img.size
    area = dimensions[0]*dimensions[1]

    #start,end 1
    data_keys1 = list(FUNCTION_1.keys())
    kmin1 = data_keys1[0]
    kmax1 = data_keys1[len(data_keys1)-1]

        
    data_keys2 = list(FUNCTION_2.keys())
    kmin2 = data_keys2[0]
    kmax2 = data_keys2[len(data_keys2)-1]

    n_rectangles = 1000000
    n_trapezoids = int(n_rectangles/3)
    n_parabolas = int(n_trapezoids/5)


    #err = 0.01 #max error -> not possible to execute so.
    print("Inizio")
    time_s = datetime.now()
    #A1 = TestRectangles(FUNCTION_1,err) it requires a supercomputer, having an error < ...
    A1 = Rectangles(FUNCTION_1,kmin1, kmax1, n_rectangles) #it is the max possible. 
    #A2 = TestRectangles(FUNCTION_2,err) it requires a supercomputer, having an error < ...
    A2 = Rectangles(FUNCTION_2,kmin2, kmax2, n_rectangles)
    rectangles = [A1[0] + A2[0], (A1[1]+A2[1])/2]
    time_rect = (datetime.now() - time_s).microseconds/1000  #it takes a little time, i don't consider it

    #just in debug phase
    print("Rettangoli")
    print(rectangles[0]/area)
    print("errore", rectangles[1])
    print("tempo", time_rect)
    #just in debug phase

    time_s = datetime.now()
    #A1 = TestTrapezoids(FUNCTION_1,err) it requires a supercomputer, having an error < ...
    #A2 = TestTrapezoids(FUNCTION_2,err) it requires a supercomputer, having an error < ...

    A1 = Trapezoids(FUNCTION_1,kmin1, kmax1, n_trapezoids)
    A2 = Trapezoids(FUNCTION_2, kmin2, kmax2, n_trapezoids)
    trapezoids = [A1[0] + A2[0], (A1[1]+A2[1])/2]
    time_trap = (datetime.now() - time_s).microseconds/1000 #milliseconds, not microseconds
    
    print("Trapezi")
    print(trapezoids[0]/area)
    print("errore", trapezoids[1])
    print("tempo", time_trap)

    time_s = datetime.now()
    #A1 = TestParabolas(FUNCTION_1,err) it requires a supercomputer, having an error < ...
    #A2 = TestParabolas(FUNCTION_2,err) it requires a supercomputer, having an error < ...
    A1 = Parabolas(FUNCTION_1, kmin1, kmax1, n_parabolas)
    A2 = Parabolas(FUNCTION_2, kmin2, kmax2, n_parabolas)
    parabolas = [A1[0] + A2[0], (A1[1]+A2[1])/2]
    time_par = (datetime.now() - time_s).microseconds/1000

    print("Parabole")
    print(parabolas[0]/area)
    print("errore",parabolas[1])
    print("tempo", time_par)

    data = [
        ["N","Method Name", "Value", "err","proportion(%)", "time (ms)", "coeff.time-err"],
        [1, "Rectangles", rectangles[0], rectangles[1],round(rectangles[0]*100/area,2), time_rect, time_rect*rectangles[1]],
        [2, "Trapezoids",trapezoids[0], trapezoids[1],round(trapezoids[0]*100/area,2), time_trap, time_trap*trapezoids[1]],
        [3, "Parabolas",parabolas[0], parabolas[1],round(parabolas[0]*100/area,2), time_par, time_par*parabolas[1]]
    ]
    return data
    #it takes the function -> three methods, data collected with datetime

#the methods will return some data stored in a tuple with
#all data to add to a list, then the list will be passed to the main
#Finally, main will give the interface back, and i will call it from the site
