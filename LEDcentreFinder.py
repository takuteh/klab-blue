# -*- coding: utf-8 -*-
import math
import cv2
import numpy as np

# --- Local ---
import setFileNameByTime
import centralRecognition
import calculation

# 距離推定
def getRTheta(fileName = "", height = 0):

  # 以下の画像がGRAYかどうか調べる必要あり
  img = centralRecognition.centralRecognition()

  # マーカの中心座標(Mx, My)を求める
  Mx, My = calculation.centerCoordinates(img)
  if Mx == 0 and My == 0:
    print('Distance can\'t be estimated.')
    return 0, 0
  print('Mx = ' + str(Mx) + ', My = ' + str(My))

  # 差分座標の算出
  diff_x, diff_y = calculation.diff(Mx, My)

  # 半径方向の差分座標
  r = np.power(np.power(diff_x,2) + np.power(diff_y,2),0.5)

  # f値の算出
  f = calculation.fNumber(r)

  # 天頂角の算出[rad]
  zenithAngle = np.arcsin(r/f)

  # 方位角の算出[rad]
  azimuthAngle = np.arcsin(diff_x/f)

  # ロボットの傾いている角度を代入[deg]
  t = 0

  # マーカの座標[m](x, y, z)の算出
  x = calculation.h*np.tan(zenithAngle)*np.cos(azimuthAngle)*np.cos(np.deg2rad(t))+calculation.h*np.sin(np.deg2rad(t))
  y = calculation.h*np.tan(zenithAngle)*np.sin(azimuthAngle)
  z = -calculation.h*np.tan(zenithAngle)*np.cos(azimuthAngle)*np.sin(np.deg2rad(t))+calculation.h*np.cos(np.deg2rad(t))

  distance = np.power((np.power(x,2)+np.power(y,2)),0.5)
  print(distance)
  theta = 0
  return distance, theta

if __name__ == "__main__":
  distance, theta = getRTheta()
  print('推定距離 : ' + str(distance) + '[cm]')