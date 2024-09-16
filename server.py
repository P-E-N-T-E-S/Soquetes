import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time = time.sleep(3)


def create():
    s.bind((socket.gethostname(), 1234))
    s.listen(5)


def start():
    while True:
        clientsocket, address = s.accept()
        print(f"{address} se conectou ao servidor")
        print(clientsocket.recv(1024))
        clientsocket.close()
            

create()
start()