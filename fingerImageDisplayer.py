from turtle import resizemode
from unittest import registerResult
from xml.dom.minidom import Element
import cv2 as cv
import numpy as np
from enum import Enum
import random
import string
'''
def main():
    imgDisplayer = fingerImageDisplayer("Eng")
    
    correct = False;
    #num = int(input("Enter picture number: "))
    num = random.randint(0, 25)
    print("Number = " + str(num))

    img = imgDisplayer.getImage(num)
    resize = imgDisplayer.rescaleFrame(img, 2.0)
    imgDisplayer.displayImage(resize)
    cv.waitKey(0)

    detected = imgDisplayer.inputFromDetected()
    result = imgDisplayer.checkIfCorrectSign(detected, num)
    print(result)
'''

class fingerImageDisplayer(object):
    def __init__(self, lang, number):
        self.lang = lang
        self.number = number

    def getImage(self, num):
        img = cv.imread("LetterPictures/"+str(num)+".png")
        return img

    def displayImage(self,img):
        cv.imshow("HandImage", img)

    def destoryImage(self):
        cv.destroyWindow("HandImage")

    def rescaleFrame(self, frame, scale):
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
        dimensions = (width, height)

        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    def checkIfCorrectSign(self, detected):
        rounded = self.getRounded(detected)
        #print("Rounded = " + str(rounded))
        if rounded == self.number:
            return True
        else:
            return False

    def getRounded(self, detected):
        avg = sum(detected)/len(detected)
        rounded = round(avg)
        #print(rounded)
        return rounded

    def inputFromDetected(self):
        detected = []

        n = int(input("Enter number of elements : " ))
        for i in range(0,n):
            detectedNumber = int(input("Number "+str(i)+"= "))
            detected.append(detectedNumber)
        return detected

    def skipCurrent(self):
        self.destoryImage()
        self.number = random.randint(0, 25)
        img = self.getImage(self.number)
        resize = self.rescaleFrame(img, 2.0)
        self.displayImage(resize)
        
    
    def getWordInput(self):
        msg = input("Write a input: ")
        stripped = msg.strip()
        upper = stripped.upper()
        return upper


    def checkInputWithWord(self, inp, word, index):
        if(inp == string.ascii_uppercase.index(word.upper()[index])):
            return True
        else:
            return False 



#main()


