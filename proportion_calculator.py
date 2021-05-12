import os
#import importlib
#importlib.import_module("image_transformer")
import image_transformer as transformer
import cv2 as cv

IMGNAME =""
KEYVAL = 0
xKERNEL = 0
yKERNEL = 0
ITERATIONS_NUMBER = 0 
FUNCTION_1, FUNCTION_2 = FunctionsFromArea(IMGNAME, KEYVAL, xKERNEL, yKERNEL, ITERATIONS_NUMBER) #method to have the function
#creates the image with the name composed by the methods, then it returns the name
def iswhite(pixelRGB):
    return pixelRGB[0] == 255 and pixelRGB[1] == 255 and pixelRGB[2] == 255 

def isblack(pixelRGB):
    return pixelRGB[0] == 0 and pixelRGB[1] == 0 and pixelRGB[2] == 0

def ThresholdedPictureName(img_name, keyval,xKernel, yKernel, iterations_number):
    return transformer.erosion(transformer.threshold(img_name, keyval),xKernel, yKernel, iterations_number)    

def FunctionsFromArea(img_name, keyval,xKernel, yKernel, iterations_number):
    img = cv.imread(ThresholdedPictureName(img_name, keyval,xKernel, yKernel, iterations_number))
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
        xstart = int(width/2)
        color = img[xstart, ystart]
        while not isblack(color):
            xstart = xstart-1
            color = img[xstart, ystart]
        function_sx[ystart] = int(width/2) - xstart #ribaltato
        ystart = ystart - 1
    return function_sx    

def DxFunc(img, ystart, width): #function on the left
    function_dx = dict()
    while ystart > 0:
        xstart = int(width/2)
        color = img[xstart, ystart]
        while not isblack(color):
            xstart = xstart + 1
            color = img[xstart, ystart]
        function_dx[ystart] = int(width/2) - xstart #ribaltato
        ystart = ystart - 1
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
def TestParabolas(img_name, err):
    i = 1 
    while True:
        J1 = Parabolas(img_name, 2*i)
        J2 = Parabolas(img_name, i)
        diff = abs(J1 - J2)/15
        if diff < err:
            return J1
        i = 2*i  


def Rectangles(f, start, end, n):
    sum = 0
    xs = Xs(start, end, n)
    for x in xs:
        sum = sum + f(x)
    h = abs(end - start)/n 
    return h*sum        
def Trapezoids(f, start, end, n):
    sum = 0
    xs = Xs(start, end, n)
    i = 0
    h = abs(end - start)/n 
    for x in xs:
        if i == 0 or i == n:
            sum = sum + f(x)
        else:
            sum = sum + 2 * f(x)
        i = i + 1    
    return h*sum/2        

def Parabolas(f, start, end, n):
    sum = 0
    xs = Xs(start, end, n)
    i = 0
    h = abs(end - start)/n 
    for x in xs:
        if i == 0 or i == n:
            sum = sum + f(x)
        elif i % 2 == 0:
            sum = sum + 2 * f(x)
        else:
            sum = sum + 4 * f(x)
        i = i + 1     
    return h*sum/3            



    
#the methods will return some data stored in a tuple with
#all data to add to a list, then the list will be passed to the main
#Finally, main will give the interface back, and i will call it from the site
