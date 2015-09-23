# photoPreprocess

Using OpenCV Python interface, cv2, this script execute the following task:

1. Detect face in a photo
2. Crop the photo into a square with the face in the center
3. Resize the image
4. Create a sketch from the photo

Usage:
```
python crop_resize_sketch.py xdim ydim photo_dir [file ...]
```
Note that the edgePreservingFilter, detailEnhance and pencilSketch are only available in OpenCV 3. Installation instruction is here:
http://www.learnopencv.com/install-opencv-3-on-yosemite-osx-10-10-x/
