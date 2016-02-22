import cv2
import numpy as np
import time
import datetime
##
## config
##

cap = cv2.VideoCapture(0)
delay = 1      # 10 sec for delay
shottime = 3   # 345 shot times
location = (0,30)
fontscale = 1.0
fontface = cv2.FONT_HERSHEY_PLAIN
color = (255,190,0)
dt = datetime.datetime.today()
fname = '/home/pi/video%02d.mp4' % dt.hour 
time.sleep(1)
print 'Will make' + fname 
##
## set video file name for making
##
f = open('/home/pi/opencv/videofile.ini','w')
f.write(fname)
f.close()
##
## capture start
##
for count in xrange(shottime):
    now = datetime.datetime.now()
    msg = now.strftime("%Y/%m/%d %H:%M:%S")
    ret, img = cap.read()
    cv2.putText(img,msg,location,fontface,fontscale,color)
    fname = "/tmp/img%03d.jpg" % (count,)
    cv2.imwrite(fname, img)
    count = count + 1
    time.sleep(delay)
##
## finish
##
##cv2.DestoryAllWindows()
##cv2.release

