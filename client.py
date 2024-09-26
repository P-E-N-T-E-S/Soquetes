import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

def send(escolha):
    i = input("Digite a mensagem para ser enviada: ")
    checksum = checkSum(i)
    mensagem_completa = f"{escolha}|{i}|{checksum}"
    s.send(bytes(mensagem_completa, "utf-8"))

def timer():
    mustend = (time.time() + 50)
    start_time = time.time()
    escolha = menu()
    send(escolha)
    while time.time() < mustend:
        response = s.recv(1024)
        if response == b"ack":
            print(f"{response} tudo certo")
            break
        else:
            print(f"{response} nao foi possivel")
            break

def checkSum(mensagem):
    mensagem = mensagem.encode("utf-8")
    checksum = 0
    for byte in mensagem:
        checksum += byte
    checksum = bin(checksum)[2:]
    return checksum

def menu():
    print("Selecione o tipo de erro a ser simulado:")
    print("1. Nenhum erro")
    print("2. Falha no tempo de execução (simular atraso)")
    print("3. Falha de checksum (simular checksum incorreto)")
    escolha = input("Digite o número da sua escolha: ")
    return escolha

timer()
print("Programa Encerrado")
