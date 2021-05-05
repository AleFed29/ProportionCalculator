import cv2 as cv
import numpy as np

def threshold(img_name,keyval):
    #name of the new image
    name_split = image_name.split(".")
    name = name_split[0] + "_bianco_e_nero." + name_split[1]
    #oldname_bianco_e_nero.format
    img = cv2.imread(img_name, 0)

    #black if color Average of RGB values < keyval else white
    ret, treshold = cv2.threshold(img, keyval, 255, cv2.THRESH_BINARY)
    
    #cv2.imshow('original', img)
    #cv2.imshow('B&W', threshold)
    #cv2.waitkey(0)
    #cv2.destroyAllWindows()
    result = cv2.imwrite(name, threshold)
    if result:
        print("File saved successfully.")
    else:
        print("Error in saving file.")
    return name


def erosion(img_name, xKernel, yKernel, iterations_number):
    name_split = image_name.split(".")
    name = name_split[0] + "_finito." + name_split[1]
    img = cv2.imread(img_name,0)
    kernel = np.ones((xKernel, yKernel),np.uint8)
    erosion = cv2.erode(img,kernel,iterations = iterations_number)

    result = cv2.imwrite(name, erosion)
    if result:
        print("File saved successfully.")
    else:
        print("Error in saving file.")
    return name


