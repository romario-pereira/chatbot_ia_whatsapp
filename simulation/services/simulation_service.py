from typing import Dict, Any, Optional
import asyncio
import time
from datetime import datetime
import uuid

from ..agents.data_generator_agent import DataGeneratorAgent
from ..agents.navigator_agent import NavigatorAgent
from ..agents.response_formatter_agent import ResponseFormatterAgent
from ..exceptions.simulation_exceptions import (
    SimulationError, 
    TimeoutError, 
    ValidationError
)
from ..utils.logger import get_logger
from ..config.settings import get_settings

class SimulationService:
    """
    Serviço principal que orquestra todo o fluxo de simulação de consórcio.
    
    Coordena a execução sequencial dos agentes:
    DataGenerator -> Navigator -> ResponseFormatter
    """
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.settings = get_settings()
        
        # Inicializa os agentes
        self.data_generator = DataGeneratorAgent()
        self.navigator = NavigatorAgent()
        self.formatter = ResponseFormatterAgent()
        
        # Configurações
        self.max_timeout = self.settings.SIMULATION_TIMEOUT_SECONDS
        self.valid_types = ["Imóveis", "Veículos", "Moto", "Serviços"]
    
    async def simulate_consortium(
        self, 
        consortium_type: str, 
        credit_value: float,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executa uma simulação completa de consórcio.
        
        Args:
            consortium_type: Tipo do consórcio (Imóveis, Veículos, Moto, Serviços)
            credit_value: Valor do crédito desejado
            user_id: ID do usuário (opcional, para logs)
            
        Returns:
            Dict com resultado da simulação formatado para WhatsApp
            
        Raises:
            ValidationError: Parâmetros inválidos
            TimeoutError: Simulação excedeu tempo limite
            SimulationError: Erro geral na simulação
        """
        simulation_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Log início da simulação
        self.logger.info(
            "Simulação iniciada",
            extra={
                "simulation_id": simulation_id,
                "user_id": user_id,
                "consortium_type": consortium_type,
                "credit_value": credit_value,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        try:
            # 1. Validação dos parâmetros
            await self._validate_parameters(consortium_type, credit_value)
            
            # 2. Prepara contexto inicial
            context = {
                "simulation_id": simulation_id,
                "user_id": user_id,
                "type": consortium_type,
                "credit_value": credit_value,
                "start_time": start_time
            }
            
            # 3. Executa fluxo com timeout
            result = await asyncio.wait_for(
                self._execute_simulation_flow(context),
                timeout=self.max_timeout
            )
            
            # 4. Calcula métricas
            execution_time = time.time() - start_time
            
            # 5. Log sucesso
            self.logger.info(
                "Simulação concluída com sucesso",
                extra={
                    "simulation_id": simulation_id,
                    "execution_time": execution_time,
                    "results_count": len(result.get('simulation_results', [])),
                    "status": "success"
                }
            )
            
            return {
                "success": True,
                "simulation_id": simulation_id,
                "execution_time": execution_time,
                "formatted_response": result.get('formatted_response'),
                "formatted_cards": result.get('formatted_cards'),
                "simulation_results": result.get('simulation_results'),
                "form_data": result.get('form_data')
            }
            
        except asyncio.TimeoutError:
            execution_time = time.time() - start_time
            self.logger.error(
                "Simulação excedeu tempo limite",
                extra={
                    "simulation_id": simulation_id,
                    "execution_time": execution_time,
                    "timeout": self.max_timeout
                }
            )
            raise TimeoutError(f"Simulação excedeu tempo limite de {self.max_timeout}s")
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(
                "Erro na simulação",
                extra={
                    "simulation_id": simulation_id,
                    "execution_time": execution_time,
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            
            # Retorna erro formatado para o usuário
            error_response = await self._format_error_response(str(e), simulation_id)
            return {
                "success": False,
                "simulation_id": simulation_id,
                "execution_time": execution_time,
                "error": str(e),
                "formatted_response": error_response
            }
    
    async def _execute_simulation_flow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa o fluxo completo de simulação."""
        self.logger.info(
            "Iniciando fluxo de agentes",
            extra={"simulation_id": context.get('simulation_id')}
        )
        
        # STEP 1: Gerar dados aleatórios
        self.logger.debug("Executando DataGeneratorAgent")
        context = await self.data_generator.handle(context)
        
        # STEP 2: Navegar e extrair resultados
        self.logger.debug("Executando NavigatorAgent")
        context = await self.navigator.handle(context)
        
        # STEP 3: Formatar resposta
        self.logger.debug("Executando ResponseFormatterAgent") 
        context = await self.formatter.handle(context)
        
        return context
    
    async def _validate_parameters(self, consortium_type: str, credit_value: float) -> None:
        """Valida os parâmetros de entrada."""
        if not consortium_type or consortium_type not in self.valid_types:
            raise ValidationError(
                f"Tipo de consórcio inválido. Tipos válidos: {', '.join(self.valid_types)}"
            )
        
        if not credit_value or credit_value <= 0:
            raise ValidationError("Valor do crédito deve ser maior que zero")
        
        if credit_value < 10000:  # Valor mínimo de R$ 10.000
            raise ValidationError("Valor mínimo para simulação é R$ 10.000,00")
        
        if credit_value > 10000000:  # Valor máximo de R$ 10 milhões
            raise ValidationError("Valor máximo para simulação é R$ 10.000.000,00")
    
    async def _format_error_response(self, error_message: str, simulation_id: str) -> str:
        """Formata uma resposta de erro amigável para o usuário."""
        try:
            return await self.formatter._format_error_response(error_message)
        except:
            # Fallback caso o formatter também falhe
            return (
                "❌ *Ops! Algo deu errado*\n\n"
                "Não consegui processar sua simulação no momento.\n"
                "🔄 Tente novamente em alguns instantes.\n\n"
                "💬 Se o problema persistir, fale com nosso especialista!\n"
                f"📋 Código de referência: {simulation_id[:8]}"
            )
    
    async def get_simulation_summary(
        self, 
        consortium_type: str, 
        credit_value: float
    ) -> Dict[str, Any]:
        """
        Retorna um resumo rápido sem executar navegação completa.
        Útil para pré-visualizações ou validações rápidas.
        """
        await self._validate_parameters(consortium_type, credit_value)
        
        return {
            "consortium_type": consortium_type,
            "credit_value": credit_value,
            "estimated_duration": "30-60 segundos",
            "available_options": "Até 3 opções de simulação",
            "features": [
                "Parcelas reduzidas",
                "Uso do FGTS",
                "Sem juros",
                "Aprovação rápida"
            ]
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Verifica a saúde do serviço e dependências."""
        try:
            # Testa se o site está acessível (simulação rápida)
            test_context = {
                "simulation_id": "health_check",
                "type": "Imóveis",
                "credit_value": 500000
            }
            
            # Só testa geração de dados (mais rápido)
            await self.data_generator.handle(test_context.copy())
            
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "services": {
                    "data_generator": "ok",
                    "settings": "ok",
                    "logger": "ok"
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy", 
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            } 