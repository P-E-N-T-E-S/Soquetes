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
    if len(partes) != 6:
        return None, None, None
    numero_sequencia = int(partes[0])
    mensagem = partes[1]
    checksum = partes[2]
    escolha = int(partes[3])
    metodo = int(partes[4])
    indice_erro = int(partes[5])
    return Pacote(numero_sequencia=numero_sequencia, mensagem=mensagem, checksum=checksum), escolha, metodo, indice_erro


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)  # Tempo limite de 10 segundos
s.bind((socket.gethostname(), 1234))
s.listen(5)


def iniciar_servidor():
    error_occurred: bool = False
    pacote_com_erro = -1
    print("Servidor aguardando conexões...")
    while True:
        try:
            conexao_cliente, endereco = s.accept()
            print(f"Cliente conectado: {endereco}")
        except socket.timeout:
            print("Tempo limite de espera para conexão expirou. Tentando novamente...")
            continue

        while True:
            try:
                print("Aguardando dados do cliente...")
                dados = conexao_cliente.recv(1024).decode("utf-8")
                if not dados:
                    print("Conexão encerrada pelo cliente.")
                    break

                pacote, escolha, metodo, indice_erro = processar_pacote(dados)
                if not pacote:
                    print("Pacote inválido.")
                    conexao_cliente.send(bytes("nack|invalid$$", "utf-8"))
                    continue

                print(f"Pacote recebido: {pacote}")

                if escolha == 2:
                    print("Simulando atraso de 5 segundos...")
                    time.sleep(5)
                    resposta = f"nack|{pacote.numero_sequencia}|atraso"
                    checksum_resposta = calcular_checksum_resposta(resposta)
                    conexao_cliente.send(bytes(f"{resposta}|{checksum_resposta}", "utf-8"))
                    continue
                if escolha == 3:
                    

                    if checksum_valido:
                        resposta = f"ack|{pacote.numero_sequencia}"
                        checksum_resposta = calcular_checksum_resposta(resposta)
                        conexao_cliente.send(bytes(f"{resposta}|{checksum_resposta}$$", "utf-8"))
                        print(f"Enviado ACK para pacote {pacote.numero_sequencia} com checksum: {checksum_resposta}")
                    else:
                        resposta = f"nack|{pacote.numero_sequencia}|checksum"
                        checksum_resposta = calcular_checksum_resposta(resposta)
                        conexao_cliente.send(bytes(f"{resposta}|{checksum_resposta}", "utf-8"))
                        print(f"Enviado NACK para pacote {pacote.numero_sequencia} com checksum: {checksum_resposta}")

                if (pacote.numero_sequencia == indice_erro) and not error_occurred:
                    error_occurred = True
                    print(f"Simulando falha de checksum no pacote {pacote.numero_sequencia}.")
                    pacote.checksum = "00000000"

                checksum_valido = calcular_checksum(pacote.mensagem) == pacote.checksum
                if metodo == 2:
                    if checksum_valido:
                        resposta = f"ack|{pacote.numero_sequencia}"
                        checksum_resposta = calcular_checksum_resposta(resposta)
                        conexao_cliente.send(bytes(f"{resposta}|{checksum_resposta}$$", "utf-8"))
                        print(f"Enviado ACK para pacote {pacote.numero_sequencia} com checksum: {checksum_resposta}")
                    else:
                        resposta = f"nack|{pacote.numero_sequencia}|checksum"
                        checksum_resposta = calcular_checksum_resposta(resposta)
                        conexao_cliente.send(bytes(f"{resposta}|{checksum_resposta}", "utf-8"))
                        print(f"Enviado NACK para pacote {pacote.numero_sequencia} com checksum: {checksum_resposta}")

                else:
                    if checksum_valido and not error_occurred:
                        resposta = f"ack|{pacote.numero_sequencia}"
                        checksum_resposta = calcular_checksum_resposta(resposta)
                        conexao_cliente.send(bytes(f"{resposta}|{checksum_resposta}$$", "utf-8"))
                        print(f"Enviado ACK para pacote {pacote.numero_sequencia} com checksum: {checksum_resposta}")
                    elif checksum_valido and error_occurred:
                        resposta = f"ack|{pacote_com_erro}"
                        checksum_resposta = calcular_checksum_resposta(resposta)
                        conexao_cliente.send(bytes(f"{resposta}|{checksum_resposta}$$", "utf-8"))
                        print(f"Enviado ACK para pacote {pacote_com_erro} com checksum: {checksum_resposta}")
                    else:
                        resposta = f"ack|{pacote.numero_sequencia}"
                        checksum_resposta = calcular_checksum_resposta(resposta)
                        conexao_cliente.send(bytes(f"{resposta}|{checksum_resposta}$$", "utf-8"))
                        print(f"Enviado ACK para pacote {pacote.numero_sequencia} com checksum: {checksum_resposta}")
                        pacote_com_erro = pacote.numero_sequencia

            except ConnectionAbortedError as e:
                print(f"Conexão encerrada pelo cliente: {e}")
                break
            except Exception as e:
                print(f"Erro inesperado: {e}")
                break

        conexao_cliente.close()


iniciar_servidor()
