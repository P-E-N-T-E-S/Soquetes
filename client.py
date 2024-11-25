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


def criar_pacote(numero_sequencia, mensagem):
    checksum = calcular_checksum(mensagem)
    return Pacote(numero_sequencia=numero_sequencia, mensagem=mensagem, checksum=checksum)


def validar_checksum_resposta(resposta):
    partes = resposta.split('|')
    if len(partes) < 3:
        return False, "Resposta malformada"
    mensagem = '|'.join(partes[:-1])  # A mensagem é tudo menos o último campo
    checksum_recebido = partes[-1]
    checksum_calculado = calcular_checksum_resposta(mensagem)
    return checksum_calculado == checksum_recebido, checksum_calculado


def enviar_pacotes(escolha):
    mensagem = input("Digite a mensagem para enviar: ")
    modo = input("Digite '1' para enviar um único pacote ou '2' para enviar em rajada: ")
    metodo = input("Insira o método de resposta do servidor a ser utilizado \n (1) - Go Back N \n (2) - Repetição Seletiva \n")

    cwnd = 1  # Janela de congestionamento inicial
    ssthresh = 16  # Limiar de lentidão inicial
    duplicados = 0  # Contador de ACKs duplicados
    max_cwnd = len(mensagem)  # Tamanho máximo para cwnd
    pacote_erro = 1230921890320193

    if modo == '1':
        pacote = criar_pacote(0, mensagem)
        s.send(bytes(f"{pacote.numero_sequencia}|{pacote.mensagem}|{pacote.checksum}|{escolha}|{metodo}|-1", "utf-8"))
        print(f"Enviado pacote único: {pacote}")

        resposta = s.recv(1024).decode("utf-8")
        valida, checksum_recebido = validar_checksum_resposta(resposta)
        if valida:
            print(f"Resposta válida do servidor: {resposta}")
        elif valida == False and modo != '1':
            print(f"Erro no checksum da resposta! Resposta recebida: {resposta} \n Reenviando")
            s.send(bytes(f"{pacote.numero_sequencia}|{pacote.mensagem}|{pacote.checksum}|{escolha}|{metodo}|-1", "utf-8"))
            print(f"Enviado pacote único: {pacote}")
    elif modo == '2':
        pacote_com_erro = int(input("Digite o índice do pacote que terá erro de integridade (ou -1 para nenhum): "))

        numero_sequencia = 0
        while numero_sequencia < len(mensagem):
            janela_envio = mensagem[numero_sequencia:numero_sequencia + cwnd]
            print(f"\n[Envio] Janela de envio: {len(janela_envio)}")

            for i, caractere in enumerate(janela_envio):
                pacote = criar_pacote(numero_sequencia + i, caractere)
                erro = numero_sequencia + i == pacote_com_erro
                mensagem_erro = f"{pacote.numero_sequencia}|{pacote.mensagem}|{'ERRO' if erro else pacote.checksum}|{escolha}|{metodo}|{pacote_com_erro}"
                s.send(bytes(mensagem_erro, "utf-8"))
                print(f"Enviado pacote {pacote.numero_sequencia}: {pacote} {'[ERRO]' if erro else ''}")
                time.sleep(0.1) 

                resposta = s.recv(1024).decode("utf-8")
                respostas = resposta.split('$$')[:-1]
                for recebido in respostas:
                    print(f"Recebido: {recebido}")

                if metodo == '1':
                    verificador = resposta.split('|')
                    for verificacao in verificador:
                        if verificacao == pacote_erro :         
                            print(f"Enviado pacote {pacote.numero_sequencia}: {pacote} ")
                            mensagem_erro = f"{pacote.numero_sequencia}|{pacote.mensagem}|{pacote.checksum}|{escolha}|{metodo}|{pacote_com_erro}"
                            s.send(bytes(mensagem_erro, "utf-8"))               

                if metodo == '2' and modo != '1':
                    verificador = resposta.split('|')
                    for verificacao in verificador:
                        if verificacao == 'nack':
                            print(f"nack recebido, reenviando pacote n° {pacote.numero_sequencia}")
                            print(f"Enviado pacote {pacote.numero_sequencia}: {pacote} ")
                            mensagem_erro = f"{pacote.numero_sequencia}|{pacote.mensagem}|{pacote.checksum}|{escolha}|{metodo}|{pacote_com_erro}"
                            s.send(bytes(mensagem_erro, "utf-8"))

                pacote_erro = resposta[4]

            sucesso = all(validar_checksum_resposta(r)[0] for r in respostas)
            if sucesso:
                print("[TCP Reno] Todos os pacotes da janela recebidos com sucesso.")
                if cwnd < ssthresh:
                    cwnd = min(cwnd * 2, max_cwnd)
                else:
                    cwnd += 1
                duplicados = 0
            else:
                print("[TCP Reno] Erro detectado! Ajustando ssthresh e reiniciando cwnd.")
                ssthresh = max(cwnd // 2, 1)
                cwnd = 1
                duplicados += 1

            numero_sequencia += len(janela_envio)

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
    s.close()


iniciar_cliente()