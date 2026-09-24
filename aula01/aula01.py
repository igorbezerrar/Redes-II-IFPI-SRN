from urllib.request import urlopen
from urllib.error import URLError

protocolo = "http"
servidor = "127.0.5.1"
porta = 8005
recurso = "/hello.html"

url = f"{protocolo}://{servidor}:{porta}{recurso}"

print(f"Cliente: programa Python")
print(f"Destino: {servidor}:{porta}")
print(f"URL solicitada: {url}")

try:
    with urlopen(url, timeout=5) as resposta:
        print(f"Status HTTP: {resposta.status}")
        print(
            f"Tipo do conteúdo: "
            f"{resposta.headers.get('Content-Type')}"
        )

        conteudo = resposta.read(200)
        texto = conteudo.decode("utf-8", errors="replace")

        print("Primeiros bytes da resposta:")
        print(texto)

except URLError as erro:
    print(f"Não foi possível acessar o serviço: {erro}")