from PIL import ImageGrab
import pytesseract
import keyboard
import threading
from time import sleep
import subprocess
import os
from math import floor

boundbox = (593,159,627,177) #bounding box in which the achcount is displayed ONLY IN MANUAL MODE
manual = False

mode = 25 #split every <mode> achievements
splitkey = 'f12' #key in livesplit for splitting
resetkey = 'f11' #key for resetting (doesn't have to be in livesplit but is reccomended)
timeout_time = 7
tess_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #path to tesseract.exe
near_box = False #toggle to true if there's like bits of a colon in the image, or the box is too big

rel_vals = [0.4822,0.0938,0.8592,0.4792]
tight_vals = [0.4841,0.1046,0.8664,0.4871]

filepath = os.path.dirname(__file__)
end = False

class box():
    def __init__(self,lst):
        self.left = lst[0]
        self.top = lst[1]
        self.bottom = lst[2]
        self.right = lst[3]
        self.width = lst[3]-lst[0]
        self.height = lst[2]-lst[1]

def getbox(rel_vals):
    proc = subprocess.run(filepath+'\\box.exe',text=True,capture_output=True)
    proc = proc.stdout
    l = proc.split('\n')
    j=0
    for i in l:
        l[j] = int(i)
        j+=1
    l = box(l)
    box1 = l.left  +( l.width*rel_vals[0])
    box2 = l.top   +(l.height*rel_vals[1])
    box3 = l.right -( l.width*rel_vals[3])
    box4 = l.bottom-(l.height*rel_vals[2])
    return [floor(box1),floor(box2),floor(box3),floor(box4)]


def keywait():
    keyboard.wait(resetkey)

if manual:
    f_box = boundbox
else:
    if near_box:
        f_box = getbox(tight_vals)
    else:
        f_box = getbox(rel_vals)


pytesseract.pytesseract.tesseract_cmd =tess_path

if __name__ == "__main__":
    while True:
        thread = threading.Thread(target=keywait)
        thread.start()
        next_split = mode
        while True:     #run until any achievement num is found, then start timer and break loop
            im = ImageGrab.grab(bbox=f_box)
            achcount = pytesseract.image_to_string(im)
            if achcount != '':
                print('let\'s a gooo!')
                keyboard.send(splitkey)
                break
            else:
                print('waiting for run start...')
        while True:     #main loop
            im = ImageGrab.grab(bbox=f_box)   #grab image from the bounding box
            try:
                achcount = int(pytesseract.image_to_string(im))     #run ocr on image
            except ValueError:
                print(achcount)
                continue
            print(achcount)
            if achcount >= next_split:  #if achcount is high enough for the next split
                next_split+=mode        
                keyboard.press(splitkey)
                if next_split >=500:
                    end = True
                    break
            if not thread.is_alive():
                keyboard.send(resetkey)
                sleep(timeout_time)
                break
        print('run aborted or finished, restarting...')
