import scp
import os.path
import ConfigParser
import time
import datetime
import os
import glob


inifile = ConfigParser.SafeConfigParser()
inifile.read("/home/pi/camlaps.ini")
serialno = inifile.get("user","serialno")
delay = inifile.getint("camera","delay")
upfolder = inifile.get("user","uploadFolder")

UPLOAD_PATH = upfolder + serialno + '/'
dt = datetime.datetime.today()
fname = "hour%02d.mp4" % (dt.hour-1,)
newest = max(glob.iglob('/tmp/hour*.mp4'), key=os.path.getctime)
print newest
if os.path.isfile(newest): 
  scp.upload(newest,UPLOAD_PATH + os.path.basename(newest))
  jpgname = os.path.basename(newest) + ".jpg"

newest = max(glob.iglob('/tmp/img*.jpg'), key=os.path.getctime)
if os.path.isfile(newest): 
  print newest
  scp.upload(newest,UPLOAD_PATH + jpgname )
