#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO  
import os
import sys
sys.path.append('/home/pi/opencv')
import lcd
import signal
import subprocess
import time
from time import sleep  # Allows us to call the sleep function to slow down our loop
import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO

GPIO.setmode(GPIO.BCM)  # Set's GPIO pins to BCM GPIO numbering
BUTTON_1 = 20           # Sets our input pins
BUTTON_2 = 21           # Sets our input pins
GPIO.setup(BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set our input pin to be an input, with internal pullup resistor on
GPIO.setup(BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set our input pin to be an input, with internal pullup resistor on

#
# Global Value
#
modeNo = 1 # 1=fast 2=slow
menu = {1:"Mode", 2:"REC Start/Stop", 3:"Upload", 4:"Shutdown", 5:"Information"}
menuNo = 1
pid = 0

#
# process check
#
def existProc(procName):
    ps = subprocess.Popen( 'ps aux | grep python', stdin=subprocess.PIPE,stdout=subprocess.PIPE, close_fds=True, shell=True).stdout
    for line in ps.readlines():
        if procName in line:
            print 'exist '+ procName
            return True
    print 'no exist ' + procName
    return False
#
# python process out
#
def killPythonPrg(procName='all'):
    ps = subprocess.Popen( 'ps aux | grep python', stdin=subprocess.PIPE,stdout=subprocess.PIPE, close_fds=True, shell=True).stdout
    print 'kill ' + procName
    for line in ps.readlines():
        if 'grep' or 'power' in line:
            continue
        if procName=='all' or procName in line:
            print line
            pid = line.strip().split(' ')[ 1 ]
    try:
        print 'kill -9 ' + pid
        os.killpg( os.getpgid(int(pid)), signal.SIGKILL )
    except:
        pass
#
# mode
#
def setMode(mode=0):
    if mode<=1:
        lcd.printLcd('Set Mode: slow. Press A')
        mode = 2
    else:
        lcd.printLcd('Set Mode: fast. Press A')
        mode = 1
    return mode
#
# shutdown
#
def shutdown():
    killPythonPrg()
    lcd.printLcd("shutdown now. Wait a green light off")
    GPIO.cleanup()          # clean up GPIO on normal exit
    os.system("/sbin/shutdown -h now")
#
# timelapse
#
def timelapse(pid):
    global modeNo
    if pid != 0:
        sys.stdout.flush()
        os.kill(pid, signal.SIGUSR1)
        os.kill(pid + 1, signal.SIGUSR1)
        lcd.printLcd('REC stopped. Press A')
        pid = 0
    else:
        proc = subprocess.Popen('python /home/pi/opencv/timelapse.py ' + str(modeNo),
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        pid = proc.pid
    return pid
#
# upload
#
def upload():
    lcd.printLcd('Now uploading.')
    if existProc('jpg2mp4') or existProc('currentmp4'):
        lcd.printLcd('Busy now.')
    else:
        proc = subprocess.Popen('python /home/pi/opencv/jpg2mp4.py',shell=True,stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        proc = subprocess.Popen('python /home/pi/opencv/currentmp4.py',shell=True,stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        print "waiting"
        proc.wait()
        lcd.printLcd('Upload Finish. Press A')    
#
# hello_world
#
def helloWorld():
    proc = subprocess.Popen('python /home/pi/lcd/hello-world.py',shell=True,stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
#
# Create functions to run when the buttons are pressed
#
def Input_1(channel):
    global menu, menuNo
    # Put whatever Button 1 does in here
    print 'Button 1';
    if menuNo < 5:
        menuNo += 1
    else:
        menuNo = 1
    lcd.printLcd('MENU: ' + menu[menuNo] + ' Press B')

def Input_2(channel):
    global modeNo, menu, menuNo, pid
    # Put whatever Button 2 does in here
    print 'Button 2';
    if menuNo==1:
        modeNo = setMode(modeNo)
    elif menuNo==2:
        pid = timelapse(pid)   
    elif menuNo==3:
        upload() 
    elif menuNo==4:
        shutdown()
    elif menuNo==5:
        helloWorld()

    GPIO.setup(BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Wait for Button 1 to be pressed, run the function in "callback" when it does, also software debounce for 300 ms to avoid triggering it multiple times a second
GPIO.add_event_detect(BUTTON_1, GPIO.BOTH, callback=Input_1, bouncetime=300)
GPIO.add_event_detect(BUTTON_2, GPIO.BOTH, callback=Input_2, bouncetime=800) # Wait for Button 2 to be pressed

# Start a loop that never ends
while True:
    # Put anything you want to loop normally in here
    sleep(60);           
    # Sleep for a full minute, any interrupt will break this so we are just saving cpu cycles.




