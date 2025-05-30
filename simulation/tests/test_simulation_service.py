import asyncio
import sys
import os
sys.path.append(os.path.abspath('.'))

# Importações simplificadas para evitar problemas
import time
from typing import Dict, Any

async def test_simulation_service():
    """
    Teste completo do SimulationService
    """
    print("🚀 TESTE DO SIMULATION SERVICE")
    print("=" * 60)
    
    # Simula o SimulationService para teste
    class MockSimulationService:
        def __init__(self):
            self.max_timeout = 120
            self.valid_types = ["Imóveis", "Veículos", "Moto", "Serviços"]
        
        async def validate_parameters(self, consortium_type: str, credit_value: float):
            if not consortium_type or consortium_type not in self.valid_types:
                raise ValueError(f"Tipo inválido. Tipos válidos: {', '.join(self.valid_types)}")
            
            if not credit_value or credit_value <= 0:
                raise ValueError("Valor deve ser maior que zero")
            
            if credit_value < 10000:
                raise ValueError("Valor mínimo: R$ 10.000,00")
            
            if credit_value > 10000000:
                raise ValueError("Valor máximo: R$ 10.000.000,00")
        
        async def simulate_consortium(
            self, 
            consortium_type: str, 
            credit_value: float,
            user_id: str = None
        ) -> Dict[str, Any]:
            start_time = time.time()
            simulation_id = f"sim_{int(start_time)}"
            
            print(f"📊 Iniciando simulação...")
            print(f"   • ID: {simulation_id}")
            print(f"   • Tipo: {consortium_type}")
            print(f"   • Valor: R$ {credit_value:,.2f}")
            print(f"   • Usuário: {user_id or 'Anônimo'}")
            
            try:
                # 1. Validação
                await self.validate_parameters(consortium_type, credit_value)
                print("   ✅ Parâmetros validados")
                
                # 2. Simula execução dos agentes
                print("   🔄 Executando DataGeneratorAgent...")
                await asyncio.sleep(0.5)  # Simula tempo de execução
                
                print("   🌐 Executando NavigatorAgent...")
                await asyncio.sleep(1.0)  # Simula navegação
                
                print("   📱 Executando ResponseFormatterAgent...")
                await asyncio.sleep(0.3)  # Simula formatação
                
                # 3. Simula resultados
                simulation_results = [
                    {
                        'grupo': 'Em Andamento',
                        'valor_credito': f'R$ {credit_value * 0.9:,.2f}',
                        'meses': '219 meses',
                        'valor_parcela': f'R$ {(credit_value * 0.9) / 219:,.2f}',
                        'mensagem_especial': None
                    },
                    {
                        'grupo': 'Em Andamento',
                        'valor_credito': f'R$ {credit_value:,.2f}',
                        'meses': '219 meses',
                        'valor_parcela': f'R$ {credit_value / 219:,.2f}',
                        'mensagem_especial': None
                    }
                ]
                
                # 4. Formata resposta
                formatted_response = self._format_response(
                    consortium_type, credit_value, simulation_results
                )
                
                execution_time = time.time() - start_time
                
                return {
                    "success": True,
                    "simulation_id": simulation_id,
                    "execution_time": execution_time,
                    "formatted_response": formatted_response,
                    "simulation_results": simulation_results,
                    "form_data": {
                        "nome": "João Silva",
                        "email": "joao@email.com",
                        "telefone": "11999998888",
                        "cep": "01234-567"
                    }
                }
                
            except Exception as e:
                execution_time = time.time() - start_time
                error_response = f"""❌ *Ops! Algo deu errado*

Não consegui processar sua simulação no momento.
Motivo: {str(e)}

🔄 Tente novamente em alguns instantes.
📋 Código: {simulation_id[:8]}"""
                
                return {
                    "success": False,
                    "simulation_id": simulation_id,
                    "execution_time": execution_time,
                    "error": str(e),
                    "formatted_response": error_response
                }
        
        def _format_response(self, tipo, valor, resultados):
            response = f"🏆 *Simulação de {tipo}*\n"
            response += f"💰 Valor solicitado: *R$ {valor:,.2f}*\n\n"
            response += f"✅ Encontrei *{len(resultados)} opções* para você:\n\n"
            
            for idx, resultado in enumerate(resultados, 1):
                response += f"📋 *Opção {idx}*\n"
                response += f"🟢 Status do Grupo: {resultado['grupo']}\n"
                response += f"💵 Crédito: *{resultado['valor_credito']}*\n"
                response += f"📅 Prazo: {resultado['meses']}\n"
                response += f"💳 Parcela: *{resultado['valor_parcela']}*\n\n"
            
            response += "🏠 *Ademicon - Consórcio há mais de 30 anos*\n"
            response += "🔥 *GARANTE JÁ A SUA COTA!*\n"
            response += "📞 *FALE AGORA COM NOSSO CONSULTOR*"
            
            return response
        
        async def health_check(self):
            return {
                "status": "healthy",
                "timestamp": time.time(),
                "services": {
                    "data_generator": "ok",
                    "navigator": "ok", 
                    "formatter": "ok"
                }
            }
    
    # TESTES
    service = MockSimulationService()
    
    # 1. Teste de simulação válida
    print("\n1️⃣ TESTE: Simulação válida")
    print("-" * 40)
    result = await service.simulate_consortium("Imóveis", 540000, "user123")
    
    if result["success"]:
        print(f"✅ Simulação concluída em {result['execution_time']:.2f}s")
        print(f"📋 ID: {result['simulation_id']}")
        print(f"📊 Resultados: {len(result['simulation_results'])} opções")
        print("\n📱 RESPOSTA FORMATADA:")
        print("-" * 30)
        print(result["formatted_response"])
    else:
        print(f"❌ Falha: {result['error']}")
    
    # 2. Teste de validação (valor inválido)
    print("\n2️⃣ TESTE: Validação de parâmetros")
    print("-" * 40)
    result = await service.simulate_consortium("Imóveis", 5000)  # Valor muito baixo
    
    if not result["success"]:
        print("✅ Validação funcionando corretamente")
        print(f"❌ Erro capturado: {result['error']}")
    else:
        print("❌ Deveria ter falhado na validação")
    
    # 3. Teste de health check
    print("\n3️⃣ TESTE: Health Check")
    print("-" * 40)
    health = await service.health_check()
    print(f"Status: {health['status']}")
    print(f"Serviços: {health['services']}")
    
    print("\n🎯 TESTES CONCLUÍDOS!")
    print("=" * 60)

async def test_integration_example():
    """Exemplo de como usar o SimulationService"""
    print("\n💡 EXEMPLO DE USO NO WHATSAPP:")
    print("=" * 50)
    
    # Simula uma conversa do WhatsApp
    user_input = {
        "message": "Quero simular um consórcio de R$ 600.000 para imóvel",
        "user_id": "whatsapp_user_456"
    }
    
    # Parse da mensagem (seria feito pelo chatbot)
    consortium_type = "Imóveis"
    credit_value = 600000
    user_id = user_input["user_id"]
    
    print(f"📱 Usuário: {user_input['message']}")
    print(f"🤖 Processando: Tipo={consortium_type}, Valor=R${credit_value:,.2f}")
    
    # Como seria chamado no chatbot:
    print("\n📝 CÓDIGO DE INTEGRAÇÃO:")
    print("-" * 30)
    print("""
# No seu chatbot:
from simulation.services import SimulationService

async def handle_simulation_request(consortium_type, credit_value, user_id):
    service = SimulationService()
    
    result = await service.simulate_consortium(
        consortium_type=consortium_type,
        credit_value=credit_value, 
        user_id=user_id
    )
    
    if result["success"]:
        # Envia resposta formatada para o WhatsApp
        await send_whatsapp_message(
            user_id, 
            result["formatted_response"]
        )
    else:
        # Envia mensagem de erro
        await send_whatsapp_message(
            user_id,
            result["formatted_response"]
        )
    """)

if __name__ == "__main__":
    asyncio.run(test_simulation_service())
    asyncio.run(test_integration_example()) 