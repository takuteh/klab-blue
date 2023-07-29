# coding:utf-8
import cv2 
#import sys
import numpy as np
 
aruco = cv2.aruco #arucoライブラリ
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
#dictionatyは任意に変更
# 4X4_50の場合，41番マーカが最もロバストに取得できるような気がする

def arReader(): 
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        #cap = cv2.VideoCapture(0) の部分＝ビデオキャプチャの開始 ＜＜番号注意＞＞/dev/video0 OR /dev/video1
        #while True:
        #ret, frame = cap.read() #ビデオキャプチャから画像を取得
        #frame = cv2.imread(1.png')
        #frame = cv2.imread('markers_in_room.jpg')
        #frame = cv2.imread('marker_on_ceil.jpg')
        #frame = cv2.resize(frame, (int(frame.shape[1]/3), int(frame.shape[0]/3)))

        
        #Height, Width = frame.shape[:2] #sizeを取得
        #frame = cv2.resize(frame,(Width,Height))
        corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary) #マーカを検出
        aruco.drawDetectedMarkers(frame, corners, ids, (0,255,0)) #検出したマーカに描画する
        #実装時は下記のimshowはコメントアウト
        #cv2.imwrite('out.png',frame)
        oframe = frame #cv2.resize(frame, (int(frame.shape[1]/3), int(frame.shape[0]/3)))
        cv2.imshow("drawDetectedMarkers", oframe) #マーカが描画された画像を表示
        #そして，検出座標を返り値として出す
        
        #もちろん，キーボード入力待ちも消す（Floor Inspectingシステムにキーボードはない）
        cv2.waitKey(1) #キーボード入力の受付
        print(rejectedImgPoints)
        print('------------------')
        print(corners)
        print('------------------')
        print(ids)
        print('------------------')

        p = np.array(corners)
        num = int((p.size)/8)
        print('detect', num)
        print('------------------')
        if num == 1:
            array = np.array(corners)
            #print(array)
            #print(array.mean(1))
            posarray = array.reshape(4,2)
            # print(posarray)
            meanposarray = posarray.mean(0)
            [x,y] = posarray.mean(0)#x,yにARマーカ四隅の座標の平均値が入る
                
            # print(meanposarray)
            print(x,y)
            # print(y)
            # print(frame.shape[1]/2, frame.shape[0]/2)
            X = x - frame.shape[1]/2
            Y = -y + frame.shape[0]/2
            R = np.sqrt(X**2+Y**2)
            Theta = np.arctan2(Y, X)
            DegTheta = Theta*180/3.141593
            print(X,Y,R,Theta,DegTheta)
            center4corners = corners
 #   cap.release() #ビデオキャプチャのメモリ解放
    #下記も実装時は消す
    cv2.destroyAllWindows() #すべてのウィンドウを閉じる
    cap.release() #ビデオキャプチャのメモリ解放

arReader()