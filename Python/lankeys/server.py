import socket
import sys
from msvcrt import getch

port = 69420 #change if port is used, client and server have to use the same port
adress = '' #fill this out with your local adress
if adress == 0:
    print('Please input adress of your computer on line 6 and restart the program!')
    raise Exception

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Starting server on port ',port,' on adress ',adress)
sock.bind((adress,port))
sock.listen(1)
while True: #find a connection
    connection, client_adress = sock.accept()
    try:
        data = connection.recv(999)
        print(data)

    except Exception as e:
        connection.close()
        raise e