## import datetime
import os.path
import ConfigParser
import Image
from paramiko import SSHClient, AutoAddPolicy
import os
import glob

HOST = 'camlaps.com'
PORT = 22
USER = 'pi'
UPLOAD_TO = '/vagrant/webroot/camlaps/campid/'+USER+'/'
PRIVATE_KEY = '/home/pi/.ssh/id_rsa'

inifile = ConfigParser.SafeConfigParser()
inifile.read("/home/pi/camlaps.ini")
serialno = inifile.get("user","serialno")
PIID = serialno + '/'

def upload(local_file, remote_file):
    if os.path.exists(local_file):
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
        print remote_file
        sftp.put(local_file, remote_file)
        sftp.close()
        ssh.close()

if __name__ == '__main__':
    fpathname = max(glob.iglob('/home/pi/hour*.mp4'), key=os.path.getctime)
    imagename = max(glob.iglob('/tmp/img*.jpg'), key=os.path.getctime)
    fname = UPLOAD_TO + PIID + os.path.basename(fpathname)
    print fpathname + ' to ' + fname
    upload(fpathname, fname)

