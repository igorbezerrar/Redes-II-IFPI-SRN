import socket

from protocolo_tcp import enviar_mensagem, receber_mensagem


HOST = "127.0.0.1"
PORTA = 9000


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect((HOST, PORTA))

print("Conectado ao servidor!")
while True:
    print("\n========MENU===========")
    print("\n1 - Enviar Mensagem;")
    print("\n2 - Saber as horas;")
    print("\n3 - Encerrar conexão")
    opcao = int(input("\n Digite a opção: "))

    match opcao:
        case 1:
            mensagem = input("Digite a mensagem")
            enviar_mensagem(cliente, "/MSG", mensagem)
        case 2:
            enviar_mensagem(cliente, "/HORAS", mensagem)
        case 3:
            enviar_mensagem(cliente, "/SAIR", mensagem)
            cliente.close()
            
    resposta = receber_mensagem(cliente)
    print("Resposta Servidor:", resposta)
    
    print("\n========================= \n")

