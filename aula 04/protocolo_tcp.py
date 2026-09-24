def enviar_mensagem(socket_conexao, mensagem):
    dados = mensagem.encode("utf-8")
    socket_conexao.sendall(dados)


def receber_mensagem(socket_conexao):
    dados = socket_conexao.recv(1024)

    if not dados:
        return None

    return dados.decode("utf-8")