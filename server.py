import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

setfail: bool = False

def create():
    s.bind((socket.gethostname(), 1234))
    s.listen(5)

def start():
    while True:
        clientsocket, address = s.accept()
        print(f"{address} se conectou ao servidor")
        end_timer = (time.time() + 5)
        data = clientsocket.recv(1024)
        
        if setfail:
            time.sleep(6)

        if (data and time.time() < end_timer):
            print(f"Mensagem recebida: {data}")
            clientsocket.send(bytes("ack", "utf-8"))
            clientsocket.close()
        else:
            print("Test")
            clientsocket.send(bytes("nack", "utf-8"))
            clientsocket.close()

create()
start()