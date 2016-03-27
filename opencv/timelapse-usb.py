import cv2
import numpy as np
import time
import datetime
import logging
import scp
import ConfigParser
import os.path
import os
import socket
import glob
import re
import lcd
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

## get ip address
gw = os.popen("ip -4 route show default").read().split()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((gw[2], 0))
ipaddr = s.getsockname()[0]

LOG_FILENAME = '/tmp/timelapse.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logging.debug(cv2.__version__)
logging.debug('timelapse start...')

# initialize the camera and grab a reference to the raw camera capture
print frameWidth
print frameHeight

location = (0,30)
fontscale = 2.0
fontface = cv2.FONT_HERSHEY_PLAIN
color = (255,190,0)
dt = datetime.datetime.today()
seekfile = '/tmp/img%02d-*.jpg' % dt.hour
newestCount = 0
##
## capture start
##
# capture frames from the camera
count = 0
cap = cv2.VideoCapture(0)
##cap.set(cv2.CV_CAP_PROP_FRAME_WIDTH, frameWidth)
##cap.set(cv2.CV_CAP_PROP_FRAME_HEIGHT, frameHeight) 
while(cap.isOpened()):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    ret, img = cap.read()
    print count
    now = datetime.datetime.now()
    msg = now.strftime("%Y/%m/%d %H:%M:%S")
    cv2.putText(img,msg,location,fontface,fontscale,color,4)
    fname = "img%02d-%04d.jpg" % (dt.hour,count,)
    fpath = "/tmp/" + fname
    #logging.debug("debug:"+fname)
    if os.path.exists(fpath):
        os.remove(fpath)
    print fname + msg
    cv2.imwrite(fpath, img)
    lcd.printLcd("Shot:%04d/%04d, IP:%s" % (count,shottime,ipaddr))
    if count < newestCount+shottime:
        time.sleep(delay)
        count+=1
    else:
        break

##
## finish
##
lcd.printIP()

