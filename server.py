# -*- coding: utf-8 -*-
import base64
import json
from types import ModuleType
import sys
sys.path.append("/home/pi/.local/lib/python3.7/site-packages")
import paho.mqtt.client as mqtt
import threading
import socket
from datetime import datetime
#from ssdpy import SSDPClient
import random
#import urllib3
import cv2
#import xml.etree.ElementTree as ET

global data
data={'IsExploring':False, 'Speed':2, 'Mue':1.0, 'Sigma':0.0, 'RThreshold':3.0, 'Height':2.0}

global ServerIP

def get_myip_address():
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

myip=get_myip_address()

def search():
    """
    client = SSDPClient()
    devices = client.m_search("urn:schemas-upnp-org:device:Basic:1")
        
    for device in devices:
        print(device.get("location"))
        try:
            http = urllib3.PoolManager()
            resp = http.request('GET',device.get("location"))
            #print(type(resp.data))#bytes
        
            xml = resp.data.decode('utf-8')
            #print(xml, type(xml))#str
            tree = ET.fromstring(xml)
            #print(type(tree))
            #print(tree.tag)
            if tree.findtext('.//{urn:schemas-upnp-org:device-1-0}friendlyName') == 'BLUE_Server':
                global ServerIP
                ServerIP=device.get("location")[7:]
                ServerIP = ServerIP[:ServerIP.find("/")]
                #print(ServerIP)
                return ServerIP              
                
        except Exception as e:
            print(e)
            """
    #return '192.168.1.105'#Klab_HEMS_2.4
    return '192.168.13.2'#Klab_HEMS_2.4mini
    #return '192.168.8.44'#Klab-1521

def initialize():

    #メッセージが届いたときの処理
    def on_message(client, userdata, msg):
        #msg.topicにトピック名がmsg.payloadに届いたデータ本体が入っている
        #Byte列をstringに変換し，それぞれのバラメータを代入
        if msg.topic =="BLUE/Status":
            global data
            data = json.loads(msg.payload.decode("ascii"))
            print(getStatus())

    #サーバに接続できた時の処理（MQTT）
    def on_connect(client, userdata, flag, rc):
        #接続できた旨表示
        print("connected OK.")
        #管理システム側への通知
        client.publish("BLUE/"+myip+"/connect","connect BLUE "+myip,0,True)
        #パラメータの変更に対するトピックをsubする
        client.subscribe("BLUE/Status",qos=1)

    #サーバが切断したときの処理（MQTT）
    def on_disconnect(client, userdata, flag, rc=-1):
        if rc != 0:
            print("Unexpected disconnection.")
            global data
            data['IsExploring']=False
    
    global client
    client = mqtt.Client("BLUE(" + myip + ")") #クラスのインスタンスの作成。()の中身はクライアントネームで自分のIPアドレスとした。

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.will_set("BLUE/"+myip+"/disconnect", "disconnect BLUE " + myip, 0, True);
    
    try:
        client.connect("192.168.1.105", 1883, 60)#Klab_HEMS_2.4
        #client.connect("192.168.13.2", 1883, 60)#Klab_HEMS_2.4mini
        #client.connect("192.168.8.44", 1883, 60)#Klab-1521
    except:
        print("connection failed")
    
    threading.Thread(target = client.loop_forever).start()

def getStatus():

    return(data['IsExploring'], data['Speed'], data['Mue'], data['Sigma'] ,data['RThreshold'] ,data['Height'])

def uploadImage(imageData, filename, whereImage):
    #引数の型：binary, string サーバに画像をアップロードする関数
    try: 
        #dict -> json形式にする
        Image_dict = {filename:base64.b64encode(imageData).decode('utf-8')}
        Image_json = json.dumps(Image_dict)
        
        client.publish("BLUE/" + myip + "/"+whereImage, Image_json, 0)
        #client.publish("BLUE/" + myip + "/"+whereImage+"/filename",filename, 0)
        #client.publish("BLUE/" + myip + "/"+whereImage+"/imageData",imageData, 0)
        print("send filename and imageData")

    except Exception as e:
        print("Upload error(" + whereImage + ")")
        print(e)
        
def uploadDeviceData(Step, R, saitaku, kikyaku, boids):
    try:
        client.publish("BLUE/" + myip + "/DeviceData",str(Step) +" "+ str(R) +" "+str(saitaku) +" "+ str(kikyaku) +" "+str(boids) +" "+" BLUE "+myip , 0)
        print("upload DeviceData")
    
    except Exception as e:
        print("upload error(DeviceData)")
        print(e)
    
def uploadDetectR(R):
    try:
        client.publish("BLUE/" + myip + "/DetectedPosition", str(R)+" BLUE "+myip, 0, retain = False)
        print("upload Detected_R")
    
    except Exception as e:
        print("upload error(Detected_R)")
        print(e)

if __name__ == '__main__':
    print(search())