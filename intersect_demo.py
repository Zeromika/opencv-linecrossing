import argparse
from random import randint
import datetime
import imutils
import math
import cv2
import numpy as np
pos_x = [None] * 10
pos_y = [None] * 10
direction = [None] * 10

deg_rad = 45 * 3.14 / 180.0

textIn = 0

# Web Cam = Unused
#camera = cv2.VideoCapture(0)
height = 800
width = 1800
 
firstFrame = None
color = [None] * 10
speed = 5
#createObj(10)
obj_mask = [None] * 10
# loop over the frames of the video
for i in range(10):
    color[i] = (0,255,0)
    direction[i] = randint(-1,1)
    pos_x[i] = randint(0,width/2)
    pos_y[i] = randint(0,height)

while True:
    # use it while 
    #(grabbed, frame) = camera.read()
    #text = "Unoccupied"
    #width = int(camera.get(3))   # float
    #height = int(camera.get(4)) # float
    #create frame
    frame = np.zeros((height,width,3), np.uint8)
    line_mask = np.zeros((height,width,3), np.uint8)
    for i in range(10):
        obj_mask[i] = np.zeros((height,width,3), np.uint8)

    cv2.line(line_mask, (width /2, 0), (width/2, height), (250, 0, 1), 5) #blue line
    cv2.line(frame, (width/2 , 0), (width/2,height), (250,0,1),20)
    #print(np.logical_and(obj_mask, line_mask))
    for i in range(10):
        cv2.circle(obj_mask[i], (pos_x[i],pos_y[i]) , 15, color[i], thickness=-1, lineType=8, shift=0) 
        if (np.any(np.logical_and(obj_mask[i], line_mask))):
            textIn = "TRUE"
            color[i] = (0,0,255)
 #       else:
  #          textIn = "FALSE"
            #color[i] = (255,255,255)
        if (pos_x[i] > width or pos_x[i] < 0):
            pos_x[i] = randint(0,200)
            color[i] = (255,255,255)
        if (pos_y[i] > height):
            pos_y[i] -= 20
            direction[i] *= -1
        elif (pos_y[i] < 0):
            pos_y[i] += 20
            direction[i] *= -1
        pos_x[i] += speed
        pos_y[i] += randint(0,10) * direction[i]
        cv2.circle(frame, (pos_x[i],pos_y[i]) , 15, color[i], thickness=-1, lineType=8, shift=0)
    key = cv2.waitKey(1) 
    if key == ord('q'):
        break
    elif key == ord('1'):
        speed += 10
    elif key == ord('2'):
        speed -= 10

    cv2.putText(frame, "Crossing Status: {}".format(str(textIn)), (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow("Security Feed", frame)
#    cv2.imshow("Line", line_mask)
#    cv2.imshow("Obj", obj_mask)

# cleanup the camera and close any open windows
#camera.release()
cv2.destroyAllWindows()

