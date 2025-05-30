import asyncio
from simulation.agents.data_generator_agent import DataGeneratorAgent
from simulation.agents.navigator_agent import NavigatorAgent
from simulation.agents.response_formatter_agent import ResponseFormatterAgent

async def test_full_integration():
    """
    Teste de integração completa:
    DataGenerator -> Navigator -> ResponseFormatter
    """
    
    print("🚀 INICIANDO TESTE DE INTEGRAÇÃO COMPLETA")
    print("=" * 60)
    
    # Contexto inicial
    context = {
        "type": "Imóveis",
        "credit_value": 540000
    }
    
    try:
        # STEP 1: Gerar dados aleatórios
        print("\n📊 STEP 1: Gerando dados aleatórios...")
        data_agent = DataGeneratorAgent()
        context = await data_agent.handle(context)
        print(f"✅ Dados gerados: {context['form_data']}")
        
        # STEP 2: Executar simulação (navegação)
        print("\n🌐 STEP 2: Executando simulação no site...")
        nav_agent = NavigatorAgent()
        context = await nav_agent.handle(context)
        print(f"✅ Simulação executada: {len(context.get('simulation_results', []))} resultados")
        
        # STEP 3: Formatar resposta
        print("\n📱 STEP 3: Formatando resposta para WhatsApp...")
        formatter_agent = ResponseFormatterAgent()
        context = await formatter_agent.handle(context)
        print("✅ Resposta formatada!")
        
        # RESULTADOS FINAIS
        print("\n" + "=" * 60)
        print("📱 MENSAGEM FINAL PARA WHATSAPP:")
        print("=" * 60)
        print(context['formatted_response'])
        
        print("\n🎯 TESTE DE INTEGRAÇÃO CONCLUÍDO COM SUCESSO!")
        
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE DE INTEGRAÇÃO: {e}")
        
        # Testa formatação de erro
        formatter_agent = ResponseFormatterAgent()
        error_response = await formatter_agent._format_error_response(str(e))
        
        print("\n📱 MENSAGEM DE ERRO FORMATADA:")
        print("-" * 40)
        print(error_response)

async def test_quick_format():
    """Teste rápido apenas da formatação com dados simulados."""
    print("\n🔥 TESTE RÁPIDO - APENAS FORMATAÇÃO")
    print("=" * 50)
    
    # Simula dados de uma simulação bem-sucedida
    context = {
        "type": "Veículos",
        "credit_value": 80000,
        "simulation_results": [
            {
                'grupo': 'Em Andamento',
                'valor_credito': 'R$ 75.000,00',
                'meses': '180 meses',
                'valor_parcela': 'R$ 650,00',
                'mensagem_especial': None
            },
            {
                'grupo': 'Em Andamento',
                'valor_credito': 'R$ 80.000,00',
                'meses': '180 meses',
                'valor_parcela': 'R$ 720,00',
                'mensagem_especial': 'Parcelas reduzidas calculadas para seu perfil'
            }
        ]
    }
    
    formatter_agent = ResponseFormatterAgent()
    context = await formatter_agent.handle(context)
    
    print("📱 MENSAGEM FORMATADA:")
    print("-" * 30)
    print(context['formatted_response'])

if __name__ == "__main__":
    # Executa primeiro o teste rápido
    asyncio.run(test_quick_format())
    
    # Pergunta se quer executar o teste completo
    print("\n" + "="*60)
    resposta = input("🤔 Executar teste completo com navegação? (s/n): ")
    
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        asyncio.run(test_full_integration())
    else:
        print("✅ Teste concluído! Use o teste completo quando quiser testar a navegação.") 