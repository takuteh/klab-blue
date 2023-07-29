import subprocess

def motorDriveTranslate(timeTranslate):
    subprocess.call(["./twomotor", "2.0", "2.0", str(timeTranslate)])
    print("Straight ", timeTranslate, "[s]")


def motorDriveRotate(timeRotate):
    subprocess.call(["./twomotor", "-1", "1", str(timeRotate)])
    print("Rotate ", timeRotate, "[s]")

def motorDriveReverseRotate(timeRotate):
    subprocess.call(["./twomotor", "1", "-1", str(timeRotate)])
    print("Rotate ", timeRotate, "[s]")

