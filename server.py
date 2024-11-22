import socket
import time
from dataclasses import dataclass

@dataclass
class Pacote:
    numero_sequencia: int
    mensagem: str
    checksum: str
    janela: str

    
atraso_flag = False
checksum_flag = False

def calcular_checksum(mensagem):
    mensagem = mensagem.encode("utf-8")
    checksum = sum(mensagem)
    return bin(checksum)[2:]

def processar_pacote(dados):
    partes = dados.split('|')
    if len(partes) != 4:
        return None
    numero_sequencia = int(partes[0])
    mensagem = partes[1]
    checksum = partes[2]
    escolha = int(partes[3])
    return Pacote(numero_sequencia=numero_sequencia, mensagem=mensagem, checksum=checksum), escolha

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

def iniciar_servidor():
    global atraso_flag, checksum_flag
    print("Servidor aguardando conexões...")
    while True:
        conexao_cliente, endereco = s.accept()
        print(f"Cliente conectado: {endereco}")
        
        while True:
            dados = conexao_cliente.recv(1024).decode("utf-8")
            if not dados:
                break
            
            pacote, escolha = processar_pacote(dados)
            if not pacote:
                print("Pacote inválido.")
                conexao_cliente.send(bytes("nack", "utf-8"))
                continue
            
            print(f"Pacote recebido: {pacote}")
            
            # Configurando simulações com base na escolha
            atraso_flag = escolha == 2
            checksum_flag = escolha == 3

            if atraso_flag:
                print("Simulando atraso de 5 segundos...")
                time.sleep(5)
                resposta = f"nack|{pacote.numero_sequencia}|atraso"
                conexao_cliente.send(bytes(resposta, "utf-8"))
                continue  # Não processa o pacote mais


            # Simulação de falha de checksum
            if checksum_flag:
                print("Simulando falha de checksum.")
                pacote.checksum = "00000000"

            # Validação do checksum
            if calcular_checksum(pacote.mensagem) == pacote.checksum:
                conexao_cliente.send(bytes(f"ack|{pacote.numero_sequencia}", "utf-8"))
                print(f"Pacote {pacote.numero_sequencia} confirmado com sucesso.")
            else:
                conexao_cliente.send(bytes(f"nack|{pacote.numero_sequencia}|checksum", "utf-8"))
                print(f"Erro no pacote {pacote.numero_sequencia}: Checksum inválido.")

        conexao_cliente.close()

iniciar_servidor()
