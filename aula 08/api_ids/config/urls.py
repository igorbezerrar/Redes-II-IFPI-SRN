"""Rotas: cada linha liga um caminho do contrato a uma função de alertas/views.py."""

from django.urls import path

from alertas import views

urlpatterns = [
    path("", views.pagina),  # página web (cliente)
    path("alertas", views.alertas),  # GET lista · POST cria
    path("alertas/<int:alerta_id>", views.alerta_por_id),  # GET consulta · DELETE apaga
    path("metricas", views.metricas),  # GET resumo
]
