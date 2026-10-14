"""Alertas ILUSTRATIVOS da aula, guardados na memória do processo.

Nada aqui vem de captura de tráfego real. Como não há banco de dados,
reiniciar a API restaura os dois alertas iniciais.
"""

import itertools
import threading

# Os IPs pertencem a faixas reservadas para documentação (RFC 5737):
# 192.0.2.0/24, 198.51.100.0/24 e 203.0.113.0/24 nunca identificam máquinas reais.
_alertas = [
    {
        "id": 1,
        "origem": "192.0.2.10",
        "tipo": "porta_incomum",
        "descricao": "Conexão observada em porta não esperada",
    },
    {
        "id": 2,
        "origem": "198.51.100.7",
        "tipo": "tentativas_repetidas",
        "descricao": "Múltiplas tentativas de conexão",
    },
]

# Contador que só cresce: um id apagado nunca é reaproveitado por outro alerta.
_proximo_id = itertools.count(start=len(_alertas) + 1)

# Vários alunos podem criar e apagar alertas ao mesmo tempo; a trava faz
# cada alteração da lista acontecer por inteiro, uma de cada vez.
_trava = threading.Lock()


def listar_alertas():
    return list(_alertas)


def buscar_alerta(alerta_id):
    for alerta in _alertas:
        if alerta["id"] == alerta_id:
            return alerta
    return None


def criar_alerta(campos):
    """Recebe origem, tipo e descricao já validados; a API atribui o id."""
    with _trava:
        novo_alerta = {"id": next(_proximo_id), **campos}
        _alertas.append(novo_alerta)
    return novo_alerta


def remover_alerta(alerta_id):
    with _trava:
        alerta = buscar_alerta(alerta_id)
        if alerta is not None:
            _alertas.remove(alerta)


def calcular_metricas():
    por_tipo = {}
    for alerta in _alertas:
        por_tipo[alerta["tipo"]] = por_tipo.get(alerta["tipo"], 0) + 1
    return {"total_alertas": len(_alertas), "por_tipo": por_tipo}
