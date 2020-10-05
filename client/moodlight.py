 # -*- coding: utf-8 -*-

from PIL import ImageGrab
from colorthief import ColorThief
import time
import sys
import os
import socket
import pickle

#GLOBAL VARIABLES
i = 0
colorThresholds = {
    "r":[255,0,0],
    "g":[0,255,0],
    "lg":[148,252,3], #lightgreen
    "b":[0,0,255],
    "o":[252,186,3], #orange
    "c":[3,252,240], #cyan
    "p":[148,3,252], #purple
    "pi":[252,3,240], #pink
    "y":[252,248,3]
}

#HELPER FUNCTION
def setupScript():
    print("setting up")
    clearImages()
    i = 0

def clearImages():
    print("clearing images in dir")
    
    directory = os.listdir('.');
    print(directory)
    
    for image in directory:
        if image.endswith('.png'):
            os.remove(os.path.join('.', image))
            
def getColorValues(currentImageUrl):
    print("getting main color of image")
    colorThief = ColorThief(currentImageUrl)
    dominantColor = colorThief.get_color(quality=15)
    print(dominantColor)
    return dominantColor
    
def grabScreen():
    bbox = None
    im = ImageGrab.grab(bbox)
    im.save(str(i)+'.png');
    im.close()
    
    return str(i)+'.png' #return url of new image

def amplifyDomColor(colorTuple): #need to setup some thresholds, and also make into a list as tuples immutable
    colorTuple = list(colorTuple)
    maxHue = max(colorTuple)
    
    for i in range(3):
        if maxHue == colorTuple[i] and (maxHue > 50 and maxHue < 205):
            colorTuple[i] += 50
        if maxHue < 10:
            colorTuple = [3, 3, 3]
    print(str(colorTuple)+" with new hue")
    return colorTuple

#MAIN LOOP
    
setupScript()

#SERVER
HOST = '192.168.1.126' 
PORT = 8000 

while True:
    newImage = grabScreen()
    newColor = amplifyDomColor(getColorValues(newImage))
    
    serial = pickle.dumps(newColor, protocol=2)
    print(str(newColor[0])+ " red") #test it works right
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    
    s.sendall(serial)
    
    reply = s.recv(1024)
    if reply == 'Terminate':
        break
    
    print(reply)
    
    s.close()
   #time.sleep(0.5)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    