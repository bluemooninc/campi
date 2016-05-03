#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO  
import os
import sys
sys.path.append('/home/pi/opencv')
import lcd
import subprocess

GPIO.setmode(GPIO.BCM)  

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

#
# python process out
#
ps = subprocess.Popen( 'ps aux | grep python', stdin=subprocess.PIPE,stdout=subprocess.PIPE, close_fds=True, shell=True).stdout
for line in ps.readlines():
    if 'grep' or 'power' in line: continue
    pid = line.strip().split(' ')[ 1 ] 
try:
    os.killpg( os.getpgid(int(pid)), signal.SIGKILL )
except:
    pass
#
# shutdown
#
try:  
        GPIO.wait_for_edge(21, GPIO.FALLING)  
except KeyboardInterrupt:  
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit  

lcd.printLcd("shutdown now. Wait a green light off")
GPIO.cleanup()          # clean up GPIO on normal exit  
os.system("/sbin/shutdown -h now")


