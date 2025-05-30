import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

def get_logger(name: str = "simulation") -> logging.Logger:
    """
    Função utilitária para obter um logger configurado.
    Compatível com o uso no SimulationService.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Handler para console
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

class SimulationLogger:
    def __init__(self, name: str = "simulation"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Configurar handler para console
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
    
    def _format_log(self, 
                   level: str,
                   simulation_id: Optional[UUID],
                   simulation_type: Optional[str],
                   credit_value: Optional[float],
                   status: str,
                   execution_time: Optional[float],
                   error: Optional[Dict[str, Any]] = None) -> str:
        
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "simulation_id": str(simulation_id) if simulation_id else None,
            "type": simulation_type,
            "credit_value": credit_value,
            "status": status,
            "execution_time": execution_time,
            "error": error
        }
        
        return json.dumps(log_data)
    
    def info(self,
            simulation_id: Optional[UUID],
            simulation_type: Optional[str],
            credit_value: Optional[float],
            status: str,
            execution_time: Optional[float] = None) -> None:
        
        log_message = self._format_log(
            level="INFO",
            simulation_id=simulation_id,
            simulation_type=simulation_type,
            credit_value=credit_value,
            status=status,
            execution_time=execution_time
        )
        self.logger.info(log_message)
    
    def error(self,
             simulation_id: Optional[UUID],
             simulation_type: Optional[str],
             credit_value: Optional[float],
             status: str,
             error: Dict[str, Any],
             execution_time: Optional[float] = None) -> None:
        
        log_message = self._format_log(
            level="ERROR",
            simulation_id=simulation_id,
            simulation_type=simulation_type,
            credit_value=credit_value,
            status=status,
            execution_time=execution_time,
            error=error
        )
        self.logger.error(log_message)
    
    def warning(self,
               simulation_id: Optional[UUID],
               simulation_type: Optional[str],
               credit_value: Optional[float],
               status: str,
               execution_time: Optional[float] = None) -> None:
        
        log_message = self._format_log(
            level="WARNING",
            simulation_id=simulation_id,
            simulation_type=simulation_type,
            credit_value=credit_value,
            status=status,
            execution_time=execution_time
        )
        self.logger.warning(log_message)

# Instância global do logger
simulation_logger = SimulationLogger() 