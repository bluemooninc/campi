import datetime
import cv2
import numpy as np
import ConfigParser
import os.path
##
## config
##
inifile = ConfigParser.SafeConfigParser()
inifile.read("/home/pi/camlaps.ini")
serialno = inifile.get("user","serialno")
frameWidth = inifile.getint("camera","frameWidth")
frameHeight = inifile.getint("camera","frameHeight")
delay = inifile.getint("camera","delay")
shottime = inifile.getint("camera","shottime")
##
## CONFIG
##
fourcc = 'H264'
fps = 30     ## 30 flame par sec
dt = datetime.datetime.today()
fname = "/home/pi/picture/weekday%d.mp4" % (dt.weekday(),)
video = cv2.VideoWriter(fname,cv2.VideoWriter_fourcc(*fourcc),fps,(frameWidth,frameHeight))
##
## read jpg and write video
##
for count in xrange(24):
    fname = "/home/pi/picture/hour%02d.mp4" % (count,)
    print fname
    cap = cv2.VideoCapture(fname)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            video.write(frame)
        else:
            break
##
## finish
##
cap.release()
cv2.destroyAllWindows()
video.release()

