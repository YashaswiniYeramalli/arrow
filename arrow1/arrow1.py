#! /usr/bin/env python
import numpy as np
import cv2,math  
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import String
import utils

cap=cv2.VideoCapture(0)

while True:
    pub=rospy.Publisher("Image",Image,queue_size=10)
    pub2=rospy.Publisher("Output",String,queue_size=1)
    rospy.init_node('arrow_publisher', anonymous=True)
    rate=rospy.Rate(10)
    success, img=cap.read()

    imgcont,conts,_=utils.getContours(img,cThr=[150,175],showCanny=False,filter=4,draw=False) 
    if len(conts) != 0:
        biggest = conts[0][2]
        imgWarp = utils.warpImg(img, biggest,350,350) #warping the Image to Region of Interest
    
        imgCont2,cont2,imgThre=utils.getContours(imgWarp,cThr=[50,50],showCanny=False,filter=7,draw=False)
        if len(cont2) != 0:
            c=utils.direction(imgWarp)
            cv2.imshow("cut",imgThre)
            if c==1:
                print("Right")
                pub2.publish('Right')
                cv2.putText(img, "RIGHT", (40,40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3) 
            elif c==2:
                print("left")
                pub2.publish('left')
                cv2.putText(img, "LEFT", (40,40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
            elif c==3:
                print("up")
                pub2.publish('up')
                cv2.putText(img, "UP", (40,40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
            else:
                print("down")
                pub2.publish('down')
                cv2.putText(img, "DOWN", (40,40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

    cv2.imshow("Video",img)
    bridge=CvBridge()
    ros_image=bridge.cv2_to_imgmsg(img,"bgr8")
    pub.publish(ros_image)
    rate.sleep()
    k=cv2.waitKey(1) 
    if k==27:
        print("Esc Pressed, Exiting!!")
        break
cap.release()
cv2.destroyAllWindows()

