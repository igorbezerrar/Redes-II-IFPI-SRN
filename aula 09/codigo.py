import socket

# Altere estes valores para fazer os testes em sala.
NOME = "lupibe.com.br"
PORTA = 443

# AF_UNSPEC aceita resultados IPv4 e IPv6.
# Experimente trocar por AF_INET ou AF_INET6.
FAMILIA = socket.AF_UNSPEC

# Para este exemplo, procuramos endereços para uma comunicação TCP.
TIPO = socket.SOCK_STREAM
PROTOCOLO = socket.IPPROTO_TCP

# Solicita também o nome canônico, quando disponível.
# Troque por 0 para comparar com a saída anterior.
OPCOES = socket.AI_CANONNAME

try:
    respostas = socket.getaddrinfo(
        host=NOME,
        port=PORTA,
        family=FAMILIA,
        type=TIPO,
        proto=PROTOCOLO,
        flags=OPCOES,
    )

except socket.gaierror as erro:
    print("Não foi possível resolver o nome:", erro)

else:
    print("Nome consultado:", NOME)
    print("Porta informada pelo programa:", PORTA)
    print("Quantidade de resultados:", len(respostas))
    print()

    for numero, resposta in enumerate(respostas, start=1):
        familia, tipo, protocolo, nome_canonico, endereco = resposta

        if familia == socket.AF_INET:
            versao_ip = "IPv4"
        elif familia == socket.AF_INET6:
            versao_ip = "IPv6"
        else:
            versao_ip = str(familia)

        print(f"Resultado {numero}")
        print("  Família:", versao_ip)
        print("  Tipo de socket:", tipo.name)
        print("  Número do protocolo:", protocolo)
        print("  Nome canônico:", nome_canonico or "(não informado)")
        print("  IP:", endereco[0])
        print("  Porta:", endereco[1])

        # No IPv6, o endereço retornado possui mais dois campos.
        if familia == socket.AF_INET6:
            print("  Flowinfo:", endereco[2])
            print("  Scope ID:", endereco[3])

        print()