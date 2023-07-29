# coding:utf-8
import sys
sys.path.append("/usr/local/lib/python3.7/site-packages")

from datetime import datetime
#import centreFinder
import server
import subprocess
import threading
import cv2
from time import perf_counter

def wait(wait_sec):
    until  = perf_counter() + wait_sec
    #print("start waiting")
    while perf_counter() < until:
        pass
    #print("%f sec wait" % wait_sec)


def takeImage():
    try:
        t = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
        filename = "/mnt/ramdisk/" + t + '_ceil.jpg'
        
        ceilCamera = cv2.VideoCapture(1)
        isSuccessed, frame = ceilCamera.read()
        
        if isSuccessed:
            subprocess.call("sudo rm /mnt/ramdisk/*.jpg",shell=True)
            cv2.imwrite(filename, frame)
            
        ceilCamera.release()
        return filename
    except Exception as e:
        print("Upload error")
        print(e)
        
def PRA_photo(StepNum,string):
    print(string)
    try:
        MyIPNum = server.get_myip_address().split('.')[3]
        imageFileName=str(MyIPNum)+"_"+str(StepNum)+ string
        filename = "/mnt/ramdisk/" + imageFileName + '.jpg'
        
        ceilCamera = cv2.VideoCapture(1)
        isSuccessed, frame = ceilCamera.read()
        
        if isSuccessed:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            subprocess.call("sudo rm /mnt/ramdisk/*.jpg",shell=True)
            cv2.imwrite(filename, frame)
            
        ceilCamera.release()
        
        #画像をサーバにアップロード    
        imageFile = open(filename, "rb")
        server.uploadImage(imageFile.read(), imageFileName)
        imageFile.close()
        wait(0.4)
        
    except Exception as e:
        print("Upload error")
        print(e)
        
def Ceil_Floor_TakeImage():
    myIP = server.get_myip_address()
    try:
        t = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
        Ceilfilename = "/mnt/ramdisk/" + t + '_ceil.jpg'
        Floorfilename = "/mnt/ramdisk/" + t + '_floor.jpg'
        
        ceilCamera = cv2.VideoCapture(1)
        #ceilCamera = cv2.VideoCapture("http://"+myIP+":8081/?action=snapshot")
        isSuccessed0, frame0 = ceilCamera.read()
        
        floorCamera = cv2.VideoCapture("http://"+myIP+":8080/?action=snapshot")
        isSuccessed1, frame1 = floorCamera.read()
        
        if isSuccessed0:
            subprocess.call("sudo rm /mnt/ramdisk/*.jpg",shell=True)
            cv2.imwrite(Ceilfilename, frame0)
            if isSuccessed1:
                cv2.imwrite(Floorfilename, frame1)
            
        ceilCamera.release()
        floorCamera.release()
        return Ceilfilename,Floorfilename
    except Exception as e:
        print("Upload error")
        print(e)

if __name__ == '__main__':
    
    #PRA_photo(0,"_test")
    Ceil_Floor_TakeImage()
