import socket

from protocolo_tcp import enviar_mensagem, receber_mensagem


HOST = "127.0.0.1"
PORTA = 9000


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect((HOST, PORTA))

print("Conectado ao servidor!")


while True:
    print("\n===== Nova conversa ====== \n")
    mensagem = input("Mensagem: ")

    if mensagem == "sair":
        break

    enviar_mensagem(cliente, mensagem)

    resposta = receber_mensagem(cliente)

    print("Resposta Servidor:", resposta)
    
    print("\n========================= \n")

cliente.close()