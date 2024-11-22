import socket
import time
from dataclasses import dataclass

@dataclass
class Pacote:
    numero_sequencia: int
    mensagem: str
    checksum: str
    janela: str


def calcular_checksum(mensagem):
    mensagem = mensagem.encode("utf-8")
    checksum = sum(mensagem)
    return bin(checksum)[2:]

def criar_pacote(numero_sequencia, mensagem):
    checksum = calcular_checksum(mensagem)
    return Pacote(numero_sequencia=numero_sequencia, mensagem=mensagem, checksum=checksum)

def enviar_pacotes(escolha):
    mensagem = input("Digite a mensagem para enviar: ")
    modo = input("Digite '1' para enviar um único pacote ou '2' para enviar em rajada: ")
    
    if modo == '1':
        # Envio de um único pacote
        pacote = criar_pacote(0, mensagem)
        s.send(bytes(f"{pacote.numero_sequencia}|{pacote.mensagem}|{pacote.checksum}|{escolha}", "utf-8"))
        print(f"Enviado pacote único: {pacote}")
    elif modo == '2':
        # Envio em rajada (caractere por caractere)
        for numero_sequencia, caractere in enumerate(mensagem):
            pacote = criar_pacote(numero_sequencia, caractere)
            s.send(bytes(f"{pacote.numero_sequencia}|{pacote.mensagem}|{pacote.checksum}|{escolha}", "utf-8"))
            print(f"Enviado pacote {numero_sequencia}: {pacote}")
            time.sleep(1)
    else:
        print("Modo inválido! Envio cancelado.")

def menu():
    print("Selecione o tipo de erro a ser simulado:")
    print("1. Nenhum erro")
    print("2. Falha no tempo de execução (simular atraso)")
    print("3. Falha de checksum (simular checksum incorreto)")
    escolha = input("Digite o número da sua escolha: ")
    return escolha

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

def iniciar_cliente():
    escolha = menu()
    enviar_pacotes(escolha)
    while True:
        resposta = s.recv(1024).decode("utf-8")
        if not resposta:
            break

        partes = resposta.split('|')
        tipo_resposta = partes[0]

        if tipo_resposta == "ack":
            print(f"Recebido ACK para pacote {partes[1]}")
        elif tipo_resposta == "nack":
            motivo = partes[2] if len(partes) > 2 else "desconhecido"
            print(f"Recebido NACK para pacote {partes[1]}: motivo: {motivo}")

            if motivo == "atraso":
                print("Atraso detectado, aguardando...")
                time.sleep(5)

iniciar_cliente()
s.close()
