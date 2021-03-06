import datetime
import os.path
import ConfigParser
import Image
import os
import glob
from paramiko import SSHClient, AutoAddPolicy

dt = datetime.datetime.today()
HOST = 'camlaps.com'
PORT = 22
PRIVATE_KEY = '/home/pi/.ssh/id_rsa'

inifile = ConfigParser.SafeConfigParser()
inifile.read("/home/pi/camlaps.ini")
serialno = inifile.get("user","serialno")
upfolder = inifile.get("user","uploadFolder")

UPLOAD_PATH = upfolder
PIID = serialno + '/'

fpathname = max(glob.iglob('/home/pi/picture/weekday*.mp4'), key=os.path.getctime)
fname = UPLOAD_PATH + PIID + os.path.basename(fpathname)

def upload(local_file, remote_file):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(HOST, PORT, serialno, key_filename=PRIVATE_KEY)
    sftp = ssh.open_sftp()
    try:
        sftp.stat(remote_file)
    except IOError:
        print 'no exist' + remote_file
    else:
        sftp.remove(remote_file)
    sftp.put(local_file, remote_file)
    sftp.close()
    ssh.close()

if __name__ == '__main__':
    print fpathname + ' to ' + fname
    upload(fpathname,fname)
