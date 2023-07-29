import subprocess

def motorDriveTranslate(timeTranslate):
    subprocess.call(["./twomotor", "5.0", "5.0", str(timeTranslate)])
    print("Straight ", timeTranslate, "[s]")


def motorDriveRotate(timeRotate):
    subprocess.call(["./twomotor", "-1", "1", str(timeRotate)])
    print("Rotate ", timeRotate, "[s]")

def motorDriveReverseRotate(timeRotate):
    subprocess.call(["./twomotor", "1", "-1", str(timeRotate)])
    print("Rotate ", timeRotate, "[s]")

def motorDriveReTranslate(timeTranslate):
    subprocess.call(["./twomotor", "-5.0", "-5.0", str(timeTranslate)])
    print("Straight ", timeTranslate, "[s]")

while True:
        x=input("flont:1,back:2,right:3,left:4->")
        if x==1:
             motorDriveTranslate(0.5)
        elif x==2:
             motorDriveReTranslate(0.5)
        elif x==3:
             motorDriveReverseRotate(0.3)
        elif x==4:
             motorDriveRotate(0.3)
	
