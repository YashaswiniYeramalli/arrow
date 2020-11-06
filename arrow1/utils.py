import cv2, numpy as np,math

def getContours(img,cThr=[100,100],showCanny=False,minArea=1000,filter=0,draw =False):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgCanny = cv2.Canny(imgBlur,cThr[0],cThr[1])
    kernel = np.ones((3,3))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=1)
    imgThre = cv2.erode(imgDial,kernel,iterations=1)
    if showCanny:cv2.imshow('Canny',imgThre)
    
    contours,hiearchy = cv2.findContours(imgThre,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    finalCountours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i,True)
            approx = cv2.approxPolyDP(i,0.02*peri,True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalCountours.append([len(approx),area,approx,bbox,i])
            else:
                finalCountours.append([len(approx),area,approx,bbox,i])
    finalCountours = sorted(finalCountours,key = lambda x:x[1] ,reverse= True)

    if draw:
        for con in finalCountours:
            cv2.drawContours(img,con[4],-1,(0,0,255),3)
    return img, finalCountours,imgThre

def direction(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 7, 0.01, 20)

    corners = np.int0(corners)
    #print(corners)
    count = 0
    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 3, 255, -1)

    ordered_coords=[]
    ordered_coords1=[]

   

    
    ordered_coords = [corner.ravel() for corner in corners]
    ordered_coords1 = [corner.ravel() for corner in corners]
        
    ordered_coords.sort(key=lambda x: x[0])
    ordered_coords1.sort(key=lambda x: x[1])
    centroid=[]
    sumx=0
    sumy=0
    for x in ordered_coords:
        sumx=x[0]+sumx
        sumy=x[1]+sumy
    
    centroid.append(sumx/7)
    centroid.append(sumy/7)

    left = 0
    right = 0
    up = 0
    down = 0
    print(ordered_coords)
  
    #print(corners)
    
    for x in ordered_coords:
        if x[0] < centroid[0]:
            left = left + 1
        else:
            right = right + 1
        #if x[1]<centroid[1]:
            #down=down + 1
        #else:
            #up=up+1    
    #for y in ordered_coords1:
                
        #if y[1] < centroid[1]:
            #down = down + 2
        #else:
            #up = up + 2
        #if y[0] < centroid[0]:
            #left = left + 1
        #else:
            #right= right + 1
        
    arr=[]
    arr.append(right)
    arr.append(left)
    arr.append(up)
    arr.append(down)
    print(right)
    print(left)
    print(up)
    print(down)
    #print(arr)
    max=0
    c=0

    c=np. argmax(arr, axis=None)
    del ordered_coords [:]
    del arr[:] 
    print("index:",c)
    print("max:",max)
    c=c+1
    return c

    
         
def reorder(myPoints):
    #print(myPoints.shape)
    myPointsNew = np.zeros_like(myPoints)
    myPoints = myPoints.reshape((4,2))
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1]= myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew

def warpImg (img,points,w,h,pad=20):
    # print(points)
    points =reorder(points)
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp = cv2.warpPerspective(img,matrix,(w,h))
    imgWarp = imgWarp[pad:imgWarp.shape[0]-pad,pad:imgWarp.shape[1]-pad]
    return imgWarp

