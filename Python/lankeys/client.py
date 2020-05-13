import socket
import sys
from msvcrt import getch

port = 69420 #change if port is used, client and server have to use the same port
adress = '' #fill this out with your servers adress
if adress == 0:
    print('Please input adress of your computer on line 6 and restart the program!')
    raise Exception

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        sock.connect((adress,port))
        message = 'test'
        if message == 'quit':
            raise ConnectionAbortedError
        sock.sendall(message)
    except Exception as e:
        sock.close()
        raise e



'''while True:
    key = ord(getch())
    if key == (75 or 77 or 80 or 72): #arrow keys
        break'''

