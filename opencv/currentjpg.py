import shutil
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

UPLOAD_PATH = '/campid/' + serialno + '/current.jpg'
newest = max(glob.iglob('/home/pi/picture/img*.jpg'), key=os.path.getctime)
print newest
shutil.copyfile(newest,'/home/pi/picture/current.jpg')
## print UPLOAD_PATH
scp.upload(newest,UPLOAD_PATH)
