# coding:utf-8
import cv2
import numpy as np
import threading
import math

from numpy.lib.npyio import genfromtxt
import CeilCamera
import server

aruco = cv2.aruco #arucoライブラリ
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
#dictionatyは任意に変更
# 4X4_50の場合，41番マーカが最もロバストに取得できるような気がする
R=0
DegTheta=0
MyIPNum = server.get_myip_address().split('.')[3]

FourPt=""

def getRTheta(imageFileName = "", height = 0, StepNum = 0):
    if not imageFileName:
        #imageFileName = CeilCamera.takeImage()
        imageFileName, Floor = CeilCamera.Ceil_Floor_TakeImage()
    
    # Pi zero では cv2.VideoCapture(1) 周辺に不具合があるかもしれないので，
    # 一旦ファイルに保存した天井画像を読み込んで処理する
    image = cv2.imread(imageFileName) # read file

    
    
    #マーカを検出
    corners, ids, rejectedImgPoints = aruco.detectMarkers(image, dictionary) 
    aruco.drawDetectedMarkers(image, corners, ids, (0,255,0))

    #画像をサーバにアップロード
    #sendThread = threading.Thread(target=upload, args=(image, imageFileName,))
    #sendThread.start()

    ## debug 用 Print 出力    
    print('------------------')
    p = np.array(corners)
    num = int((p.size)/8)
    print('detect', num)
    print('------------------')

    # 以下の処理はARマーカが１つだけ検出されたときのみ実施する
    # ２つ以上検出された時は，画像上でマーカの位置を出力する処理はしない
    # 今回はどのidのARマーカでもよいから１つだけ検出されたときに処理するようにしているが，
    # 特定のIDのマーカに対してのみ処理するようにしてもよい．
    # ただし，その場合でも環境中に重複するidのマーカ存在しないように注意を払う必要あり．
    if num == 1:# もし検出数が１ならば～
        # AR marker の4隅の座標を配列に代入
        array = np.array(corners)

        # 配列修正
        posarray = array.reshape(4,2)
        global FourPt
        FourPt = ""
        for x in posarray:
            #global FourPt
            FourPt = FourPt + str(int(x[0])) + "_" + str(int(x[1])) + "_"
        print(FourPt)

        # 配列の中の４コーナーの平均をとる，すなわち，ARマーカのだいたい中心の座標(pixel)が得られる
        meanposarray = posarray.mean(0)
        [x,y] = posarray.mean(0)#x,yにARマーカ四隅の座標の平均値が入る
        print('AR center = ', x,y)
        
        # x,yは画像左上端を原点としているため中心原点へ変換し、カメラの座標に合わせる
        X = y - image.shape[0]/2.0
        Y = -x + image.shape[1]/2.0

        # 中心からの距離R[px], 角度Theta[rad]を算出
        global R
        R = np.sqrt(X ** 2 + Y ** 2)
        Theta = np.arctan2(Y, X)

        # -2π～2πから、0～360に変換
        global DegTheta
        DegTheta = Theta * 180 / math.pi
        DegTheta = DegTheta -360 * math.floor(DegTheta / 360)
        print('X[px], Y[px], R, Theta[rad], Theta[deg] = ', X,Y,R,Theta,DegTheta)
        
        if height != 0:
            # [px] -> [cm]
            print("ピクセル数")
            print(R)
            R = height * (6 * pow(10, -5) * pow(R, 2) + 0.0464 * R) / 10 / 1.8

    
    #画像をサーバにアップロード    
    sendThread = threading.Thread(target=upload, args=(image, imageFileName, StepNum, "CeilImage",))
    FloorThread = threading.Thread(target=upload, args=(cv2.imread(Floor), Floor, StepNum, "FloorImage",))
    sendThread.start()
    FloorThread.start()
    
    return R, DegTheta

def upload(image, fileName,StepNum,whereImage):
    cv2.imwrite(fileName, image)
    imageFile = open(fileName, "rb")
    imageFileName=str(round(R,1)).replace('.','-')+"_"+str(round(DegTheta,1)).replace('.','-')+"_"+str(StepNum+1)+"_"+MyIPNum
    Ceilname = str(StepNum + 1) + "_" + MyIPNum + "_" + FourPt + "_ceil.jpg"
    if "Ceil" in whereImage:
        #imageFileName = imageFileName + "_ceil.jpg"
        imageFileName = Ceilname
    elif "Floor" in whereImage:
        imageFileName = imageFileName + "_floor.jpg"
    print(imageFileName)
    
    server.uploadImage(imageFile.read(), imageFileName,whereImage)
    imageFile.close()

if __name__ == '__main__':
    getRTheta()


#print('This is :{}'.format(__name__))
