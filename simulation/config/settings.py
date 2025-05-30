from typing import Dict, Any
from pydantic_settings import BaseSettings
from functools import lru_cache

class SimulationSettings(BaseSettings):
    # Configurações do site
    SITE_URL: str = "https://ademicon.com.br/"
    SIMULATION_TIMEOUT: int = 120  # 2 minutos em segundos
    
    # Configurações de cache
    CACHE_TTL: int = 432000  # 5 dias em segundos
    CACHE_PREFIX: str = "simulation:"
    
    # Configurações de validação
    MIN_CREDIT_VALUE: float = 10000
    MAX_CREDIT_VALUE: float = 2000000
    
    # Configurações de simulação
    SIMULATION_TYPES: Dict[str, str] = {
        "imoveis": "Imóveis",
        "servicos": "Serviços",
        "moto": "Moto",
        "veiculos": "Veículos"
    }
    
    # Configurações de retry
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 1  # segundos
    
    # Configurações de rate limiting
    RATE_LIMIT: int = 10  # requisições
    RATE_LIMIT_WINDOW: int = 60  # segundos
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Permite variáveis extras no .env

@lru_cache()
def get_settings() -> SimulationSettings:
    return SimulationSettings() 