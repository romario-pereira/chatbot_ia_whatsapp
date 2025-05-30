import asyncio
import sys
import os
sys.path.append(os.path.abspath('.'))

async def test_real_simulation_service():
    """
    Teste usando o SimulationService real
    """
    print("🚀 TESTE DO SIMULATION SERVICE REAL")
    print("=" * 60)
    
    try:
        # Importação que pode falhar
        from simulation.services.simulation_service import SimulationService
        
        # Cria o serviço
        service = SimulationService()
        
        print("✅ SimulationService carregado com sucesso!")
        
        # 1. Health Check
        print("\n🏥 HEALTH CHECK:")
        print("-" * 30)
        health = await service.health_check()
        print(f"Status: {health['status']}")
        print(f"Serviços: {health['services']}")
        
        # 2. Teste de validação
        print("\n🔍 TESTE DE VALIDAÇÃO:")
        print("-" * 30)
        
        try:
            await service._validate_parameters("TipoInválido", 50000)
            print("❌ Deveria ter falhado")
        except Exception as e:
            print(f"✅ Validação funcionando: {e}")
        
        # 3. Teste de resumo (sem navegação)
        print("\n📋 TESTE DE RESUMO:")
        print("-" * 30)
        summary = await service.get_simulation_summary("Imóveis", 500000)
        for key, value in summary.items():
            print(f"   {key}: {value}")
        
        # 4. Pergunta se quer executar simulação completa
        print("\n" + "="*60)
        print("💡 Para executar uma simulação COMPLETA (com navegação):")
        print("   Este processo pode levar 30-60 segundos e abrirá o navegador")
        print("="*60)
        
        resposta = input("🤔 Executar simulação completa? (s/n): ")
        
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            print("\n🌐 EXECUTANDO SIMULAÇÃO COMPLETA...")
            print("-" * 40)
            
            result = await service.simulate_consortium(
                consortium_type="Imóveis",
                credit_value=540000,
                user_id="test_user"
            )
            
            if result["success"]:
                print(f"✅ Simulação concluída em {result['execution_time']:.2f}s")
                print(f"📋 ID: {result['simulation_id']}")
                print(f"📊 Resultados: {len(result.get('simulation_results', []))} opções")
                
                print("\n📱 MENSAGEM PARA WHATSAPP:")
                print("-" * 40)
                print(result["formatted_response"])
                
            else:
                print(f"❌ Erro na simulação: {result['error']}")
                print("\n📱 MENSAGEM DE ERRO:")
                print("-" * 40)
                print(result["formatted_response"])
        else:
            print("📝 Simulação completa cancelada.")
        
        print("\n✅ Teste concluído!")
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("\n💡 SOLUÇÃO ALTERNATIVA:")
        print("Execute os testes individuais:")
        print("   python simulation/tests/test_response_formatter.py")
        print("   python simulation/tests/test_navigator_manual.py")
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

async def show_integration_example():
    """Mostra exemplo de integração com WhatsApp"""
    print("\n💡 EXEMPLO DE INTEGRAÇÃO COM WHATSAPP:")
    print("="*60)
    
    exemplo_codigo = """
# 1. INSTALAÇÃO NO SEU CHATBOT
from simulation.services import SimulationService

# 2. INICIALIZAR O SERVIÇO (uma vez)
simulation_service = SimulationService()

# 3. FUNÇÃO PARA PROCESSAR SIMULAÇÃO
async def processar_simulacao_consorcio(message, user_id):
    '''
    Processa uma solicitação de simulação de consórcio
    '''
    
    # Extrair dados da mensagem (você implementa o parser)
    tipo_consorcio = extrair_tipo(message)  # "Imóveis", "Veículos", etc.
    valor_credito = extrair_valor(message)  # 540000
    
    # Executar simulação
    resultado = await simulation_service.simulate_consortium(
        consortium_type=tipo_consorcio,
        credit_value=valor_credito,
        user_id=user_id
    )
    
    # Enviar resposta
    if resultado["success"]:
        # Envia mensagem formatada
        await enviar_whatsapp(user_id, resultado["formatted_response"])
        
        # Opcional: enviar cartões individuais
        for card in resultado["formatted_cards"]:
            await enviar_whatsapp(user_id, card)
    else:
        # Envia mensagem de erro amigável  
        await enviar_whatsapp(user_id, resultado["formatted_response"])

# 4. EXEMPLO DE USO NO FLUXO DE CONVERSA
async def handle_user_message(message, user_id):
    if "simular consórcio" in message.lower():
        await processar_simulacao_consorcio(message, user_id)
    elif "consórcio" in message.lower():
        await enviar_whatsapp(user_id, 
            "💡 Para simular um consórcio, envie: "
            "'Quero simular consórcio de R$ 500.000 para imóveis'"
        )
"""
    
    print(exemplo_codigo)
    
    print("\n🎯 RECURSOS DISPONÍVEIS:")
    print("-" * 30)
    recursos = [
        "✅ Simulação completa automatizada",
        "✅ Validação de parâmetros",  
        "✅ Formatação para WhatsApp",
        "✅ Tratamento de erros",
        "✅ Logs estruturados",
        "✅ Health check",
        "✅ Timeout automático",
        "✅ IDs únicos para rastreamento"
    ]
    
    for recurso in recursos:
        print(f"   {recurso}")

if __name__ == "__main__":
    asyncio.run(test_real_simulation_service())
    asyncio.run(show_integration_example()) 