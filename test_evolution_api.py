import os
import sys

# Configurar variáveis para teste local
os.environ['EVOLUTION_API_URL'] = 'http://localhost:8080'
os.environ['EVOLUTION_INSTANCE_NAME'] = 'BOT_GBC'
os.environ['AUTHENTICATION_API_KEY'] = 'paid3'

def test_evolution_api():
    """
    Teste da Evolution API com configurações locais
    """
    print("🧪 TESTE DA EVOLUTION API")
    print("=" * 50)
    
    try:
        # Importar após configurar as variáveis
        from config import EVOLUTION_API_URL, EVOLUTION_INSTANCE_NAME, EVOLUTION_AUTHENTICATION_API_KEY
        
        print(f"📡 URL: {EVOLUTION_API_URL}")
        print(f"🤖 Instance: {EVOLUTION_INSTANCE_NAME}")
        print(f"🔑 API Key: {EVOLUTION_AUTHENTICATION_API_KEY[:8]}...")
        
        # Testar importação
        from evolution_api import send_whatsapp_message
        print("✅ Importação da evolution_api: OK")
        
        # Teste básico (sem enviar mensagem real)
        print("\n🔍 Testando requisição...")
        
        import requests
        url = f'{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE_NAME}'
        headers = {
            'apikey': EVOLUTION_AUTHENTICATION_API_KEY,
            'Content-Type': 'application/json'
        }
        
        # Teste sem enviar (só verificar se API responde)
        test_url = f'{EVOLUTION_API_URL}/'
        response = requests.get(test_url)
        
        if response.status_code == 200:
            print("✅ Evolution API respondendo corretamente")
            print(f"📊 Status: {response.status_code}")
            
            # Teste de endpoint específico
            instance_url = f'{EVOLUTION_API_URL}/instance/fetchInstances'
            instance_response = requests.get(instance_url, headers={'apikey': EVOLUTION_AUTHENTICATION_API_KEY})
            
            print(f"🏢 Teste de instâncias: Status {instance_response.status_code}")
            
            if instance_response.status_code == 200:
                print("✅ API Key válida e funcionando")
                
                # Teste final - simulação de envio
                payload = {
                    'number': '5511999999999',  # Número de teste
                    'text': 'Teste de integração - Não enviar'
                }
                
                # Apenas simular - NÃO enviar realmente
                print("\n📱 Simulação de envio de mensagem:")
                print(f"   URL: {url}")
                print(f"   Payload: {payload}")
                print("   ✅ Configuração válida para envio!")
                
            else:
                print(f"❌ Problema com API Key: {instance_response.status_code}")
                print(f"   Response: {instance_response.text[:200]}")
        else:
            print(f"❌ Evolution API não respondeu corretamente: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - Evolution API não acessível")
        print("💡 Verifique se o container está rodando: docker ps")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()

def show_solutions():
    """
    Mostra soluções para problemas comuns
    """
    print("\n🛠️ SOLUÇÕES PARA PROBLEMAS COMUNS:")
    print("=" * 50)
    
    solutions = """
🔧 PROBLEMA: "evolution-api" não resolve
   SOLUÇÃO: Para testes locais, use localhost:8080
   
🔧 PROBLEMA: Connection refused
   SOLUÇÃO: Verifique se containers estão rodando
   COMANDO: docker ps
   
🔧 PROBLEMA: 401 Unauthorized
   SOLUÇÃO: Verifique API Key no .env
   
🔧 PROBLEMA: 404 Not Found
   SOLUÇÃO: Verifique se a instância BOT_GBC existe
   
🔧 SOLUÇÃO DEFINITIVA PARA DESENVOLVIMENTO:
   1. Crie arquivo .env.local com:
      EVOLUTION_API_URL=http://localhost:8080
      EVOLUTION_INSTANCE_NAME=BOT_GBC
      AUTHENTICATION_API_KEY=peid3
      
   2. Modifique config.py para carregar .env.local em desenvolvimento
   
   3. Para produção (Docker), mantenha evolution-api:8080
"""
    
    print(solutions)

if __name__ == "__main__":
    test_evolution_api()
    show_solutions() 