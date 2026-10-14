"""Views da API do IDS didático: uma função para cada caminho do contrato.

O decorador @api_view lista os métodos aceitos. Qualquer outro método recebe
405 Method Not Allowed automaticamente (exemplo: POST /metricas).
"""

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import dados
from .serializers import AlertaSerializer


def pagina(request):
    """Página web (cliente) servida pela mesma origem da API."""
    return render(request, "index.html")


@api_view(["GET", "POST"])
def alertas(request):
    """Mesmo caminho, dois métodos: GET consulta a lista; POST cria um alerta."""
    if request.method == "GET":
        return Response(dados.listar_alertas())  # 200 OK

    # POST: o corpo JSON precisa ter origem, tipo e descricao.
    serializer = AlertaSerializer(data=request.data)
    if not serializer.is_valid():
        # O DRF usaria 400 por padrão; o contrato da aula define 422.
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    novo_alerta = dados.criar_alerta(serializer.validated_data)
    return Response(novo_alerta, status=status.HTTP_201_CREATED)


@api_view(["GET", "DELETE"])
def alerta_por_id(request, alerta_id):
    """GET consulta um alerta; DELETE o apaga. Se o id não existir: 404."""
    alerta = dados.buscar_alerta(alerta_id)
    if alerta is None:
        return Response(
            {"detail": f"Alerta {alerta_id} não encontrado."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "DELETE":
        dados.remover_alerta(alerta_id)
        return Response(status=status.HTTP_204_NO_CONTENT)  # sucesso, sem corpo

    return Response(alerta)  # 200 OK


@api_view(["GET"])
def metricas(request):
    """Resumo calculado a partir dos alertas atuais."""
    return Response(dados.calcular_metricas())  # 200 OK
