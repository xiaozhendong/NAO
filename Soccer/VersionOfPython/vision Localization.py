import cv2
import numpy
import time
import paramiko
import math
from naoqi import ALProxy

IP = "192.168.199.88"
PORT = 9559
transPORT = 22
#imgName = "test"
# 0 camera on the top, 1 camera om the bottom
cameraID = 1

start = time.clock()

"""
 def turn_head(IP, PORT):
        HeadMove=ALProxy("ALMotion",IP, PORT)
        names=["HeadYaw","HeadPitch"]
        angleLists=[[-0.7,-0.5,-0.4,-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4,0.5,0.7,0.5,0.4,0.3,0.2,0.1,0.0,-0.1,-0.2,-0.3,-0.4,-0.5,-0.7,0.0],[-0.1,0.1,0.0]]
        timeLists=[[1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5,25.5,28],[1.5,14.5,28]]
        isAbsolute=True
        HeadMove.angleInterpolation(names, angleLists, timeLists, isAbsolute)
"""      

def set_head_angles(IP, PORT):

    motionProxy = ALProxy("ALMotion", IP, PORT)

    stiffnesses = 0.0

    motionProxy.setStiffnesses("HeadPitch", stiffnesses)
    motionProxy.setStiffnesses("HeadYaw", stiffnesses)

def get_head_angles(IP, PORT):

    motionProxy = ALProxy("ALMotion", IP, PORT)

    use_sensors= True
    HeadPitch_Angle = motionProxy.getAngles("HeadPitch", use_sensors)
    HeadYaw_Angle = motionProxy.getAngles("HeadYaw", use_sensors)

    print "HeadPitch:", str(HeadPitch_Angle), "HeadYaw:", str(HeadYaw_Angle)

    return HeadPitch_Angle, HeadYaw_Angle


def take_picture(IP, PORT, cameraID):

    photoCaptureProxy = ALProxy("ALPhotoCapture", IP, PORT)
    Resolution = 2
    Format = "jpg"

    # Take a picture in VGA and store them in /home/nao/recordings/cameras/
    photoCaptureProxy.setCameraID(cameraID)
    photoCaptureProxy.setResolution(Resolution)
    photoCaptureProxy.setPictureFormat(Format)
    photoCaptureProxy.takePicture("/home/nao/recordings/cameras/", "test1")

def transport_image(IP, transPORT):

    localpath = 'E:/test1.jpg'
    remotepath = '/home/nao/recordings/cameras/test1.jpg'

    t = paramiko.Transport((IP, transPORT))
    t.connect(username='nao', password='nao')
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.get(remotepath, localpath)
    t.close()

    print "transport picture done"

def FindCoor():

    original_img = cv2.imread('E:/test1.jpg', cv2.IMREAD_GRAYSCALE)
    #cv2.imshow("test1", original_img)

    ret, img = cv2.threshold(original_img, 155, 255, cv2.THRESH_BINARY)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    cv2.imshow("test1", img)
    cv2.waitKey(1000)
    rows, cols = img.shape
    print rows, cols

    colsum = []
    for i in range(rows):
        a = img[i].sum()
        colsum.append(a)

    rowsum = []
    for j in range(cols):
        b = img[:, j].sum()
        rowsum.append(b)

    #print colsum, '\n', rowsum

    cx = max(colsum)
    ry = max(rowsum)
    for i in range(len(rowsum)):
        if rowsum[i] == ry:
            rynum = i

    for i in range(len(colsum)):
        if colsum[i] == cx:
            cxnum = i
    #print cxnum, rynum
    return cxnum, rynum
    #cv2.waitKey()
	#cv2.destroyAllWindows()


def CountDistance(cameraID):

    cxnum,rynum = FindCoor()
    HeadPitch_Angle,HeadYaw_Angle=get_head_angles(IP, PORT)
    distx = -(cxnum-640/2)
    disty = rynum-480/2
    print distx
    print disty
    Picture_angle=disty*(47.64/480)

    if cameraID == 0:
        h = 0.508
        Camera_angle = 1.2
    else:
        h = 0.457
        Camera_angle = 39.7

    a = math.pi*(Picture_angle+Camera_angle)/180+HeadPitch_Angle
    d1 = h/math.tan(a)
    alpha = math.pi*(distx*60.92/640)/180
    d2 = d1/math.cos(alpha)
    Forword_Distance = d2*math.cos(alpha+HeadYaw_Angle)
    Sideword_Distance = -d2*math.sin(alpha+HeadYaw_Angle)

    return Forword_Distance, Sideword_Distance

def WalkTo(IP, PORT):
    motionProxy = ALProxy("ALMotion", IP, PORT)
    postureProxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    # Example showing the moveTo command
    # The units for this command are meters and radians
    x, y = CountDistance(cameraID)
    theta = 0
    motionProxy.moveTo(x, y, theta)
    # Will block until move Task is finished

    # Go to rest position
    motionProxy.rest()

def main(IP, PORT, cameraID, transPORT):
    set_head_angles(IP, PORT)
    get_head_angles(IP, PORT)
    take_picture(IP, PORT, cameraID)
    transport_image(IP, transPORT)
   # FindCoor()
   # CountDistance(cameraID)
    #WalkTo(IP, PORT)

if __name__ == "__main__":
    main(IP, PORT, cameraID, transPORT)

end = time.clock()
print "read: %f s" % (end - start)

"""
def catchTarget():
    # Choregraphe bezier export in Python.

    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ -0.11868, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ -0.17185, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ -0.17185, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ -0.17185, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ -0.17338, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ -0.17185, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ -0.17185, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ -0.17338, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("HeadYaw")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ -0.01845, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ -0.01845, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ -0.01845, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ -0.01845, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ -0.01845, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ -0.01845, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ -0.01845, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ -0.01845, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("LAnklePitch")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 0.09046, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ 0.09046, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ 0.08893, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ 0.08893, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ 0.08893, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ 0.09046, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ 0.08586, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ 0.08740, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("LAnkleRoll")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ -0.13035, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ -0.13035, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ -0.13035, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ -0.13035, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ -0.13035, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ -0.13035, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ -0.13035, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ -0.13035, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("LElbowRoll")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ -0.38192, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ -0.37732, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ -0.38192, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ -0.38192, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ -0.37579, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ -0.38499, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ -0.38499, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ -0.38499, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("LElbowYaw")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ -1.18889, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ -1.19043, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ -1.19043, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ -1.18889, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ -1.18889, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ -1.19043, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ -1.19043, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ -1.19043, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("LHand")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 0.00538, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ 0.00538, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ 0.00538, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ 0.00538, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ 0.00538, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ 0.00538, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ 0.00538, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ 0.00538, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("LHipPitch")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 0.12736, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ 0.13043, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ 0.13043, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ 0.13043, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ 0.13197, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ 0.12736, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ 0.12890, [ 3, -0.58667, -0.00048], [ 3, 0.66667, 0.00054]], [ 0.13043, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("LHipRoll")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 0.09975, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ 0.10129, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ 0.09975, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ 0.09975, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ 0.09975, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ 0.09975, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ 0.09975, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ 0.09975, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("LHipYawPitch")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ -0.16870, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ -0.16870, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ -0.17023, [ 3, -0.41333, 0.00055], [ 3, 0.36000, -0.00048]], [ -0.17177, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ -0.17177, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ -0.17177, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ -0.17177, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ -0.17177, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("LKneePitch")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ -0.09233, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ -0.09233, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ -0.08901, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ -0.09055, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ -0.09055, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ -0.09208, [ 3, -0.45333, 0.00019], [ 3, 0.58667, -0.00025]], [ -0.09233, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ -0.09233, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("LShoulderPitch")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 1.53089, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ 1.53089, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ 1.53089, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ 1.53089, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ 1.52936, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ 1.53089, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ 1.53089, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ 1.53089, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("LShoulderRoll")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 0.11654, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ 0.11501, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ 0.11654, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ 0.11501, [ 3, -0.36000, 0.00035], [ 3, 0.70667, -0.00068]], [ 0.11347, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ 0.12114, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ 0.11808, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ 0.11808, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("LWristYaw")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 0.08893, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ 0.08893, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ 0.08740, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ 0.08740, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ 0.09046, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ 0.08893, [ 3, -0.45333, 0.00045], [ 3, 0.58667, -0.00058]], [ 0.08740, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ 0.08893, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("RAnklePitch")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 0.09055, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ 0.08748, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ 0.09055, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ 0.09055, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ 0.09055, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ 0.08901, [ 3, -0.45333, 0.00067], [ 3, 0.58667, -0.00087]], [ 0.08595, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ 0.08748, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("RAnkleRoll")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 0.12890, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ 0.12890, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ 0.13043, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ 0.12890, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ 0.12890, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ 0.13043, [ 3, -0.45333, -0.00045], [ 3, 0.58667, 0.00058]], [ 0.13197, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ 0.13043, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("RElbowRoll")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 0.94345, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ 0.99561, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ 0.81766, [ 3, -0.41333, 0.04400], [ 3, 0.36000, -0.03832]], [ 0.74863, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ 0.77318, [ 3, -0.70667, -0.02454], [ 3, 0.45333, 0.01574]], [ 1.22724, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ 1.08305, [ 3, -0.58667, 0.07994], [ 3, 0.66667, -0.09084]], [ 0.71489, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("RElbowYaw")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 0.00763, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ -0.25775, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ 0.01530, [ 3, -0.41333, -0.05821], [ 3, 0.36000, 0.05070]], [ 0.06899, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ -0.05373, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ 0.75162, [ 3, -0.45333, -0.21174], [ 3, 0.58667, 0.27402]], [ 1.40357, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ 0.66265, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("RHand")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 5.68000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 0.08000, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]],
                  [ 0.70000, [ 3, -0.38667, -0.00005], [ 3, 0.41333, 0.00005]],
                  [ 0.70000, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]],
                  [ 0.70000, [ 3, -0.36000, 0.00000], [ 3, 0.30667, 0.00000]],
                  [ 0.80000, [ 3, -0.30667, 0.00000], [ 3, 0.40000, 0.00000]],
                  [ 0.08000, [ 3, -0.40000, 0.00198], [ 3, 0.45333, -0.00224]],
                  [ 0.07000, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]],
                  [ 0.07000, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]],
                  [ 0.07000, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("RHipPitch")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 0.11501, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ 0.11654, [ 3, -0.38667, -0.00153], [ 3, 0.41333, 0.00164]], [ 0.12881, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ 0.12728, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ 0.12728, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ 0.12114, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ 0.12421, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ 0.12421, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("RHipRoll")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ -0.09967, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ -0.09967, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ -0.09967, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ -0.09967, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ -0.09967, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ -0.09967, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ -0.09967, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ -0.09967, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("RHipYawPitch")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ -0.16870, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ -0.16870, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ -0.17023, [ 3, -0.41333, 0.00055], [ 3, 0.36000, -0.00048]], [ -0.17177, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ -0.17177, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ -0.17177, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ -0.17177, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ -0.17177, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("RKneePitch")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ -0.08893, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ -0.08893, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ -0.08893, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ -0.09200, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ -0.09200, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ -0.08893, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ -0.09233, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ -0.09200, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("RShoulderPitch")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ -0.14415, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ -0.33284, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ -0.21165, [ 3, -0.41333, -0.02760], [ 3, 0.36000, 0.02404]], [ -0.17790, [ 3, -0.36000, -0.00708], [ 3, 0.70667, 0.01389]], [ -0.14876, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ -0.27454, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ -0.24540, [ 3, -0.58667, -0.02915], [ 3, 0.66667, 0.03312]], [ 1.37911, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("RShoulderRoll")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ -0.67193, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ -0.25775, [ 3, -0.38667, -0.11072], [ 3, 0.41333, 0.11836]], [ 0.01530, [ 3, -0.41333, -0.02113], [ 3, 0.36000, 0.01841]], [ 0.03371, [ 3, -0.36000, 0.00000], [ 3, 0.70667, 0.00000]], [ 0.02604, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ 0.08893, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ -0.71489, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ -0.20406, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append("RWristYaw")
    times.append([ 1.28000, 2.44000, 3.68000, 4.76000, 6.88000, 8.24000, 10.00000, 12.00000])
    keys.append([ [ 1.75179, [ 3, -0.42667, 0.00000], [ 3, 0.38667, 0.00000]], [ 1.82387, [ 3, -0.38667, 0.00000], [ 3, 0.41333, 0.00000]], [ 1.68889, [ 3, -0.41333, 0.00000], [ 3, 0.36000, 0.00000]], [ 1.69503, [ 3, -0.36000, -0.00397], [ 3, 0.70667, 0.00779]], [ 1.72417, [ 3, -0.70667, 0.00000], [ 3, 0.45333, 0.00000]], [ 0.31903, [ 3, -0.45333, 0.00000], [ 3, 0.58667, 0.00000]], [ 0.69333, [ 3, -0.58667, 0.00000], [ 3, 0.66667, 0.00000]], [ 0.63350, [ 3, -0.66667, 0.00000], [ 3, 0.00000, 0.00000]]])

    try:
        motion = ALProxy("ALMotion", robotIP, 9559)
        motion.angleInterpolationBezier(names, times, keys);
    except BaseException, err:
        print err
"""