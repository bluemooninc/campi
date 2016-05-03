import datetime
import cv2
import ConfigParser
import os.path
import glob
import re
##
## config
##
inifile = ConfigParser.SafeConfigParser()
inifile.read("/home/pi/camlaps.ini")
serialno = inifile.get("user","serialno")
frameWidth = inifile.getint("camera","frameWidth")
frameHeight = inifile.getint("camera","frameHeight")
delay = inifile.getfloat("camera","delay")
shottime = inifile.getint("camera","shottime")
##
## CONFIG
##
fourcc = 'H264'
fps = 30     ## 30 flame par sec
dt = datetime.datetime.today()

dth = dt.day

seekfile = '/home/pi/picture/img%02d-*.jpg' % (dth,)
print seekfile
lastCount = 0
if glob.glob(seekfile):
    newestFile = max(glob.iglob(seekfile), key=os.path.getctime)
    if os.path.exists(newestFile):
        a = re.search('img(\w+)-(\w+)\.jpg', newestFile)
        lastCount = int(a.group(2)) + 1

mfname = "/home/pi/picture/day%02d.mp4" % (dth,)
if os.path.exists(mfname):
    os.remove(mfname)
video = cv2.VideoWriter(mfname,cv2.VideoWriter_fourcc(*fourcc),fps,(frameWidth,frameHeight))
##
## read jpg and write video
##
for count in xrange(lastCount):
    fname = "/home/pi/picture/img%02d-%04d.jpg" % (dth,count,)
    img = cv2.imread(fname)
    video.write(img)
##
## finish
##
cv2.destroyAllWindows()
video.release()
