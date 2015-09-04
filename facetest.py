#!/usr/local/bin/python
import cv2
import numpy as np
import os

def detect(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(gray, 1.7, 1, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return [], img
    points = np.empty_like(rects)
    points[:] = rects
    points[:, 2:] += points[:, :2]
    return rects, points, img

def box(points, img):
    for x1, y1, x2, y2 in points:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
    cv2.imwrite('detected.jpg', img)


def facecrop(path, rescale):
    fname,ext=os.path.splitext(path)
    rects, points, img= detect(path)
    height, width, channels = img.shape
    for x, y, w, h in rects:
        xdelta = max(w*(rescale-1),0)
        ydelta = max(h*(rescale-1),0)
        x1 = max(x-xdelta,0)
        x2 = min(x+w+xdelta,width)
        y1 = max(y-ydelta,0)
        y2 = min(y+h+ydelta,height)
        
        final_delta = min(x-x1,x2-x-w,y-y1,y2-y-h)
        x1 = x-final_delta
        x2 = x+w+final_delta
        y1 = y-final_delta
        y2 = y+h+final_delta
        
        cropped = img[y1:y2, x1:x2]
        cv2.imwrite(fname+'_cropped.jpg', cropped)
    

def facecrop_max(path):
    fname,ext=os.path.splitext(path)
    rects, points, img= detect(path)
    height, width, channels = img.shape
    
    x1,y1,x2,y2 = points[0]
    final_delta = min(x1,width-x2,y1,height-y2)
    x1 = x1-final_delta
    x2 = x2+final_delta
    y1 = y1-final_delta
    y2 = y2+final_delta
    
    cropped = img[y1:y2, x1:x2]
    cv2.imwrite(fname+'_cropped.jpg', cropped)



rects, points, img= detect("testPics/CharlesProfilePicture1.jpg")
box(points, img)
#facecrop_max("testPics/dave.jpg")
