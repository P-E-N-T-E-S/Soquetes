import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

setfail: bool = False
checksumfail: bool = False

def create():
    s.bind((socket.gethostname(), 1234))
    s.listen(5)

def start():
    global checksumfail
    while True:
        clientsocket, address = s.accept()
        print(f"{address} se conectou ao servidor")
        data = clientsocket.recv(1024).decode("utf-8")
        mensagens = data.split('|')
        
        if len(mensagens) != 3:
            print("Formato de mensagem incorreto")
            clientsocket.send(bytes("nack", "utf-8"))
            clientsocket.close()
            continue

        escolha, mensagem, checksum = mensagens[0], mensagens[1], mensagens[2]
        escolha = int(escolha)
        end_timer = (time.time() + 5)

        if escolha == 2:
            time.sleep(6)
        elif escolha == 3:
            checksumfail = True
        
        if data and time.time() < end_timer:
            if confirm_checksum(mensagem, checksum):
                print(f"Mensagem recebida: {mensagem}")
                print(f"Checksum recebido: {checksum}")
                clientsocket.send(bytes("ack", "utf-8"))
            else:
                print("Checksum incorreto")
                clientsocket.send(bytes("nack", "utf-8"))
        else:
            print("Tempo esgotado ou dados inválidos")
            clientsocket.send(bytes("nack", "utf-8"))

        clientsocket.close()
    s.close()

def confirm_checksum(mensagem, checksum):
    mensagem = mensagem.encode("utf-8")
    calc_checksum = sum(mensagem)
    calc_checksum = bin(calc_checksum)[2:]
    
    if checksumfail:
        checksum_simulado = int(checksum, 2) + 1
        checksum_simulado = bin(checksum_simulado)[2:]
        return calc_checksum == checksum_simulado
    else:
        return calc_checksum == checksum

create()
start()
