import cv2
import numpy as np
import time
import HandTrackingModule as HM
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#Pycaw is a audio library  

cap = cv2.VideoCapture(0)
#Using webcam for realtime input

Previous_time = 0

detector = HM.handDetector(detectionCon=0.7)
#Creating an instance of class handDetector from HandTrackingModule

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
print(volRange)
#minVol = volRange[0]
#maxVol = volRange[1]
#vol = 0
#volBar = 400
#volPer = 0

while True :
    success,img = cap.read()
    img = detector.findHands(img)
    #Detects and draws landmarks
    lmList = detector.findPosition(img, draw=False)
    #Gives position of the landmarks 
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])
        #For volume control , we are using the thumb and index finger
        #Landmark position of them are 4 and 8
        x1, y1 = lmList[4][1], lmList[4][2]
        #For 4th landmark , we are taking the 1th index(x coordinate) and 2th index(y coordinate)
        x2, y2 = lmList[8][1], lmList[8][2]
        #For 8th landmark , we are taking the 1th index(x coordinate) and 2th index(y coordinate)
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        #cx and cy is center point of the line
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        #Here we drew circles over those two landmarks
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        #Then we drew line connecting those two circles
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        #Then we drew circle at the center point too
        length = math.hypot(x2 - x1, y2 - y1)
        #We will use the length of line to adjust the volume
        print(length)
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])

    Current_time = time.time()
    fps = 1/(Current_time-Previous_time)
    Previous_time=Current_time

    cv2.putText(img,str(int(fps)),(40,40),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),3)
    cv2.imshow("image",img)
    cv2.waitKey(1)