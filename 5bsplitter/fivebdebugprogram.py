from PIL import ImageDraw
from PIL import ImageGrab
import fivebsplitter

box = fivebsplitter.box
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


im.save('example.png',format="PNG")
print('output saved as example.png!')
