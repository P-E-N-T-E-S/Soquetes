import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

tamanho_janela = 1
tamanho_max_janela = 4

def checkSum(mensagem):
    mensagem = mensagem.encode("utf-8")
    checksum = 0
    for byte in mensagem:
        checksum += byte
    checksum = bin(checksum)[2:]
    return checksum

def enviar_pacotes(escolha, num_pacotes=1):
    mensagem = input("Digite a mensagem para ser enviada: ")
    checksum = checkSum(mensagem)
    
    if num_pacotes == 1:
        print("Enviando um único pacote...")
        mensagem_completa = f"{escolha}|{mensagem}|{checksum}"
        s.send(bytes(mensagem_completa, "utf-8"))
    else:
        for indice, caractere in enumerate(mensagem):
            mensagem_pacote = f"{escolha}|{caractere}|{checksum}"
            print(f"Enviando pacote {indice + 1}/{len(mensagem)}: {caractere}")
            s.send(bytes(mensagem_pacote, "utf-8"))
            time.sleep(1) 

def menu():
    print("Selecione o tipo de erro a ser simulado:")
    print("1. Nenhum erro")
    print("2. Falha no tempo de execução (simular atraso)")
    print("3. Falha de checksum (simular checksum incorreto)")
    escolha = input("Digite o número da sua escolha: ")
    return escolha

def temporizador():
    escolha = menu()
    num_pacotes = int(input("Digite o número de pacotes a serem enviados (1 para um único ou o tamanho da mensagem para rajada): "))
    enviar_pacotes(escolha, num_pacotes)
    resposta = s.recv(1024)
    if resposta == b"ack":
        print("Recebido ACK: Pacote(s) recebido(s) corretamente.")
    else:
        print("Recebido NACK: Erro na recepção dos pacotes.")

temporizador()
print("Programa Encerrado")
