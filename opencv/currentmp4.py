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
fname = "hour%02d.mp4" % (dt.hour-1,)
mp4fname = max(glob.iglob('/tmp/hour*.mp4'), key=os.path.getctime)
print mp4fname
if os.path.isfile(mp4fname): 
  fname, ext = os.path.splitext(os.path.basename(mp4fname))
  jpgname = fname + ".jpg"

currentjpg = max(glob.iglob('/tmp/img*.jpg'), key=os.path.getctime)
if os.path.isfile(currentjpg): 
  print currentjpg
  scp.upload(currentjpg,UPLOAD_PATH + jpgname )

## ffmpeg make m3u8 and upload
fname, ext = os.path.splitext(os.path.basename(mp4fname))
command = 'ffmpeg -i ' + mp4fname + \
    ' -codec copy -map 0 -f segment -vbsf h264_mp4toannexb' + \
    ' -segment_format mpegts -segment_time 10' + \
    ' -segment_list /tmp/' + fname + '-playlist.m3u8' + \
    ' /tmp/' + fname + '-%03d.ts'
print command
ret  =  sp.check_output( command.split(" ") )
print ret

for name in glob.glob('/tmp/' + fname + '-*'):
    print name
    scp.upload(name,UPLOAD_PATH + os.path.basename(name))
