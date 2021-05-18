import os
import cv2 as cv
import modules.image_transformer as transformer
import datetime


global KEYVAL
global xKERNEL
global yKERNEL
global ITERATIONS_NUMBER

#creates the image with the name composed by the methods, then it returns the name
def iswhite(pixelRGB):
    return pixelRGB[0] == 255 and pixelRGB[1] == 255 and pixelRGB[2] == 255 

def isblack(pixelRGB):
    return pixelRGB[0] == 0 and pixelRGB[1] == 0 and pixelRGB[2] == 0
   

def FunctionsFromArea(img_name, keyval):
    img = cv.imread(str(transformer.ThresholdedPictureName(img_name, keyval)), 0)
    # get dimensions of image
    dimensions = img.shape
    # height, width, number of channels in image
    height = dimensions[0]
    img_width = dimensions[1]
    sxfunc = SxFunc(img, ystart=height, width=img_width)
    dxfunc = DxFunc(img, ystart=height, width=img_width)
    return sxfunc, dxfunc

def SxFunc(img, ystart, width): #function on the left
    function_sx = dict()
    while ystart > 0:
        xstart = int(width)
        color = img[xstart, ystart]
        while not iswhite(color):
            xstart = xstart-1
            color = img[xstart, ystart]
        function_sx[ystart] = xstart - int(width/2)  #ribaltato
        ystart = ystart - 1
        if xstart == int(width/2): break #se la figura è terminata, per dama con ermellino che ha impurezze sopra la testa 
    return function_sx    

def DxFunc(img, ystart, width): #function on the left
    function_dx = dict()
    while ystart > 0:
        xstart = int(width)
        color = img[xstart, ystart]
        while not isblack(color):
            xstart = xstart + 1
            color = img[xstart, ystart]
        function_dx[ystart] = int(width/2) - xstart #ribaltato
        ystart = ystart - 1
        if xstart == int(width/2): break #se la figura è terminata, per dama con ermellino che ha impurezze sopra la testa 
    return function_dx

def GetValueFrom(x, dictionary):
    return dictionary[x] if x in dictionary else None

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
        sum = sum + GetValueFrom(x,f)
    h = abs(end - start)/n
    errmax = derMax(f)*h*(end-start)/2
    return h*sum, errmax

def Trapezoids(f, start, end, n):
    sum = 0
    xs = Xs(start, end, n)
    i = 0
    h = abs(end - start)/n 
    for x in xs:
        if i == 0 or i == n:
            sum = sum + GetValueFrom(x,f)
        else:
            sum = sum + 2 * GetValueFrom(x,f)
        i = i + 1
    errmax = derIIMax(f) * h*h*(end-start)/12        
    return h*sum/2, errmax        

def Parabolas(f, start, end, n):
    sum = 0
    xs = Xs(start, end, n)
    i = 0
    h = abs(end - start)/n 
    for x in xs:
        if i == 0 or i == n:
            sum = sum + GetValueFrom(x,f)
        elif i % 2 == 0:
            sum = sum + 2 * GetValueFrom(x,f)
        else:
            sum = sum + 4 * GetValueFrom(x,f)
        i = i + 1
        errmax = derIVMax(f)*(h**4)*(end-start)/2880
    return h*sum/3, errmax 

def TestRectangles(f,err):
    kmin = f.keys()[0]
    kmax = f.keys()[len(f.keys())-1] #they are already ordered
    i = 1
    J2 = Rectangles(f, kmin, kmax, i)
    while True:
        J1 = Rectangles(f,kmin, kmax, 2*i)
        diff = abs(J1[0] - J2[0])/15
        if diff < err:
            return J1
        J2 = J1
        i = 2*i


def TestTrapezoids(f, err):
    kmin = f.keys()[0]
    kmax = f.keys()[len(f.keys())-1] #they are already ordered
    i = 1
    J2 = Trapezoids(f, kmin, kmax, i)
    while True:
        J1 = Trapezoids(f, kmin, kmax, 2*i)
        diff = abs(J1[0] - J2[0])/15
        if diff < err:
            return J1
        J2 = J1
        i = 2*i  

def TestParabolas(f,err):
    kmin = f.keys()[0]
    kmax = f.keys()[len(f.keys())-1] #they are already ordered
    i = 1 
    J2 = Parabolas(f, kmin, kmax, i)
    while True:
        J1 = Parabolas(f, kmin, kmax, 2*i)[0]
        diff = abs(J1[0] - J2[0])/15
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
        if yprev != None and ysucc != None:
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
        if yprev != None and ysucc != None:
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
    intIIprev = (yf-ym)-(ym - ys) if ys != None and ym != None and yf != None else 0 #f''(0)

    ys = ym
    ym = yf
    yf = GetValueFrom(3,f)
    intIIsucc = (yf-ym)-(ym - ys) if ys != None and ym != None and yf != None else 0 #f''(1) 
    
    intIVprev = intIIsucc - intIIprev #f'''(0)
    intIIprev = intIIsucc

    ys = ym
    ym = yf
    yf = GetValueFrom(4,f)
    intIIsucc = (yf-ym)-(ym - ys) if ys != None and ym != None and yf != None else 0 #f''(2)

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
        if ys != None and ym != None and yf != None: continue
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
    height = dimensions[0]
    width = dimensions[1]
    area = height*width

    err = 0.01
    time_s = datetime()
    A1 = TestRectangles(FUNCTION_1,err)
    A2 = TestRectangles(FUNCTION_2,err)
    rectangles = [A1[0] + A2[0], (A1[1]+A2[1])/2]
    time_rect = time_s - datetime() #it takes a little time, i don't consider it
    time_s = datetime()
    A1 = TestTrapezoids(FUNCTION_1,err)
    A2 = TestTrapezoids(FUNCTION_2,err)
    trapezoids = [A1[0] + A2[0], (A1[1]+A2[1])/2]
    time_trap = time_s - datetime()
    time_s = datetime()
    A1 = TestParabolas(FUNCTION_1,err)
    A2 = TestParabolas(FUNCTION_2,err)
    parabolas = [A1[0] + A2[0], (A1[1]+A2[1])/2]
    time_par = time_s - datetime() 
    return [
        ["N", "Value", "err","proportion(%)", "time", "coeff.time-err"],
        [1, rectangles[0], rectangles[1],round(rectangles[0]*100/area,2), time_rect, time_rect*rectangles[1]],
        [2, trapezoids[0], trapezoids[1],round(trapezoids[0]*100/area,2), time_trap, time_trap*trapezoids[1]],
        [3, parabolas[0], parabolas[1],round(parabolas[0]*100/area,2), time_par, time_par*parabolas[1]]
    ]
    #it takes the function -> three methods, data collected with datetime

#the methods will return some data stored in a tuple with
#all data to add to a list, then the list will be passed to the main
#Finally, main will give the interface back, and i will call it from the site
