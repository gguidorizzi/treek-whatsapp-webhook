import os
from fastapi import FastAPI, Request, Response

app = FastAPI()

# Defina esse valor como uma variável de ambiente no seu servidor.
# É a mesma string que você vai colar no campo "Verificar token" no Meta.
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "treek_verify_123")


@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    A Meta chama essa rota (GET) uma única vez quando você clica em
    'Verifique e salve'. Ela manda hub.mode, hub.verify_token e
    hub.challenge. Se o token bater, devolvemos o challenge como texto puro.
    """
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")

    return Response(content="Token inválido", status_code=403)


@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    A Meta chama essa rota (POST) toda vez que chega um evento:
    mensagem recebida, status de entrega, leitura, etc.
    Por enquanto só logamos o payload — depois plugamos no pipeline.
    """
    body = await request.json()
    print("Webhook recebido:", body)

    # TODO: aqui entra a lógica de negócio depois:
    # - extrair mensagens recebidas (respostas de leads)
    # - extrair status de entrega/leitura
    # - salvar no Supabase / disparar próxima ação do pipeline

    return Response(status_code=200)


@app.get("/")
async def health_check():
    return {"status": "ok", "service": "treek-whatsapp-webhook"}
