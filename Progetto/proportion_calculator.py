import os
import image_transformer

#creates the image with the name composed by the methods, then it returns the name
def ThresholdedPictureName(img_name, keyval,xKernel, yKernel, iterations_number):
    return erosion(threshold(img_name, keyval),xKernel, yKernel, iterations_number)    

#img_name = ThresholdedPictureName()

#def Rectangles(img_name):
#def Trapezoids(img_name)
#def Parabolas(img_name):

#the methods will return some data stored in a tuple with
#all data to add to a list, then the list will be passed to the main
#Finally, main will give the interface back, and i will call it from the site
