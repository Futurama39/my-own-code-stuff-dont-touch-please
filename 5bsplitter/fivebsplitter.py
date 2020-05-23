from PIL import ImageGrab
from PIL import ImageStat
import keyboard
import threading
from time import sleep
wait = False

#edit these vars probably!
box = (500,500,600,600)
splitkey = 'f12'
verbose = False

def keywait():
    keyboard.wait('r')
    global wait
    wait = True

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


