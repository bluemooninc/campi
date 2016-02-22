from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time
import datetime
import logging
import scp
import ConfigParser
import os.path
import os
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

LOG_FILENAME = '/tmp/timelapse.log'
UPLOAD_PATH = '/vagrant/html/camlaps/' + serialno + '/current.jpg'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logging.debug(cv2.__version__)
logging.debug('timelapse start...')
#logging.debug(UPLOAD_PATH)
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (frameWidth, frameHeight)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(frameWidth, frameHeight))

print frameWidth
print frameHeight

location = (0,30)
fontscale = 2.0
fontface = cv2.FONT_HERSHEY_PLAIN
color = (255,190,0)
dt = datetime.datetime.today()
seekfile = '/tmp/img%02d-*.jpg' % dt.hour
newestCount = 0
##if glob.glob(seekfile):
##    newestFile = max(glob.iglob(seekfile), key=os.path.getctime)
##    print newestFile
##    if os.path.exists(newestFile):
##        a = re.search('img(\w+)-(\w+)\.jpg', newestFile)
##        newestCount = int(a.group(2)) + 1
##print newestCount
##
## capture start
##
# capture frames from the camera
count = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    img = frame.array
    print count
    now = datetime.datetime.now()
    msg = now.strftime("%Y/%m/%d %H:%M:%S")
    cv2.putText(img,msg,location,fontface,fontscale,color)
    fname = "img%02d-%04d.jpg" % (dt.hour,count,)
    fpath = "/tmp/" + fname
    #logging.debug("debug:"+fname)
    if os.path.exists(fpath):
        os.remove(fpath)
    print fname + msg
    cv2.imwrite(fpath, img)
    ## upload current jpg
    lcd.printLcd("Shot:%04d/%04d, Srial:%s" % (count,shottime,serialno))
    ## scp.upload(fpath,UPLOAD_PATH)
    ## wait
    frame.truncate(0)
    if count < newestCount+shottime:
        time.sleep(delay)
        count+=1
    else:
        break
    

##
## finish
##
lcd.printIP()

