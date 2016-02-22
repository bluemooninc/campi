import cv2
import time

codec = 'XVID'
fourcc = cv2.cv.CV_FOURCC(*codec)
print cv2.__version__
cap=cv2.VideoCapture(0)
rectime=60

# set W,D
ret, img = cap.read()
height, width, layers = img.shape
print height
print width
video = cv2.VideoWriter('./driverec.avi',fourcc,1,(width,height))

for count in xrange(rectime):
    ret, img = cap.read()
    Video.write(img)

cv2.destroyAllWindows()
video.release()
cv2.release

