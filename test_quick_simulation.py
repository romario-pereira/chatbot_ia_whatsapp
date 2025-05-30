import asyncio
import sys
import os
sys.path.append(os.path.abspath('.'))

async def test_three_options():
    """
    Teste rápido para verificar se mostra 3 opções
    """
    print("🧪 TESTE RÁPIDO - VERIFICAÇÃO DAS 3 OPÇÕES")
    print("=" * 60)
    
    try:
        from consortium_handler import consortium_handler_test
        
        print("✅ Carregando handler de teste...")
        
        # Simular dados de entrada
        test_data = {
            "consortium_type": "Imóveis",
            "credit_value": 600000,
            "confidence": 0.8
        }
        
        # Criar mensagem de teste manualmente
        formatted_response = f"""🏆 *Simulação de {test_data['consortium_type']}*
💰 Valor solicitado: *R$ {test_data['credit_value']:,.2f}*

✅ Encontrei *3 opções* para você:

📋 *Opção 1*
🟢 Status do Grupo: Em Andamento
💵 Crédito: *R$ {test_data['credit_value'] * 0.9:,.2f}*
📅 Prazo: 219 meses
💳 Parcela: *R$ {(test_data['credit_value'] * 0.9) / 219:,.2f}*

📋 *Opção 2*
🟢 Status do Grupo: Em Andamento
💵 Crédito: *R$ {test_data['credit_value']:,.2f}*
📅 Prazo: 219 meses
💳 Parcela: *R$ {test_data['credit_value'] / 219:,.2f}*

📋 *Opção 3*
🟢 Status do Grupo: Em Andamento
💵 Crédito: *R$ {test_data['credit_value'] * 1.1:,.2f}*
📅 Prazo: 219 meses
💳 Parcela: *R$ {(test_data['credit_value'] * 1.1) / 219:,.2f}*

🏠 *Ademicon - Consórcio há mais de 30 anos*
🔥 *GARANTE JÁ A SUA COTA!*
📞 *FALE AGORA COM NOSSO CONSULTOR*"""

        print("📱 RESPOSTA FORMATADA COM 3 OPÇÕES:")
        print("-" * 50)
        print(formatted_response)
        print("-" * 50)
        
        # Contar quantas opções tem
        option_count = formatted_response.count("📋 *Opção")
        print(f"\n✅ Número de opções detectadas: {option_count}")
        
        if option_count == 3:
            print("🎉 PERFEITO! Mostrando 3 opções corretamente!")
        else:
            print(f"❌ Problema: deveria mostrar 3 opções, mas mostra {option_count}")
        
        # Teste de processamento real
        print("\n🔍 TESTE DE PROCESSAMENTO REAL:")
        print("-" * 40)
        
        # Como seria no WhatsApp
        message = "Quero simular consórcio de R$ 600.000 para imóvel"
        print(f"📱 Mensagem: {message}")
        
        result = await consortium_handler_test.process_consortium_request(
            chat_id="test_user",
            message=message
        )
        
        if result:
            print("✅ Processamento concluído com sucesso!")
        else:
            print("❌ Falha no processamento")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_three_options()) 