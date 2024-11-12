import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

falha_tempo = False
falha_checksum = False
tamanho_janela = 2 

def criar():
    s.bind((socket.gethostname(), 1234))
    s.listen(5)

def init():
    global falha_checksum, tamanho_janela
    while True:
        cliente_socket, endereco = s.accept()
        print(f"{endereco} se conectou ao servidor")

        pacotes_recebidos = 0
        while pacotes_recebidos < tamanho_janela:
            dados = cliente_socket.recv(1024).decode("utf-8")
            if not dados:
                break
            
            mensagens = dados.split('|')
            if len(mensagens) != 3:
                print("Formato de mensagem incorreto")
                cliente_socket.send(bytes("nack", "utf-8"))
                continue

            escolha, mensagem, checksum = mensagens[0], mensagens[1], mensagens[2]
            escolha = int(escolha)
            tempo_limite = (time.time() + 10)

            if escolha == 2:
                time.sleep(6)
            elif escolha == 3:
                falha_checksum = True

            if confirmar_checksum(mensagem, checksum):
                print(f"Pacote recebido: {mensagem}")
                print(f"Checksum recebido: {checksum}")
                cliente_socket.send(bytes("ack", "utf-8"))
                pacotes_recebidos += 1
            else:
                print("Checksum incorreto")
                cliente_socket.send(bytes("nack", "utf-8"))
        
        tamanho_janela = min(tamanho_janela + 1, 4)

        cliente_socket.close()

def confirmar_checksum(mensagem, checksum):
    mensagem = mensagem.encode("utf-8")
    checksum_calculado = sum(mensagem)
    checksum_calculado = bin(checksum_calculado)[2:]

    if falha_checksum:
        checksum_simulado = int(checksum, 2) + 1
        checksum_simulado = bin(checksum_simulado)[2:]
        return checksum_calculado == checksum_simulado
    else:
        return checksum_calculado == checksum

criar()
iniciar()
