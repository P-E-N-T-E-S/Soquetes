import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

def send():
    i = input("Digite a mensagem para ser enviada: ")
    checksum = bytes(i, encoding="ASCII")
    time.sleep(30)
    s.send(bytes(f"Mensagem de hoje: {i}", "utf-8"))

def timer():
    mustend = time.time() + 5
    while True:
        start_time = time.time()
        send()
        while time.time() < mustend:
            try:
                response = s.recv(1024)
                if response == b"ack":
                    print("tudo certo")
                    break
            except socket.timeout:
                print("nao foi possivel")
                break

timer()
