import socket
import time
from dataclasses import dataclass


@dataclass
class Pacote:
    numero_sequencia: int
    mensagem: str
    checksum: str


def calcular_checksum(mensagem):
    mensagem = mensagem.encode("utf-8")
    checksum = sum(mensagem)
    return bin(checksum)[2:]


def calcular_checksum_resposta(resposta):
    resposta = resposta.encode("utf-8")
    checksum = sum(resposta)
    return bin(checksum)[2:]


def processar_pacote(dados):
    partes = dados.split('|')
    if len(partes) != 5:
        return None, None, None
    numero_sequencia = int(partes[0])
    mensagem = partes[1]
    checksum = partes[2]
    escolha = int(partes[3])
    indice_erro = int(partes[4])
    return Pacote(numero_sequencia=numero_sequencia, mensagem=mensagem, checksum=checksum), escolha, indice_erro


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)


def iniciar_servidor():
    print("Servidor aguardando conexões...")
    while True:
        conexao_cliente, endereco = s.accept()
        print(f"Cliente conectado: {endereco}")

        while True:
            dados = conexao_cliente.recv(1024).decode("utf-8")
            if not dados:
                break

            pacote, escolha, indice_erro = processar_pacote(dados)
            if not pacote:
                print("Pacote inválido.")
                conexao_cliente.send(bytes("nack|invalid$$", "utf-8"))
                continue

            print(f"Pacote recebido: {pacote}")

            # Simula atraso se o cliente escolheu a opção correspondente
            if escolha == 2:
                print("Simulando atraso de 5 segundos...")
                time.sleep(5)

            # Simula falha no checksum para o índice especificado
            if pacote.numero_sequencia == indice_erro:
                print(f"Simulando falha de checksum no pacote {pacote.numero_sequencia}.")
                pacote.checksum = "00000000"

            # Validação do checksum
            checksum_valido = calcular_checksum(pacote.mensagem) == pacote.checksum
            if checksum_valido:
                # Resposta de ACK (confirmação)
                resposta = f"ack|{pacote.numero_sequencia}"
                checksum_resposta = calcular_checksum_resposta(resposta)
                conexao_cliente.send(bytes(f"{resposta}|{checksum_resposta}$$", "utf-8"))
                print(f"Enviado ACK para pacote {pacote.numero_sequencia} com checksum: {checksum_resposta}")
            else:
                # Resposta de NACK (falha na entrega)
                resposta = f"nack|{pacote.numero_sequencia}|checksum"
                checksum_resposta = calcular_checksum_resposta(resposta)
                conexao_cliente.send(bytes(f"{resposta}|{checksum_resposta}", "utf-8"))
                print(f"Enviado NACK para pacote {pacote.numero_sequencia} com checksum: {checksum_resposta}")

        conexao_cliente.close()


iniciar_servidor()