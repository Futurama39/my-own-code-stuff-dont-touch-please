from PIL import ImageDraw
from PIL import ImageGrab
import goimeautosplitter

box = goimeautosplitter.box
line1a = (box[0],box[1])
line1b = (box[0],box[3])
line2a = (box[0],box[3])
line2b = (box[2],box[3])
line3a = (box[2],box[3])
line3b = (box[2],box[1])
line4a = (box[2],box[1])
line4b = (box[0],box[1])
line1 = [line1a,line1b]
line2 = [line2a,line2b]
line3 = [line3a,line3b]
line4 = [line4a,line4b]
im = ImageGrab.grab()
draw = ImageDraw.Draw(im)
draw.line(xy=(line1),fill=(255,0,0), width=3)
draw.line(xy=(line2),fill=(255,0,0), width=3)
draw.line(xy=(line3),fill=(255,0,0), width=3)
draw.line(xy=(line4),fill=(255,0,0), width=3)
im2 = ImageGrab.grab(bbox=box)

im.save('exampledrawn.png',format="PNG")
im2.save('onlybox.png',format="PNG")
print('example saved saved as exampledrawn.png!')
print('content only in box saved as onlybox.png')
