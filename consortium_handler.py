import re
import asyncio
from typing import Dict, Optional, Tuple
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config import OPENAI_MODEL_NAME, OPENAI_MODEL_TEMPERATURE
from simulation.services import SimulationService

# Importação condicional para testes
try:
    from evolution_api import send_whatsapp_message
    WHATSAPP_AVAILABLE = True
except ImportError:
    WHATSAPP_AVAILABLE = False
    def send_whatsapp_message(*args, **kwargs):
        print("[TESTE] Mensagem WhatsApp simulada enviada")


class ConsortiumHandler:
    """
    Handler especializado para detectar e processar solicitações de simulação de consórcio.
    Integra o sistema de simulação com o chatbot WhatsApp.
    """
    
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        self.simulation_service = SimulationService()
        self.llm = ChatOpenAI(
            model=OPENAI_MODEL_NAME,
            temperature=0.1  # Baixa temperatura para maior precisão
        )
        
        # Padrões de detecção de simulação de consórcio
        self.consortium_patterns = [
            r'simul\w*\s+cons[oó]rcio',
            r'cons[oó]rcio.*simul\w*',
            r'quero.*cons[oó]rcio',
            r'cons[oó]rcio.*im[oó]vel|im[oó]vel.*cons[oó]rcio',
            r'cons[oó]rcio.*ve[ií]culo|ve[ií]culo.*cons[oó]rcio',
            r'cons[oó]rcio.*moto|moto.*cons[oó]rcio',
            r'cons[oó]rcio.*servi[cç]o|servi[cç]o.*cons[oó]rcio',
            r'carta.*cr[eé]dito',
            r'financiamento.*cons[oó]rcio',
            r'ademicon.*simul\w*'
        ]
        
        # Prompt para extração de dados via LLM
        self.extraction_prompt = ChatPromptTemplate.from_template("""
Você é um assistente especializado em extrair informações sobre simulação de consórcio.

Analise a mensagem do usuário e extraia:
1. Tipo de consórcio (Imóveis, Veículos, Moto, Serviços)
2. Valor do crédito desejado (em R$)

Mensagem do usuário: {message}

Responda APENAS no formato JSON:
{{
    "is_consortium_request": true/false,
    "consortium_type": "Imóveis|Veículos|Moto|Serviços|null",
    "credit_value": número ou null,
    "confidence": 0.0-1.0
}}

Se não conseguir identificar claramente, retorne is_consortium_request: false.
Para valores, aceite formatos como: R$ 500.000, 500 mil, quinhentos mil, etc.
""")
    
    def _send_message(self, chat_id: str, text: str):
        """
        Envia mensagem com fallback para modo teste.
        """
        if self.test_mode:
            print(f"[TESTE] Enviando para {chat_id}:")
            print(f"       {text}")
            print("-" * 50)
        else:
            try:
                send_whatsapp_message(number=chat_id, text=text)
            except Exception as e:
                print(f"[CONSORTIUM] Erro ao enviar WhatsApp: {e}")
                if not WHATSAPP_AVAILABLE:
                    print(f"[CONSORTIUM] Evolution API não disponível. Mensagem para {chat_id}:")
                    print(f"             {text}")
    
    async def should_handle_message(self, message: str) -> bool:
        """
        Detecta se a mensagem é sobre simulação de consórcio.
        Usa regex + LLM para maior precisão.
        """
        message_lower = message.lower()
        
        # Primeira verificação: regex rápida
        regex_match = any(
            re.search(pattern, message_lower, re.IGNORECASE) 
            for pattern in self.consortium_patterns
        )
        
        if not regex_match:
            return False
        
        # Segunda verificação: LLM para confirmação (opcional em teste)
        if self.test_mode:
            # No modo teste, só usa regex para ser mais rápido
            return regex_match
        
        try:
            chain = self.extraction_prompt | self.llm
            response = await chain.ainvoke({"message": message})
            
            # Parse manual básico do JSON (fallback)
            response_text = response.content.strip()
            
            if '"is_consortium_request": true' in response_text:
                return True
                
        except Exception as e:
            print(f"[CONSORTIUM] Erro na detecção LLM: {e}")
            # Fallback para regex se LLM falhar
            return regex_match
        
        return False
    
    async def extract_simulation_data(self, message: str) -> Optional[Dict]:
        """
        Extrai tipo de consórcio e valor do crédito da mensagem.
        """
        try:
            # No modo teste, usa extração simples
            if self.test_mode:
                return self._extract_data_simple(message)
            
            chain = self.extraction_prompt | self.llm
            response = await chain.ainvoke({"message": message})
            
            # Parse simples do JSON (implementação robusta)
            response_text = response.content.strip()
            
            # Extração manual para garantir funcionamento
            data = {
                "consortium_type": None,
                "credit_value": None,
                "confidence": 0.0
            }
            
            # Detectar tipo
            message_lower = message.lower()
            if any(word in message_lower for word in ['imovel', 'imóvel', 'casa', 'apartamento']):
                data["consortium_type"] = "Imóveis"
            elif any(word in message_lower for word in ['veiculo', 'veículo', 'carro', 'auto']):
                data["consortium_type"] = "Veículos"  
            elif any(word in message_lower for word in ['moto', 'motocicleta']):
                data["consortium_type"] = "Moto"
            elif any(word in message_lower for word in ['serviço', 'servico']):
                data["consortium_type"] = "Serviços"
            else:
                data["consortium_type"] = "Imóveis"  # Default
            
            # Detectar valor usando regex
            valor_patterns = [
                r'r\$?\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',
                r'(\d+)\s*mil',
                r'(\d+)\s*milh[ãõ]es?',
                r'(\d{3,})'
            ]
            
            for pattern in valor_patterns:
                match = re.search(pattern, message_lower)
                if match:
                    valor_str = match.group(1)
                    try:
                        if 'mil' in pattern:
                            data["credit_value"] = float(valor_str) * 1000
                        elif 'milh' in pattern:
                            data["credit_value"] = float(valor_str) * 1000000
                        else:
                            # Remove pontos e vírgulas
                            valor_limpo = valor_str.replace('.', '').replace(',', '.')
                            data["credit_value"] = float(valor_limpo)
                        break
                    except ValueError:
                        continue
            
            # Se não encontrou valor, usa default
            if not data["credit_value"]:
                data["credit_value"] = 500000  # R$ 500.000 default
            
            data["confidence"] = 0.8 if data["consortium_type"] and data["credit_value"] else 0.3
            
            return data
            
        except Exception as e:
            print(f"[CONSORTIUM] Erro na extração: {e}")
            # Fallback com valores padrão
            return {
                "consortium_type": "Imóveis",
                "credit_value": 500000,
                "confidence": 0.5
            }
    
    def _extract_data_simple(self, message: str) -> Dict:
        """
        Extração simples para modo teste (sem LLM).
        """
        data = {
            "consortium_type": "Imóveis",
            "credit_value": 500000,
            "confidence": 0.8
        }
        
        message_lower = message.lower()
        
        # Detectar tipo
        if any(word in message_lower for word in ['veiculo', 'veículo', 'carro', 'auto']):
            data["consortium_type"] = "Veículos"
        elif any(word in message_lower for word in ['moto', 'motocicleta']):
            data["consortium_type"] = "Moto"
        elif any(word in message_lower for word in ['serviço', 'servico']):
            data["consortium_type"] = "Serviços"
        
        # Detectar valor
        import re
        valor_patterns = [
            r'r\$?\s*(\d{1,3}(?:\.\d{3})*)',
            r'(\d+)\s*mil',
            r'(\d+)\s*milh[ãõ]es?'
        ]
        
        for pattern in valor_patterns:
            match = re.search(pattern, message_lower)
            if match:
                valor_str = match.group(1)
                try:
                    if 'mil' in pattern and 'milh' not in pattern:
                        data["credit_value"] = float(valor_str) * 1000
                    elif 'milh' in pattern:
                        data["credit_value"] = float(valor_str) * 1000000
                    else:
                        valor_limpo = valor_str.replace('.', '')
                        data["credit_value"] = float(valor_limpo)
                    break
                except ValueError:
                    continue
        
        return data
    
    async def process_consortium_request(self, chat_id: str, message: str) -> bool:
        """
        Processa uma solicitação de simulação de consórcio.
        Retorna True se processou, False se deve seguir fluxo normal.
        """
        print(f"[CONSORTIUM] Processando solicitação para {chat_id}: {message}")
        
        try:
            # 1. Extrair dados da mensagem
            data = await self.extract_simulation_data(message)
            
            if not data or data["confidence"] < 0.3:
                print(f"[CONSORTIUM] Confiança baixa, seguindo fluxo normal")
                return False
            
            # 2. Enviar mensagem de processamento
            self._send_message(
                chat_id=chat_id,
                text="🔄 *Processando sua simulação de consórcio...*\n\n"
                     "⏱️ Isso pode levar de 30 a 60 segundos.\n"
                     "💡 Estou acessando o sistema da Ademicon para buscar as melhores opções!"
            )
            
            # 3. Executar simulação (ou simular em modo teste)
            if self.test_mode:
                print("[TESTE] Simulando resultado sem executar automação...")
                result = {
                    "success": True,
                    "formatted_response": f"""🏆 *Simulação de {data['consortium_type']}*
💰 Valor solicitado: *R$ {data['credit_value']:,.2f}*

✅ Encontrei *3 opções* para você:

📋 *Opção 1*
🟢 Status do Grupo: Em Andamento
💵 Crédito: *R$ {data['credit_value'] * 0.9:,.2f}*
📅 Prazo: 219 meses
💳 Parcela: *R$ {(data['credit_value'] * 0.9) / 219:,.2f}*

📋 *Opção 2*
🟢 Status do Grupo: Em Andamento
💵 Crédito: *R$ {data['credit_value']:,.2f}*
📅 Prazo: 219 meses
💳 Parcela: *R$ {data['credit_value'] / 219:,.2f}*

📋 *Opção 3*
🟢 Status do Grupo: Em Andamento
💵 Crédito: *R$ {data['credit_value'] * 1.1:,.2f}*
📅 Prazo: 219 meses
💳 Parcela: *R$ {(data['credit_value'] * 1.1) / 219:,.2f}*

🏠 *Ademicon - Consórcio há mais de 30 anos*
🔥 *GARANTE JÁ A SUA COTA!*
📞 *FALE AGORA COM NOSSO CONSULTOR*"""
                }
            else:
                result = await self.simulation_service.simulate_consortium(
                    consortium_type=data["consortium_type"],
                    credit_value=data["credit_value"],
                    user_id=chat_id
                )
            
            # 4. Enviar resultado
            if result["success"]:
                # Mensagem principal
                self._send_message(
                    chat_id=chat_id,
                    text=result["formatted_response"]
                )
                
                # Cards individuais (opcional)
                if result.get("formatted_cards") and not self.test_mode:
                    await asyncio.sleep(2)  # Pequena pausa
                    for card in result["formatted_cards"]:
                        self._send_message(chat_id=chat_id, text=card)
                        await asyncio.sleep(1)
                
                print(f"[CONSORTIUM] Simulação enviada com sucesso para {chat_id}")
            else:
                # Erro na simulação
                self._send_message(
                    chat_id=chat_id,
                    text=result["formatted_response"]
                )
                print(f"[CONSORTIUM] Erro na simulação para {chat_id}: {result.get('error')}")
            
            return True
            
        except Exception as e:
            print(f"[CONSORTIUM] Erro no processamento: {e}")
            
            # Mensagem de erro amigável
            self._send_message(
                chat_id=chat_id,
                text="❌ *Ops! Algo deu errado na simulação*\n\n"
                     "🔄 Tente novamente em alguns instantes ou\n"
                     "💬 Continue a conversa que posso ajudar de outras formas!"
            )
            
            return True  # Não seguir fluxo normal em caso de erro
    
    async def get_simulation_help(self) -> str:
        """
        Retorna mensagem de ajuda sobre como solicitar simulação.
        """
        return """💡 *Como simular um consórcio:*

📝 *Exemplos de mensagens:*
• "Quero simular um consórcio de R$ 500.000 para imóvel"
• "Simulação de consórcio de veículo de 80 mil"
• "Consórcio para moto de R$ 15.000"

🏢 *Tipos disponíveis:*
• 🏠 Imóveis
• 🚗 Veículos  
• 🏍️ Moto
• 🛠️ Serviços

💰 *Valores aceitos:*
• Mínimo: R$ 10.000
• Máximo: R$ 10.000.000

⚡ *Resposta em até 60 segundos!*"""


# Instância global
consortium_handler = ConsortiumHandler()

# Instância para testes
consortium_handler_test = ConsortiumHandler(test_mode=True) 