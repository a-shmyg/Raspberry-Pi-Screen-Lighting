import socket
import RPi.GPIO as GPIO
import sys, time
import pickle

#setup the led shit
GPIO.setmode(GPIO.BOARD)

red = 11
blue = 15
green = 13

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

g = GPIO.PWM(green, 100)
b = GPIO.PWM(blue, 100)
r = GPIO.PWM(red, 100)

#start em off at quarter brightness
r.start(0)
g.start(0)
b.start(25)

HOST = '192.168.1.126' #host
PORT = 8000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("made socket")

def rgbToDutyCycle(num):
        newDC = (num/255.0) * 100
        print(num)
        print(newDC)
        return int(newDC) #just for test


try:
        s.bind((HOST,PORT))
except socket.error as e:
        print("failed socket part")
        print(e)

s.listen(5)

while True:
        print("waiting for message")
        (conn,addr) = s.accept()
        print("connected")


        data = conn.recv(1024)
        print("got it chief")

        reply = ""

        if data == "hello":
                reply = "sup chief"

        else:
        #       b.ChangeDutyCycle(DC)

                tuple = pickle.loads(data)
                print(tuple)
                print(str(tuple[0]))

                redDC = rgbToDutyCycle(tuple[0])
                greenDC = rgbToDutyCycle(tuple[1])
                blueDC = rgbToDutyCycle(tuple[2])

                print(str(redDC)+" "+str(greenDC)+" "+str(blueDC))

                r.ChangeDutyCycle(redDC)
                g.ChangeDutyCycle(greenDC)
                b.ChangeDutyCycle(blueDC)

                reply = "these colours "+data

        conn.send(reply)
        conn.close()
        print("closed connection")
