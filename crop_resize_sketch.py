import sys
import cv2
import numpy as np
import os

"""
Using OpenCV Python interface, cv2, this script execute the following task:
1, Detect face in a photo
2, Crop the photo into a square with the face in the center
3, Resize the image
4, Create a sketch from the photo

Usage:
python crop_resize_sketch.py xdim ydim photo_dir [file ...]

Note that the edgePreservingFilter, detailEnhance and pencilSketch are only available in OpenCV 3. Installation instruction is here:
http://www.learnopencv.com/install-opencv-3-on-yosemite-osx-10-10-x/
"""

def detect(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    xmlpath = os.path.dirname(__file__)
    cascade = cv2.CascadeClassifier(xmlpath+'/haarcascade_frontalface_alt.xml')
    rects = cascade.detectMultiScale(gray, scaleFactor=1.15, \
            minNeighbors=6, minSize=(20,20))

    if len(rects) == 0:
        print path
        return [], img
            
    points = np.empty_like(rects)
    points[:] = rects
    points[:, 2:] += points[:, :2]
    return rects, points, img
    

def facecrop_max(path):    
    rects, points, img= detect(path)
    height, width, channels = img.shape
    
    x1,y1,x2,y2 = points[0]
    final_delta = min(x1,width-x2,y1,height-y2)
    x1 = x1-final_delta
    x2 = x2+final_delta
    y1 = y1-final_delta
    y2 = y2+final_delta
    
    cropped = img[y1:y2, x1:x2]
    return cropped
    

def resize_img(img, outsize):
    height, width = img.shape[:2]
    if height > outsize[0] or width > outsize[1]:
        res = cv2.resize(img, outsize, interpolation = cv2.INTER_CUBIC)    
    else:
        res = cv2.resize(img, outsize, interpolation = cv2.INTER_AREA)
    return res


def sketch_img(img):
    # outimg = cv2.stylization(img, sigma_s=60, sigma_r=0.07)
    outimg = cv2.edgePreservingFilter(img, flags=1, sigma_s=60, sigma_r=0.4)
    outimg = cv2.detailEnhance(outimg, sigma_s=10, sigma_r=0.15)
    dst_gray, dst_color = cv2.pencilSketch(outimg, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
    return dst_gray


def main():
    args = sys.argv[1:]
    
    if not args:
        print 'usage: xdim ydim photo_dir [file ...]'
        sys.exit(1)
    
    outsize = (int(args[0]), int(args[1]))
    dir = args[2]
    
    if len(args)>3:
        filenames = args[3:]
    else:
        filenames = next(os.walk(dir))[2]
        filenames = [f for f in filenames if not f[0] == '.']
               
    for fname in filenames:
        path = dir + fname
        
        cropimg = facecrop_max(path)
        resizeimg = resize_img(cropimg, outsize)
        
        resdir = dir + 'resizedImg/'
        if not os.path.exists(resdir):
            os.mkdir(resdir)
        cv2.imwrite(resdir+fname, resizeimg)
        
        sketchimg = sketch_img(cropimg)
        sketchimg = resize_img(sketchimg, outsize)
        
        sktdir = dir + 'sketchImg/'
        if not os.path.exists(sktdir):
            os.mkdir(sktdir)
        cv2.imwrite(sktdir+fname, sketchimg)
    
    sys.exit(0)


if __name__ == '__main__':
  main()
    