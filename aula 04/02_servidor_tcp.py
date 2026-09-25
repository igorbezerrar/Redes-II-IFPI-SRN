import socket

from protocolo_tcp import enviar_mensagem, receber_mensagem


HOST = "127.0.0.1"
PORTA = 9000


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

import socket

servidor = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

print("Objeto:", servidor)
print("Família:", servidor.family)
print("Tipo:", servidor.type)
print("Protocolo:", servidor.proto)
print("Descritor:", servidor.fileno())

servidor.bind((HOST, PORTA))
servidor.listen()


print("Endereço local:", servidor.getsockname())
print("Timeout:", servidor.gettimeout())
print(f"Servidor esperando em {HOST}:{PORTA}...")



conexao, endereco = servidor.accept()

print(f"Cliente conectado: {endereco}")


while True:

    mensagem = receber_mensagem(conexao)

    if mensagem is None:
        print("Cliente desconectou.")
        break

    print("Recebido:", mensagem)

    resposta = "ECO: " + mensagem

    enviar_mensagem(conexao, resposta)


conexao.close()
servidor.close()