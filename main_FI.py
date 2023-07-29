# coding:utf-8
# 独自機能のインポート（おなじディレクトリにあること）
import CeilCamera
import centreFinder
#import LEDcentreFinder
import motorDrive
import safeTwoMotor
import server

# python 標準の機能のインポート
import random
import subprocess
from time import sleep
import math
import numpy as np
from scipy.stats import norm #正規分布


# 完全ランダムモード
def perfectRamdomAction():
    randTranslateTime = random.uniform(0.5,1)
    randRotateTime = random.uniform(0,2.5)
    motorDrive.motorDriveRotate(randRotateTime)
    safeTwoMotor.driveMotor(speed,speed,randTranslateTime)

#探査パラメータ------------------
norm1 = 0.0
norm2 = 0.0
#Boidsモデルで離れすぎたと認識する距離
r = 0.0 #確率の比
Ran = 0.0 #0~1の乱数
Rbe = 0.0 #直前までいた距離におけるR
R = 0.0
findCentre = True
Th = 0.0
N = 0
randTranslateTime = 1
back = 0
i = 0
kikyaku = 0
saitaku = 0
JudgeFlag=True

#探査パラメータここまで-------------

# 完全ランダムモード&撮像（天井・床）
def PRA_TakePhoto(N):
    CeilCamera.wait(0.2)
    randTranslateTime = random.uniform(0.5,1)
    randRotateTime = random.uniform(0,2.5)
    CeilCamera.PRA_photo(N,"_beforeRot")
    motorDrive.motorDriveRotate(randRotateTime)
    CeilCamera.PRA_photo(N,"_afterRot")
    safeTwoMotor.driveMotor(speed,speed,randTranslateTime)  
    


#サーバを初期化
server.initialize()

#探査開始
while True:
    #sleep(0.5)
    isExploring, speed, mue, sigma, R_Threshold, Height = server.getStatus()
    #床面魚眼カメラのBLUEは方向が逆のため
    speed = speed * (-1)
    #sleep(0.5)
    

    #100回になったら自動で停止
    if N == 100:
        N = 0
        while isExploring:
            isExploring,_,_,_,_,_ = server.getStatus()
            sleep(1)

    #完全ランダムモード
    if Height == -1 and isExploring:
        perfectRamdomAction()        
        N = N + 1
        server.uploadDeviceData(N, -2.0, 0, 0, 0)
        
        continue

    #完全ランダムモード+Photo
    if Height == -2 and isExploring:
        PRA_TakePhoto(N)        
        N = N + 1
        server.uploadDeviceData(N, -2.0, 0, 0, 0)
        
        continue
    
    if isExploring:
        #以後が行動アルゴリズム
        #フローは以下
        #1.旋回量と移動量を決めて旋回
        #2.ARマーカーの方向検出
        #3.距離情報からの確率の算出
        #4.確率的行動決定(ARマーカの方向・距離＆確率から決定)

        # 1.直進駆動時間と，旋回駆動時間を範囲付きrandomで生成し、旋回を行う。
        randTranslateTime = random.uniform(0.5,1) #短く設定すること。
        randRotateTime = random.uniform(0,2.5)

        if N > 0:
            motorDrive.motorDriveRotate(randRotateTime) #最初はexcept文の処理の旋回のみを行う。
        
        
        # 2.<<Find Leader>>
        try: #例外が発生するかもしれないが、実行したい処理。（ARマーカーなしの場合、例外が発生）
            sleep(0.5)
            R,Th = centreFinder.getRTheta("", Height,N) #距離(cm)と角度(deg)を取得
            #R,Th = LEDcentreFinder.getRTheta("", Height) #距離(cm)と角度(deg)を取得
            Rot1 = Th * 0.19 / 30.0 #分散中心方向への角度を秒数化
            sleep(2.5) 
            back = 0
        except: #例外発生時に行う処理（ARマーカーが見つからなかった)
            print("ARマーカーなし")
            findCentre = False
            if N == 0: #ARマーカがなければ最初だけ少しずつ回る。
                randRotateTime = 0.5
                motorDrive.motorDriveRotate(randRotateTime)
                continue #現在のwhile文を抜けて、次のwhile文を実行
            # マーカーを見失った場合の処理（一つ前の位置に戻る。）
            else:
                if back == 0:
                    #motorDrive.motorDriveReverseRotate(randRotateTime) #マーカ方向へむく。
                    safeTwoMotor.driveMotor(-speed,-speed,randTranslateTime) #回転させずに後方へ下がる。
                    back = 1
                    continue #現在のwhile文を抜けて、次のwhile文を実行

        if N == 0 :
            Rbe = R #最初のステップ時だけ例外処理

        #3.メトロポリス法を行うプログラム(確率的に採択・棄却を行う。)
        #正規分布の生成とパラメータ代入(xは距離)、x:定義域、loc:平均m、scale:標準偏差σ

        #norm1 = norm.pdf(mue,mue,sigma) #分散中心距離の確率(距離＝０)
        #norm2 = norm.pdf(R,mue,sigma) #現地点の距離における確率

        norm1 = norm.pdf(Rbe,mue,sigma) #一つ前の距離における確率
        norm2 = norm.pdf(R,mue,sigma) #現地点の距離における確率
        
        r = norm2 / norm1 #確率の比をとる。
        Ran = random.random() #0~1乱数生成

        if back == 1:
            r = 1
            R = 0

        Boids = 0 #Boidsカウンターの初期化

        #4.位置と3の確率値から確率的行動決定
        print('中心からの値は')
        print(R)
        
        if R < R_Threshold : #R_ThresholdはBoids距離,離れすぎていないかのチェックを最初にする。
            print("ランダム移動")
            print(Th)
            #採択される場合は下の条件分をスルーする。
            #棄却行動の条件(設定した分散密度の低い方向へ移動する場合は確率的に行動方向を棄却)
            if mue > 0: #ドーナツ型
                if ((90 <= Th < 270) and (R < mue)) or (((0 <= Th < 90) or (270 < Th <= 360))  and R > mue) and (r < Ran):
                    th90 = 90.0
                    Rot2 = th90 * 0.19 / 30.0 #度数から秒数への変換
                    kikyaku = kikyaku + 1
                    print("棄却")
                    print(kikyaku)
                    JudgeFlag = False
                    motorDrive.motorDriveRotate(Rot1 + Rot2) #光源方向に対して鉛直方向に移動する。
                else:
                    saitaku = saitaku + 1
                    print("採択")
                    print(saitaku)
                    JudgeFlag = True
            else: #ドーナツ型でない分散中心のみに集中する場合（mue = 0）
                if (90 <= Th < 270) and (r < Ran):
                        th90 = 90.0
                        Rot2 = th90 * 0.19 / 30.0 #度数から秒数への変換
                        kikyaku = kikyaku + 1
                        print("棄却")
                        print(kikyaku)
                        JudgeFlag = False
                        motorDrive.motorDriveRotate(Rot1 + Rot2) #光源方向に対して鉛直方向に移動する。
                else:
                    saitaku = saitaku + 1
                    print("採択")
                    print(saitaku)
                    JudgeFlag = True
        else: #Boidsモデルの接近処理
            print("マーカ方向へ向く")
            print(Th)
            motorDrive.motorDriveRotate(Rot1) #マーカ方向へむく。
            Boids = 1 #直進時の移動量を大きくするためのカウンター

        if Boids == 1:
            randTranslateTime = random.uniform(1,1.5) #長く設定すること。

        #障害物を検知するまで直進
        print("直進")
        if not safeTwoMotor.driveMotor(speed,speed,randTranslateTime):
            print("障害物検知")
            th90 = 100.0
            Rot2 = th90 * 0.19 / 30.0 #度数から秒数への変換

            # 障害物回避
            if 0<=Ran<0.5:
                motorDrive.motorDriveRotate(Rot2) #障害物に対して90度旋回(右)
                safeTwoMotor.driveMotor(speed,speed,randTranslateTime)
            else:
                motorDrive.motorDriveReverseRotate(Rot2) #左回転
                safeTwoMotor.driveMotor(speed,speed,randTranslateTime)
            # 回避中に障害物検知したら止まる。

        # integer increment
        Rbe = R #現在の距離の保存
        N = N + 1 #ステップ数
        
        #デバイスデータを送信        
        if findCentre == True :
            if Boids==1:
                server.uploadDeviceData(N,round(R,1),0,0,1)
            elif JudgeFlag == True:
                server.uploadDeviceData(N, round(R,1),1,0,Boids)
            else:
                server.uploadDeviceData(N, round(R,1),0,1,Boids)
        else :
            if Boids==1:
                    server.uploadDeviceData(N,-1,0,0,1)
            elif JudgeFlag == True:
                server.uploadDeviceData(N,-1,1,0,Boids)
            else:
                server.uploadDeviceData(N,-1,0,1,Boids)
            
            findCentre = True        
        
    else:
        # 探査しないときは一秒待つ
        sleep(1)
        N = 0
        #ステップ数Nを送信
        

