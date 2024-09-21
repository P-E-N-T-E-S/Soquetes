import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)  # Define um tempo limite para o socket

def create():
    s.bind((socket.gethostname(), 1234))
    s.listen(5)

def start():
    while True:
        try:
            clientsocket, address = s.accept()
            print(f"{address} se conectou ao servidor")
            start_timer = time.time()
            end_timer = start_timer + 30
            try:
                data = clientsocket.recv(1024)
                if data and start_timer < end_timer:
                    print("Recebi")
                    clientsocket.send(bytes("ack", "utf-8"))
                else:
                    raise ValueError("No data received or timeout")
            except (socket.timeout, ValueError):
                print(f"{start_timer} Nao recebi")
                clientsocket.send(bytes("NACK", "utf-8"))
                clientsocket.send(bytes("Encerrei", "utf-8"))
                clientsocket.close()
        except socket.timeout:
            print("Timeout ao tentar aceitar uma conexão. Tentando novamente...")

create()
start()
