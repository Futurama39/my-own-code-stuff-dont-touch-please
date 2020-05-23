from PIL import ImageGrab
from PIL import ImageStat
import keyboard
import threading
from time import sleep
wait = False

#edit these vars probably!
box = (500,500,550,550)
splitkey = 'a'


def keywait():
    keyboard.wait('r')
    global wait
    wait = True

thread = threading.Thread(target=keywait)
thread.start()
while True:
    if wait:
        sleep(2)
        wait = False
    else:
        im = ImageGrab.grab(bbox=box)
        extrema = im.getextrema()
        if extrema[0][0] == 255 and extrema[1][0] == 255 and extrema[2][0] == 255:
            print('fraame!')
            keyboard.send(splitkey)
        else:
            print('no frame :(')


