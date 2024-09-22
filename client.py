import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

def send():
    i = input("Digite a mensagem para ser enviada: ")
    checksum = bytes(i, encoding="ASCII")
    s.send(bytes(f"Mensagem de hoje: {i}", "utf-8"))

def timer():
    mustend = (time.time() + 50)
    start_time = time.time()
    send()
    while time.time() < mustend:
        response = s.recv(1024)
        if response == b"ack":
            print(f"{response} tudo certo")
            break
        else:
            print(f"{response} nao foi possivel")
            break

timer()
print("Programa Encerrado")