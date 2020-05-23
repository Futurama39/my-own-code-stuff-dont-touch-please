from PIL import ImageGrab
from PIL import ImageStat
import keyboard
import threading
from time import sleep
import os
import subprocess
wait = False

#edit these vars probably!
splitkey = 'f12'
verbose = False

filepath = os.path.dirname(__file__)

def get_box():
    proc = subprocess.run(filepath+'\\box.exe',text=True,capture_output=True)
    proc = proc.stdout
    l = proc.split('\n')
    j=0
    for i in l:
        l[j] = int(i)
        j+=1
    return[l[0]+10,l[1]+10,l[0]+110,l[1]+110]

def keywait():
    keyboard.wait('r')
    global wait
    wait = True

box = get_box()

if __name__ =='__main__':
    thread = threading.Thread(target=keywait)
    thread.start()
    while True:
        print(thread.is_alive())
        if wait:
            sleep(1)
            wait = False
        else:
            im = ImageGrab.grab(bbox=box)
            extrema = im.getextrema()
            if extrema[0][0] == 255 and extrema[1][0] == 255 and extrema[2][0] == 255:
                print('fraame!')
                keyboard.send(splitkey)
                sleep(1)
            else:
                if verbose:
                    print('no frame :(')
        if not thread.is_alive():
            thread = threading.Thread(target=keywait)
            thread.start()


