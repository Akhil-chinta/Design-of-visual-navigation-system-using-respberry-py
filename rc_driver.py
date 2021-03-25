import sys
import threading
import socketserver
import numpy as np
import cv2 as cv
import time
#from getkey import getkey, keys
import keyboard

# distance data measured by ultrasonic sensor
sensor_data = None


class SensorDataHandler(socketserver.BaseRequestHandler):

    data = " "
    data1 = "Welcome"

    def handle(self):
        global sensor_data
        
        while self.data:
            self.data = self.request.recv(1024)
            #sensor_data = round(float(self.data), 1)
            # print "{} sent:".format(self.client_address[0])
            self.request.sendall(self.data1.encode())
            print(self.data.decode())


class DriveDataHandler(socketserver.BaseRequestHandler):




    def handle(self):
        
        self.send_inst = True
        
        while (self.send_inst):
            #self.key = getkey()
            self.key=keyboard.read_key()
            if self.key == "up":
                self.data='u'
                print("u")
            if self.key == "down":
                self.data='d'
            if self.key == "right":
                self.data='r'
            if self.key == "left":
                self.data='l'
            if self.key == 's':
                self.data='s'
            if self.key == 'q':
                break
            if self.key == 'a':
                self.data='a'
            if self.key == 'z':
                self.data='z'

            #self.data ='s'
            self.request.sendall(self.data.encode())
            time.sleep(0.5)



class Server(object):
    def __init__(self, host, port2, port3):
        self.host = host
        
        self.port2 = port2
        self.port3 = port3

    

    def sensor_stream(self, host, port):
        s = socketserver.TCPServer((host, port), SensorDataHandler)
        s.serve_forever()

    def drive_stream(self, host, port):
        s = socketserver.TCPServer((host, port), DriveDataHandler)
        s.serve_forever()

    def start(self):
        drive_thread = threading.Thread(target=self.drive_stream, args=(self.host, self.port3))
        sensor_thread = threading.Thread(target=self.sensor_stream, args=(self.host, self.port2))
        sensor_thread.daemon = True
        sensor_thread.start()
        #drive_thread.daemon = True
        drive_thread.start()
   




if __name__ == '__main__':
    h, p2, p3 = "192.168.43.22", 8002, 8004
    
    
    ts = Server(h, p2, p3)
    ts.start()
ts  .stop()
    
