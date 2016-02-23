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

UPLOAD_PATH = upfolder + serialno + '/current.jpg'
newest = max(glob.iglob('/tmp/img*.jpg'), key=os.path.getctime)
print newest
scp.upload(newest,UPLOAD_PATH)