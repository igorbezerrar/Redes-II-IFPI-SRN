# API do IDS didático — Redes II (Aulas 08 e 09)

API em Django REST Framework que implementa o contrato usado nas aulas.

> **Dados ilustrativos.** Nenhum alerta ou métrica vem de captura de tráfego real.
> Os dados ficam na memória do processo: reiniciar a API restaura os dois alertas iniciais.

## Como executar

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux/macOS
pip install -r requirements.txt
python manage.py runserver
```

Abra <http://127.0.0.1:8000/> com o DevTools (F12) na aba **Network**.

Para que os outros computadores do laboratório acessem a API do professor, rode
`python manage.py runserver 0.0.0.0:8000` e use `http://<IP-do-professor>:8000/`.

## Contrato

| Requisição | Resultado |
|---|---|
| `GET /alertas` | Lista JSON · `200 OK` |
| `GET /alertas/1` | Alerta JSON · `200 OK` |
| `GET /alertas/999` | Recurso inexistente · `404 Not Found` |
| `GET /metricas` | Resumo JSON · `200 OK` |
| `POST /alertas` com JSON válido | Cria o alerta · `201 Created` |
| `POST /alertas` sem campo obrigatório | Erro de validação · `422 Unprocessable Content` |
| `POST /metricas` | `405 Method Not Allowed` |
| `DELETE /alertas/1` | Apaga o alerta · `204 No Content` (sem corpo) |
| `DELETE /alertas/999` | Recurso inexistente · `404 Not Found` |
| `DELETE /alertas` | `405 Method Not Allowed` (não se apaga a coleção inteira) |

Um `id` apagado nunca é reaproveitado: depois de apagar o alerta 3, o próximo POST recebe `id: 4`.

Corpo do `POST /alertas` (o `id` é atribuído pela API):

```json
{
  "origem": "203.0.113.8",
  "tipo": "acesso_suspeito",
  "descricao": "Acesso observado fora do padrão"
}
```

## Onde está cada parte

| Arquivo | Papel |
|---|---|
| `alertas/dados.py` | alertas ilustrativos em memória e cálculo das métricas |
| `alertas/serializers.py` | contrato de entrada do `POST /alertas` |
| `alertas/views.py` | uma função para cada caminho do contrato |
| `config/urls.py` | liga cada caminho à sua função |
| `alertas/templates/index.html` | página web (cliente) que usa `fetch()` |

## Testando pelo terminal (curl)

```bash
curl -i http://127.0.0.1:8000/alertas
curl -i http://127.0.0.1:8000/alertas/999
curl -i -X POST http://127.0.0.1:8000/metricas
curl -i -X DELETE http://127.0.0.1:8000/alertas/1
curl -i -X POST http://127.0.0.1:8000/alertas -H "Content-Type: application/json" -d '{"origem": "203.0.113.8", "tipo": "acesso_suspeito", "descricao": "Acesso observado"}'
curl -i -X POST http://127.0.0.1:8000/alertas -H "Content-Type: application/json" -d '{"origem": "203.0.113.8", "descricao": "Sem o campo tipo"}'
```

No Windows, o terminal pode enviar letras acentuadas fora de UTF-8. Nesse caso a API
responde `400 Bad Request` (JSON malformado), e não `201`. A página web sempre envia UTF-8.
