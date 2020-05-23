from PIL import ImageGrab
import pytesseract
import keyboard
import threading
from time import sleep

box = (593,159,627,177) #bounding box in which the achcount is displayed
mode = 25 #split every <mode> achievements
splitkey = 'f12' #key in livesplit for splitting
resetkey = 'f11' #key for resetting (doesn't have to be in livesplit but is reccomended)
timeout_time = 7
tess_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #path to tesseract.exe

pytesseract.pytesseract.tesseract_cmd =tess_path

end = False

def keywait():
    keyboard.wait(resetkey)


if __name__ == "__main__":
    while True:
        thread = threading.Thread(target=keywait)
        thread.start()
        next_split = mode
        while True:     #run until any achievement num is found, then start timer and break loop
            im = ImageGrab.grab(bbox=box)
            achcount = pytesseract.image_to_string(im)
            if achcount != '':
                print('let\'s a gooo!')
                keyboard.send(splitkey)
                break
            else:
                print('waiting for run start...')
        while True:     #main loop
            im = ImageGrab.grab(bbox=box)   #grab image from the bounding box
            try:
                achcount = int(pytesseract.image_to_string(im))     #run ocr on image
            except ValueError:
                print('poop!')
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
