# coding:utf-8
import centreFinder
import server
import motorDrive
import safeTwoMotor

count = 0

#サーバを検索
serverIPAddress = server.search()

_, speed, _, _, _, Height = server.getStatus(serverIPAddress)

try: #例外が発生するかもしれないが、実行したい処理。
    R,Th = centreFinder.getRTheta("", Height, serverIPAddress) #距離(pixel))と角度(degtheta)を取得
    count = 1
except: #例外発生時に行う処理
    randTranslateTime = 0.5
    th180 = 180.0
    Rot2 = th180 * 0.19 / 30.0 #度数(deg)から秒数への変換
    motorDrive.motorDriveReverseRotate(Rot2) #来た道の方向へ向く。左回転
    print("Rotate")
    safeTwoMotor.driveMotor(speed,speed,randTranslateTime)
    print("Return to before position")

if count == 1:
    #度数を秒数へ変換
    Th = Th *0.19 / 30.0

    print("距離[m]", R)

    #マーカー方向へ向く。
    motorDrive.motorDriveRotate(Th) #()のなかを適宜修正することでマーカー方向に向くようにする。
