"""Aula 07: servidor e cliente HTTP/1.1 em um arquivo, sem classes.

Terminal 1: py aula_http_servidor_cliente.py servidor
Terminal 2: py aula_http_servidor_cliente.py cliente

Abra também http://127.0.0.1:8000/ no Chrome e observe a aba Network.
O servidor serve arquivos da mesma pasta deste script. Na primeira execução,
ele cria exemplos nessa pasta, mas não substitui arquivos existentes.

Exemplo didático: aceita uma requisição por conexão; implementa GET e HEAD.
Não implementa HTTPS nem deve ser exposto à internet.
"""

import mimetypes
import socket
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


PASTA = Path(__file__).resolve().parent
IP = "127.0.0.1"
PORTA = 8000


def criar_exemplos():
    """Cria uma página que faz o navegador pedir vários recursos."""
    arquivos = {
        "index.html": '''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Laboratório HTTP</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="estilo.css">
  <script src="app.js" defer></script>
</head>
<body>
  <h1>Uma página, várias requisições</h1>
  <img src="imagem.svg" alt="Esquema de uma requisição" width="500">
  <p id="resultado">O JavaScript ainda vai buscar dados.txt...</p>
</body>
</html>
''',
        "estilo.css": "body { font: 20px Arial; margin: 40px; background: #101820; color: white; }\n",
        "app.js": '''fetch("dados.txt")
  .then(resposta => resposta.text())
  .then(texto => document.querySelector("#resultado").textContent = texto);
''',
        "dados.txt": "Dados recebidos por uma nova requisição HTTP!\n",
        "imagem.svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="90">
<rect width="500" height="90" rx="12" fill="#17395b"/>
<text x="25" y="54" fill="white" font-size="25">Navegador → GET /imagem.svg</text>
</svg>
''',
    }
    for nome, conteudo in arquivos.items():
        destino = PASTA / nome
        if not destino.exists():
            destino.write_text(conteudo, encoding="utf-8")


def responder(conexao, codigo, motivo, corpo, tipo, enviar_corpo=True, extras=""):
    """Constrói uma resposta HTTP com linha de status, cabeçalhos e corpo."""
    cabecalho = (
        f"HTTP/1.1 {codigo} {motivo}\r\n"
        f"Content-Type: {tipo}\r\n"
        f"Content-Length: {len(corpo)}\r\n"
        "Connection: close\r\n"
        f"{extras}"
        "\r\n"
    )
    conexao.sendall(cabecalho.encode("ascii"))
    if enviar_corpo:
        conexao.sendall(corpo)
    print(f"RESPOSTA: {codigo} {motivo} | {tipo} | {len(corpo)} bytes\n")


def atender(conexao):
    """Lê a requisição, localiza o arquivo e envia a resposta."""
    dados = b""
    while b"\r\n\r\n" not in dados and len(dados) < 16384:
        parte = conexao.recv(4096)
        if not parte:
            return
        dados += parte

    if b"\r\n\r\n" not in dados:
        responder(conexao, 400, "Bad Request", b"Cabecalhos muito grandes.\n", "text/plain; charset=utf-8")
        return

    # Nesta aula só nos interessam a linha inicial e os cabeçalhos.
    linhas = dados.split(b"\r\n\r\n", 1)[0].decode("iso-8859-1").split("\r\n")
    print("\nREQUISIÇÃO RECEBIDA:")
    for linha in linhas:
        print("  " + linha)

    partes = linhas[0].split()
    if len(partes) != 3 or partes[2] != "HTTP/1.1":
        responder(conexao, 400, "Bad Request", b"Requisicao HTTP/1.1 invalida.\n", "text/plain; charset=utf-8")
        return

    metodo, alvo, _ = partes
    if metodo not in ("GET", "HEAD"):
        responder(conexao, 405, "Method Not Allowed", b"Use GET ou HEAD.\n",
                  "text/plain; charset=utf-8", extras="Allow: GET, HEAD\r\n")
        return

    caminho_url = unquote(urlsplit(alvo).path)
    if caminho_url == "/":
        caminho_url = "/index.html"

    # resolve() e is_relative_to() impedem acessar arquivos fora da pasta.
    arquivo = (PASTA / caminho_url.lstrip("/")).resolve()
    print("RECURSO SOLICITADO:", caminho_url)
    if not arquivo.is_relative_to(PASTA):
        responder(conexao, 403, "Forbidden", b"Acesso fora da pasta.\n", "text/plain; charset=utf-8",
                  enviar_corpo=(metodo == "GET"))
    elif not arquivo.is_file():
        responder(conexao, 404, "Not Found", b"Arquivo nao encontrado.\n", "text/plain; charset=utf-8",
                  enviar_corpo=(metodo == "GET"))
    else:
        corpo = arquivo.read_bytes()
        tipo = mimetypes.guess_type(arquivo.name)[0] or "application/octet-stream"
        if tipo.startswith("text/") or tipo in ("image/svg+xml", "application/javascript"):
            tipo += "; charset=utf-8"
        responder(conexao, 200, "OK", corpo, tipo, enviar_corpo=(metodo == "GET"))


def servidor():
    criar_exemplos()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((IP, PORTA))
        sock.listen(5)
        print(f"Servidor em http://{IP}:{PORTA}/")
        print("Pasta servida:", PASTA)
        print("Abra a página no Chrome ou execute o cliente em outro terminal. Ctrl+C encerra.\n")
        try:
            while True:
                conexao, endereco = sock.accept()
                print("Cliente conectado:", endereco)
                with conexao:
                    try:
                        atender(conexao)
                    except (OSError, UnicodeError) as erro:
                        print("Erro nesta conexão:", erro)
        except KeyboardInterrupt:
            print("\nServidor encerrado.")


def cliente():
    metodo = (input("Método [GET/HEAD/POST] (Enter = GET): ").strip().upper() or "GET")
    if metodo not in ("GET", "HEAD", "POST"):
        print("Escolha GET, HEAD ou POST.")
        return
    caminho = input("Caminho (Enter = /; teste /estilo.css ou /inexistente): ").strip() or "/"
    if not caminho.startswith("/") or "\r" in caminho or "\n" in caminho or " " in caminho:
        print("Use um caminho começando com / e sem espaços.")
        return

    requisicao = (
        f"{metodo} {caminho} HTTP/1.1\r\n"
        f"Host: {IP}:{PORTA}\r\n"
        "User-Agent: Aula-Redes-II\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    print("\nREQUISIÇÃO ENVIADA:")
    print(requisicao.replace("\r", ""))

    with socket.create_connection((IP, PORTA), timeout=5) as sock:
        sock.sendall(requisicao.encode("ascii"))
        partes = []
        while True:
            dados = sock.recv(4096)
            if not dados:
                break
            partes.append(dados)

    resposta = b"".join(partes)
    cabecalho, separador, corpo = resposta.partition(b"\r\n\r\n")
    if not separador:
        print("Resposta incompleta.")
        return
    print("RESPOSTA RECEBIDA (status e cabeçalhos):")
    print(cabecalho.decode("iso-8859-1"))
    print(f"\nCORPO RECEBIDO: {len(corpo)} bytes")
    if corpo:
        if caminho.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".pdf")):
            print("Arquivo binário; não exibiremos seus bytes na tela.")
        else:
            print(corpo[:500].decode("utf-8", errors="replace"))


if __name__ == "__main__":
    modo = sys.argv[1].lower() if len(sys.argv) > 1 else input("servidor ou cliente? ").strip().lower()
    try:
        if modo == "servidor":
            servidor()
        elif modo == "cliente":
            cliente()
        else:
            print("Use: py aula_http_servidor_cliente.py servidor|cliente")
    except (ConnectionRefusedError, TimeoutError):
        print("Não foi possível conectar. Inicie primeiro o servidor no outro terminal.")
