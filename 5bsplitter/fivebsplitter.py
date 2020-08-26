from PIL import ImageGrab
from PIL import ImageStat
import keyboard
import threading
from time import sleep
import os
import subprocess

wait = False
verbose = False
filepath = os.path.dirname(__file__)
countdown = 5 #change for a different countdown

def remove(string): 
    return string.replace(" ", "")
splitkey = input("What is your splitkey? (Usually what the key is called) \n")
mode = input("How may levels do you want before each split? \n")

input('Press enter to start the 5 second countdown. Make sure to have 5b open and      ready. LiveSplit too.\n')
keyboard.send(splitkey)
while countdown < 1 :
    print('starting in ',countdown,' seconds!')
    sleep(1)
    countdown -= 1
print('Start!')

i= 1
def get_box():
    proc = subprocess.run(filepath+'\\box.exe',text=True,capture_output=True)
    proc = proc.stdout
    l = proc.split('\n')
    j=0
    print(l)
    for i in l:
        l[j] = int(i)
        j+=1
    return[l[0]+100,l[1]+100,l[0]+200,l[1]+200]

def keywait():
    keyboard.wait('r')
    global wait
    wait = True

box = get_box()

if __name__ =='__main__':
    thread = threading.Thread(target=keywait)
    thread.start()
    while True:
        if wait:
            sleep(1)
            wait = False
        else:
            im = ImageGrab.grab(bbox=box)
            extrema = im.getextrema()
            if extrema[0][0] >= 245 and extrema[1][0] >= 245 and extrema[2][0] >= 245:
                if i == mode:
                    print('fraame!')
                    keyboard.send(splitkey)
                    sleep(0.5)
                    i=1
                else:
                    i+= 1
                    print('frame but no split')
                    sleep(0.5)
            else:
                if verbose:
                    print('no frame :(')
        if not thread.is_alive():
            thread = threading.Thread(target=keywait)
            thread.start()


