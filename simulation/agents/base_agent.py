from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from uuid import UUID

from ..utils.logger import simulation_logger
from ..exceptions.simulation_exceptions import SimulationError

class BaseAgent(ABC):
    def __init__(self):
        self.next_agent: Optional[BaseAgent] = None
    
    def set_next(self, agent: 'BaseAgent') -> 'BaseAgent':
        """Define o próximo agente na cadeia."""
        self.next_agent = agent
        return agent
    
    @abstractmethod
    async def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa o contexto e passa para o próximo agente se necessário.
        
        Args:
            context: Dicionário com o contexto da simulação
            
        Returns:
            Dict[str, Any]: Contexto atualizado
            
        Raises:
            SimulationError: Se houver erro no processamento
        """
        pass
    
    async def _handle_next(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Passa o contexto para o próximo agente se existir."""
        if self.next_agent:
            return await self.next_agent.handle(context)
        return context
    
    def _log_error(self, 
                  simulation_id: UUID,
                  error: Exception,
                  context: Dict[str, Any]) -> None:
        """Registra erro no logger."""
        simulation_logger.error(
            simulation_id=simulation_id,
            simulation_type=context.get('type'),
            credit_value=context.get('credit_value'),
            status='ERROR',
            error={
                'code': error.__class__.__name__,
                'message': str(error),
                'stack': str(error.__traceback__)
            }
        ) 