# -*- coding:utf-8 -*-
import picamera
import time
import cv2
import os

import calculation
import setFileNameByTime

# ----- importされた際に実行される -----
camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True
camera.resolution = (3280, 2464)
camera.shutter_speed = 100
time.sleep(2)
global mask
# !---- importされた際に実行される ----!

def centralRecognition():
  mask = 0
  for i in range(calculation.numOfImgTaken):

    # 撮影時の時刻をファイル名とする
    currentFileName = setFileNameByTime.setFileNameByTime() + '.jpg'

    # そのファイル名で撮像する
    camera.capture(currentFileName)

    # 1回目の撮像時は差分をとれない(2枚画像がない)ので2回目の撮像を行う
    if i == 0:

      # ファイル名の入れ替え
      beforeFileName = currentFileName
      continue

    # 前回の撮像した画像と今回撮像した画像を読み込む
    beforeImg = cv2.imread(filename = beforeFileName)
    currentImg = cv2.imread(filename = currentFileName)

    # 2枚ともRGBからGRAYに変換
    beforeImg = cv2.cvtColor(beforeImg, cv2.COLOR_BGR2GRAY)
    currentImg = cv2.cvtColor(currentImg, cv2.COLOR_BGR2GRAY)

    # 2枚のGRAY画像から差分をとる
    tmpMask = cv2.absdiff(beforeImg, currentImg)

    # ある閾値で2値化処理をする
    th = 100
    tmpMask[tmpMask < th] = 0
    tmpMask[tmpMask >= th] = 255

    # maskに差分結果を足していく
    mask += tmpMask
    os.remove(beforeFileName)
    # ファイル名の入れ替え
    beforeFileName = currentFileName

    if i == 4:
      os.remove(beforeFileName)
      mask[mask >= 255] = 255
      currentFileName = currentFileName.replace('.jpg', '')
      cv2.imwrite(str(currentFileName) + '-mask.jpg', mask)
      return mask