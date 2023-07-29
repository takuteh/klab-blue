import os
import sys
import server
#import urllib2
import cv2
import subprocess
from datetime import datetime
import threading

"""
def takeFloorImage(ipAddress):
    try:        
        response = urllib2.urlopen("http://"+ipAddress+":8080/?action=snapshot")
        t = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
        filename = t + '_floor.jpg'
        
        server.uploadFloorImage(response.read(), filename)
    except Exception as e:
        print("Upload error")
        print(e)
    
    #sendThread = threading.Timer(0.5, takeImageForever, (ipAddress,))
    #sendThread.start()
"""
def takeImage():
    try:
        t = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
        filename = "/mnt/ramdisk/" + t + '_floor.jpg'
        
        floorCamera = cv2.VideoCapture(0)
        isSuccessed, frame = floorCamera.read()
        
        if isSuccessed:
            subprocess.call("sudo rm /mnt/ramdisk/*.jpg",shell=True)
            cv2.imwrite(filename, frame)
            
        floorCamera.release()
        return filename
    except Exception as e:
        print("Upload error")
        print(e)
        

class FloorImage():
    
    __MyIP = server.get_myip_address()
    __ImageDir = "serverImage"
    FileName = ""
    
    def __init__(self) :
        if not os.path.exists(self.__ImageDir):
            os.makedirs(self.__ImageDir)
    
    def takeImage(self, Step):    
        self.FileName = str(Step)+"_floor.jpg"
        try:
            floorCamera = cv2.VideoCapture("http://"+self.__MyIP+":8080/?action=snapshot")
            isSucceed, frame = floorCamera.read()
            
            if isSucceed:
                
                cv2.imwrite(os.path.join(self.__ImageDir, self.FileName), frame)
                
        except Exception as e:
            print("takeImage error")
            print(e)
        
        floorCamera.release()
        return self.FileName
    
    def UploadImage(self, filename:str, Distance, Step, DegTheta):
        imageFile = open(os.path.join(self.__ImageDir, filename), "rb")
        imageFileName = str(round(Distance,1)).replace('.','-')+"_"+str(round(DegTheta,1)).replace('.','-')+"_"+str(Step+1)+"_"+self.__MyIP.split('.')[3] + "_floor.jpg"
        print(self.FileName)    
        server.uploadImage(imageFile.read(), imageFileName, "FloorImage")
        imageFile.close()
        #os.remove(os.path.join(self.__ImageDir, filename))


if __name__ == '__main__':
    
    floor = FloorImage()
    #print("Filename:"+floor.__FileName)
    floor.UploadImage(floor.takeImage(Step = 1), Distance = 1, Step = 1, DegTheta = 90)
    print("Filename:"+floor.FileName)
    #IPAddress = sys.argv[1]
    #takeImageForever(IPAddress)
