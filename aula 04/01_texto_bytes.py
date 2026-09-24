texto = "Olá"

dados = texto.encode("utf-8")  # String -> bytes

print("Texto:", texto)
print("Bytes:", dados)
print("Lista de bytes:", list(dados))

# Bytes -> string
texto_recuperado = dados.decode("utf-8")

print("Texto recuperado:", texto_recuperado)