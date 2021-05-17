import cv2
import numpy as np


def threshold(img_name,keyval):
  #name of the new image
    name_split = img_name.split(".")
    name = name_split[0] + "_bianco_e_nero." + name_split[1]
    #oldname_bianco_e_nero.format
    img = cv2.imread(img_name, 0)
    
    cv2.imshow("prov", img)
    cv2.waitKey(0)
    #black if color Average of RGB values < keyval else white
    #treshold_img = cv2.threshold(img, keyval, 255, cv2.THRESH_BINARY)[1] #ret, threshold = ... 
    ret, threshold_img = cv2.threshold(img, keyval, 255, cv2.THRESH_BINARY)
    #treshold_img = np.array(cv2.threshold(img, keyval, 255, cv2.THRESH_BINARY)[1])
    
    #threshold_img = threshold_img
    cv2.imshow("Prova", threshold_img)
    cv2.waitkey(0)
    #cv2.imshow('original', img)
    #cv2.imshow('B&W', threshold)
    #cv2.waitkey(0)
    #cv2.destroyAllWindows()
    result = cv2.imwrite(name, threshold_img)
    if result:
        print("File saved successfully.")
    else:
        print("Error in saving file.")
    return name



def erosion(img_name, xKernel, yKernel, iterations_number):
    name_split = img_name.split(".")
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

def ThresholdedPictureName(img_name, keyval,xKernel, yKernel, iterations_number):
    return erosion(threshold(img_name, keyval),xKernel, yKernel, iterations_number) 