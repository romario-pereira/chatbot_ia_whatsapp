from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from message_buffer import buffer_message
app = FastAPI()

@app.post('/webhook')
async def webhook(request: Request):
    data = await request.json()
    chat_id = data.get('data').get('key').get('remoteJid')
    message = data.get('data').get('message').get('conversation')
    
    if chat_id and message and not '@g.us' in chat_id:
        await buffer_message(
            chat_id=chat_id,
            message=message,
        )

    return {'status': 'ok'}

@app.get('/metrics')
async def metrics():
    """
    Endpoint básico para métricas do Prometheus
    """
    return PlainTextResponse("""# HELP bot_status Status do bot WhatsApp
# TYPE bot_status gauge
bot_status{service="whatsapp_bot"} 1

# HELP bot_requests_total Total de requisições processadas
# TYPE bot_requests_total counter
bot_requests_total{endpoint="webhook"} 0

# HELP bot_uptime_seconds Tempo de execução em segundos
# TYPE bot_uptime_seconds gauge
bot_uptime_seconds{service="whatsapp_bot"} 1
""", media_type="text/plain")

@app.get('/health')
async def health():
    """
    Endpoint de health check
    """
    return {'status': 'healthy', 'service': 'whatsapp_bot'}


