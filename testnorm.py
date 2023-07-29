# coding:utf-8
import math
import numpy as np
import random
#from scipy import stats
#from numpy.random import *
from scipy.stats import norm #正規分布
# 使用環境でnumpy,scipyが使えれば良い。要書き換え。

Rbe = 1.0
R = 2.0

#内部パラメータの設定、main.pyに移しても良い。
m = 0
sigma =1


#メトロポリス法を行うプログラム(確率的に採択・棄却を行う。)
#正規分布の生成とパラメータ代入(xは距離)、x:この値の時の確率密度を得られる。、loc:平均m、scale:標準偏差σ

norm1 = norm.pdf(Rbe,m,sigma) #一つ前の距離における確率
norm2 = norm.pdf(R,m,sigma) #現地点の距離における確率

print("norm1 = ",norm1)
print("norm2 = ",norm2)

r = norm2 / norm1 #確率の比をとる。
Ran = random.random() #0~1乱数生成

print("r, Ram = ", r, Ran)