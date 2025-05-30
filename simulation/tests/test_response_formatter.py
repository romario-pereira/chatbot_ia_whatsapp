import asyncio
from simulation.agents.response_formatter_agent import ResponseFormatterAgent

async def test_response_formatter():
    # Dados simulados de exemplo (similares ao que vem do NavigatorAgent)
    context = {
        "type": "Imóveis",
        "credit_value": 540000,
        "simulation_results": [
            {
                'grupo': 'Em Andamento',
                'valor_credito': 'R$ 450.000,00',
                'meses': '219 meses',
                'valor_parcela': 'R$ 1.524,60',
                'mensagem_especial': None
            },
            {
                'grupo': 'Em Andamento',
                'valor_credito': 'R$ 500.000,00',
                'meses': '219 meses',
                'valor_parcela': 'R$ 1.694,00',
                'mensagem_especial': None
            },
            {
                'grupo': 'Em Andamento',
                'valor_credito': 'R$ 550.000,00',
                'meses': '219 meses',
                'valor_parcela': 'R$ 1.863,40',
                'mensagem_especial': 'Parcelas reduzidas calculadas com desconto especial'
            }
        ]
    }
    
    # Testa o ResponseFormatterAgent
    formatter = ResponseFormatterAgent()
    result_context = await formatter.handle(context)
    
    print("=" * 50)
    print("TESTE DO RESPONSE FORMATTER AGENT")
    print("=" * 50)
    
    print("\n📱 MENSAGEM PRINCIPAL:")
    print("-" * 30)
    print(result_context['formatted_response'])
    
    print("\n📋 MENSAGENS INDIVIDUAIS:")
    print("-" * 30)
    for i, card in enumerate(result_context['formatted_cards'], 1):
        print(f"\n--- Card {i} ---")
        print(card)
    
    print("\n✅ Teste concluído com sucesso!")

async def test_error_formatting():
    """Testa formatação de erro."""
    context = {
        "type": "Imóveis",
        "credit_value": 540000,
        "simulation_results": []  # Lista vazia para simular erro
    }
    
    formatter = ResponseFormatterAgent()
    
    try:
        await formatter.handle(context)
    except Exception as e:
        error_response = await formatter._format_error_response(str(e))
        print("\n❌ MENSAGEM DE ERRO:")
        print("-" * 30)
        print(error_response)

if __name__ == "__main__":
    asyncio.run(test_response_formatter())
    asyncio.run(test_error_formatting()) 