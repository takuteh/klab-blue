# coding:utf-8
import func_Get_R_Theta_by_ARmarker
import subprocess
from datetime import datetime

# <<GetTime>>
t = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
print(t)
filename1 = '/mnt/ramdisk/' + t + '_ceil.jpg'
filename2 = '/mnt/ramdisk/' + t + '_floor.jpg'

# <<GetCeilCam>>
subprocess.call("sudo rm /mnt/ramdisk/*.jpg",shell=True)
subprocess.call(["gst-launch-1.0", "-v", "v4l2src", "device=/dev/video1", "num-buffers=1", "!", "jpegenc", "!", "filesink", "location=" + filename1])
R,Th = func_Get_R_Theta_by_ARmarker.main(filename1) #距離(pixel))と角度を取得

print(R)
print(Th)