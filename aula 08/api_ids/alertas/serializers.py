"""Contrato de entrada do POST /alertas."""

from rest_framework import serializers


class AlertaSerializer(serializers.Serializer):
    """Valida o corpo JSON enviado pelo cliente.

    origem, tipo e descricao são textos obrigatórios. O id é somente leitura:
    o cliente não o envia; a API o atribui ao criar o alerta.
    """

    id = serializers.IntegerField(read_only=True)
    origem = serializers.CharField()
    tipo = serializers.CharField()
    descricao = serializers.CharField()
