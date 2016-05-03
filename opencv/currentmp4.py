import shutil
import scp
import os.path
import ConfigParser
import time
import datetime
import os
import glob
import subprocess as sp

inifile = ConfigParser.SafeConfigParser()
inifile.read("/home/pi/camlaps.ini")
serialno = inifile.get("user","serialno")
delay = inifile.getint("camera","delay")
upfolder = inifile.get("user","uploadFolder")

UPLOAD_PATH = upfolder + serialno + '/'
dt = datetime.datetime.today()
fname = "day%02d.mp4" % (dt.day,)
mp4fname = max(glob.iglob('/home/pi/picture/day*.mp4'), key=os.path.getctime)
print mp4fname
if os.path.isfile(mp4fname): 
  fname, ext = os.path.splitext(os.path.basename(mp4fname))
  jpgname = fname + ".jpg"
  scp.upload(mp4fname,UPLOAD_PATH + os.path.basename(mp4fname))

currentjpg = max(glob.iglob('/home/pi/picture/img*.jpg'), key=os.path.getctime)
if os.path.isfile(currentjpg): 
  print currentjpg
  shutil.copyfile(currentjpg,'/home/pi/picture/'+jpgname)
  scp.upload(currentjpg,UPLOAD_PATH + jpgname )

## ffmpeg make m3u8 and upload
##fname, ext = os.path.splitext(os.path.basename(mp4fname))
##command = 'ffmpeg -i ' + mp4fname + \
##    ' -codec copy -map 0 -f segment -vbsf h264_mp4toannexb' + \
##    ' -segment_format mpegts -segment_time 10' + \
##    ' -segment_list /home/pi/picture/' + fname + '-playlist.m3u8' + \
##    ' /home/pi/picture/' + fname + '-%03d.ts'
##print command
##ret  =  sp.check_output( command.split(" ") )
##print ret
##for name in glob.glob('/home/pi/picture/' + fname + '-*'):
##    print name
##    scp.upload(name,UPLOAD_PATH + os.path.basename(name))
