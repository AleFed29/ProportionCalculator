import cv2
import numpy as np


def threshold(img_name,keyval):
  #name of the new image
    name_split = str(img_name).split(".")
    begin = ""
    for n in range(len(name_split)-1):
        begin = begin + name_split[n]
    name = "." + begin + "_bianco_e_nero." + name_split[len(name_split)-1]
    #oldname_bianco_e_nero.format
    img = cv2.imread(img_name, 0) #0 grayscale, 1 coloured, -1 unchanged
    cv2.imshow("prov", img)
    mainname = begin.split('/')[2]

    if mainname == "SalvatorMundi":
        #black if color Average of RGB values < keyval else white
        ret, threshold_img = cv2.threshold(img, keyval, 255, cv2.THRESH_BINARY)
        threshold_img  = cv2.erode(threshold_img , None, iterations=1)

    elif mainname == "DamaConErmellino":
        ret, threshold_img = cv2.threshold(img, keyval, 255, cv2.THRESH_BINARY)
        threshold_img  = cv2.erode(threshold_img , None, iterations=2)

    elif mainname == "Gioconda":
        threshold_img = cv2.rectangle(img, (0,200), (100,600), (255,255,255), -1) #fill with a white rectangle to have good threshold
        threshold_img = cv2.rectangle(threshold_img, (0,200), (200,450), (255,255,255), -1) #fill with a white rectangle to have good threshold
        threshold_img = cv2.rectangle(threshold_img, (525,400), (680,450), (255,255,255), -1)
        threshold_img = cv2.rectangle(threshold_img, (0,600), (50,500), (255,255,255), -1)
        ret, threshold_img = cv2.threshold(threshold_img, keyval, 255, cv2.THRESH_BINARY)
        threshold_img = cv2.bitwise_not(threshold_img)
        #rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
        #threshold_img  = cv2.morphologyEx(threshold_img, cv2.MORPH_BLACKHAT, rectKernel)
        #threshold_img = cv2.bitwise_not(threshold_img)
        threshold_img  = cv2.erode(threshold_img , None, iterations=4)
    cv2.imshow(mainname,threshold_img)
    cv2.waitKey(0)
    result = cv2.imwrite(name, threshold_img)
    if result:
        print("File saved successfully.")
    else:
        print("Error in saving file.")
    cv2.destroyAllWindows()
    return name



#def erosion(img_name, xKernel, yKernel, iterations_number):
    name_split = img_name.split(".")
    name = name_split[0] + "_finito." + name_split[1]
    img = cv2.imread(img_name,0)
    #kernel = np.ones((xKernel, yKernel),np.uint8) non expedit
    erosion = cv2.erode(img,None,iterations = iterations_number)

    result = cv2.imwrite(name, erosion)
    if result:
        print("File saved successfully.")
    else:
        print("Error in saving file.")
    return name

def ThresholdedPictureName(img_name, keyval):
    #return erosion(threshold(img_name, keyval),xKernel, yKernel, iterations_number) 
    return threshold(img_name, keyval)