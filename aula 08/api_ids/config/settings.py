"""Configurações mínimas da API didática do IDS (Redes II, Aulas 08 e 09).

Uso exclusivo em sala de aula: estas configurações não servem para produção.
"""

import os

# O Django exige uma chave, mas esta API não usa sessões nem login.
# No servidor público (VPS), DJANGO_SECRET_KEY e DJANGO_DEBUG=0 vêm do serviço.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "apenas-para-aula-nao-use-em-producao")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

# "*" permite que os computadores do laboratório acessem a API pelo IP do professor.
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "rest_framework",
    "alertas",
]

ROOT_URLCONF = "config.urls"

# Permite ao Django encontrar alertas/templates/index.html (a página web).
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    },
]

# Sem banco de dados: os alertas ficam na memória do processo (alertas/dados.py).
DATABASES = {}

# Mensagens de erro do DRF em português.
LANGUAGE_CODE = "pt-br"

REST_FRAMEWORK = {
    # A API responde sempre em JSON, mesmo quando aberta direto no navegador.
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    # Sem login nesta etapa: qualquer cliente pode consultar e criar alertas.
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "UNAUTHENTICATED_USER": None,
}
