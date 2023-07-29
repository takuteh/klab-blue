import cv2
import numpy as np
# カメラの内部パラメータの定義
# fx = 675.508479333196
# fy = 674.936608139554
Cx = 1633.39414024524
Cy = 1218.19031757266

# 撮像回数
numOfImgTaken = 5

# 天井までの高さ
# h1[cm] : 床から天井まで
h1 = 142

# h2[cm] : 床からカメラまで
h2 = 2.2

# h [cm] : カメラから天井まで
h = h1 - h2

def centerCoordinates(mask):
  # 輪郭検出
  mask = cv2.medianBlur(mask, 5)
  ret,thresh = cv2.threshold(mask,127,255,0)
  contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

  #リストの中の１つ目の長方形を取得
  #リストには検出された長方形がcontours[i]に格納されているが１つしかないはずなのでその１つ目(インデックス番号的には0)を取得する

  # 検出されなかった場合
  if len(contours) == 0:
    return 0, 0
  a = contours[0]

  #x座標とy座標をそれぞれ抽出する.ただし, aはndarray
  x = a[:, :, 0]
  y = a[:, :, 1]

  #検出された長方形の中心座標を計算する
  X1 = (np.amax(x)).astype(np.float32)
  X2 = (np.amin(x)).astype(np.float32)
  Y1 = (np.amax(y)).astype(np.float32)
  Y2 = (np.amin(y)).astype(np.float32)
  Xo = ((X1 + X2) / np.float32(2)).astype(np.int32)
  Yo = ((Y1 + Y2) / np.float32(2)).astype(np.int32)
  return Xo, Yo
# !-- マーカの中心座標を求める --!

# 差分座標[pixel]を求める
def diff(x, y):
  x = abs(x - Cx)
  y = abs(y - Cy)
  return x, y

# 以下にf値の近似式の係数を記す
# y = a*x**6 + b*x**5 + c*x**4 + d*x**3 + e*x**2 + f*x + g
a = 3.6884E-14
b = -1.52853E-10
c = 2.57674E-07
d = -0.000225456
e = 0.107899161
f = -26.39607535
g = 3264.428615

def fNumber(x):
    return a*x**6 + b*x**5 + c*x**4 + d*x**3 + e*x**2 + f*x + g 