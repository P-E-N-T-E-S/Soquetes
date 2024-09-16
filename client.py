import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))
def send():
    i = input("Digite a mensagem para ser enviada: ")
    checksum = bytes(i, encoding="ASCII")
    s.send(bytes(f"Mensagem de hoje: {i}", "utf-8"))
    bytes()


send()