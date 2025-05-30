import os
import socket

from dotenv import load_dotenv


load_dotenv()

def is_running_in_docker():
    """
    Detecta se está rodando dentro do Docker
    """
    try:
        # Tenta resolver o nome evolution-api (só funciona no Docker)
        socket.gethostbyname('evolution-api')
        return True
    except socket.gaierror:
        return False

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL_NAME')
OPENAI_MODEL_TEMPERATURE = os.getenv('OPENAI_MODEL_TEMPERATURE')

MAX_TOKENS_USUARIO = int(os.getenv("MAX_TOKENS_USUARIO", "300"))
AI_CONTEXTUALIZE_PROMPT = os.getenv("AI_CONTEXTUALIZE_PROMPT", "").replace("\\n", "\n")
AI_SYSTEM_PROMPT_RAW    = os.getenv("AI_SYSTEM_PROMPT", "").replace("\\n", "\n")

AI_SYSTEM_PROMPT = AI_SYSTEM_PROMPT_RAW.replace(
    "{{MAX_TOKENS_USUARIO}}",
    str(MAX_TOKENS_USUARIO)
)


VECTOR_STORE_PATH = os.getenv('VECTOR_STORE_PATH')
RAG_FILES_DIR = os.getenv('RAG_FILES_DIR')

# CONFIGURAÇÃO INTELIGENTE DA EVOLUTION API
if is_running_in_docker():
    # Dentro do Docker: usa nome do serviço
    EVOLUTION_API_URL = os.getenv('EVOLUTION_API_URL', 'http://evolution-api:8080')
    print("[CONFIG] Detectado ambiente Docker - usando evolution-api:8080")
else:
    # Desenvolvimento local: usa localhost
    base_url = os.getenv('EVOLUTION_API_URL', 'http://evolution-api:8080')
    EVOLUTION_API_URL = base_url.replace('evolution-api', 'localhost')
    print(f"[CONFIG] Detectado ambiente local - usando {EVOLUTION_API_URL}")

EVOLUTION_INSTANCE_NAME = os.getenv('EVOLUTION_INSTANCE_NAME')
EVOLUTION_AUTHENTICATION_API_KEY = os.getenv('AUTHENTICATION_API_KEY')

REDIS_URL = os.getenv('CACHE_REDIS_URI')

BUFFER_KEY_SUFIX = os.getenv('BUFFER_KEY_SUFIX')
DEBOUNCE_SECONDS = os.getenv('DEBOUNCE_SECONDS')
BUFFER_TTL = os.getenv('BUFFER_TTL')