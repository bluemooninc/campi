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

##
## upload jpg
##
dt = datetime.datetime.today()
mp4fname = "weekday%d.mp4" % (dt.weekday(),)
fname, ext = os.path.splitext(mp4fname)
UPLOAD_PATH = upfolder + serialno + '/'
newest = max(glob.iglob('/home/pi/picture/img*.jpg'), key=os.path.getctime)
print newest
shutil.copyfile(newest,'/home/pi/picture/'+fname+'.jpg')
scp.upload(newest,UPLOAD_PATH + fname +'.jpg')
##
## ffmpeg make m3u8 and upload
##
command = 'ffmpeg -i ~/picture/' + mp4fname + \
    ' -codec copy -map 0 -f segment -vbsf h264_mp4toannexb' + \
    ' -segment_format mpegts -segment_time 10' + \
    ' -segment_list ~/picture/' + fname + '-playlist.m3u8' + \
    ' ~/picture/' + fname + '-%03d.ts'
print command
ret  =  sp.check_output( command.split(" ") )
print ret
for name in glob.glob('~/picture/' + fname + '-*'):
    print name
    scp.upload(name,UPLOAD_PATH + os.path.basename(name))

