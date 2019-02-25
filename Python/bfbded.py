import cv2

imagenum = 0
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(40,40))

def numtofile(num):
    return num + 100000

try:
    while True:
        img = cv2.imread(r'F:/BFB/'+str(numtofile(imagenum))+'.jpg')
        print("Opening: ",numtofile(imagenum),".jpg")
        imgp = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
        cv2.imwrite(('F:/BFB2/'+str(numtofile(imagenum))+'.jpg'),imgp)
        imagenum = imagenum+1
except cv2.error:
    print("Finished. Converted ",imagenum," images")