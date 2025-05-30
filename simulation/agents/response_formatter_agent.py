from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..exceptions.simulation_exceptions import FormattingError
from datetime import datetime

class ResponseFormatterAgent(BaseAgent):
    """
    Agente responsável por formatar os resultados da simulação em mensagens 
    bonitas e legíveis para envio no WhatsApp.
    """
    
    async def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            simulation_results = context.get('simulation_results', [])
            if not simulation_results:
                raise FormattingError("Nenhum resultado de simulação encontrado no contexto")
            
            # Formata a resposta principal
            context['formatted_response'] = await self._format_main_response(context)
            
            # Formata respostas individuais para cada cartão (opcional)
            context['formatted_cards'] = await self._format_individual_cards(simulation_results)
            
            # Passa para o próximo agente se houver
            return await self._handle_next(context)
            
        except Exception as e:
            raise FormattingError(f"Erro ao formatar resposta: {e}")
    
    async def _format_main_response(self, context: Dict[str, Any]) -> str:
        """Formata a resposta principal com todos os resultados."""
        simulation_results = context.get('simulation_results', [])
        tipo_consorcio = context.get('type', 'Consórcio')
        valor_solicitado = context.get('credit_value', 0)
        
        # Cabeçalho da mensagem
        response = f"🏆 *Simulação de {tipo_consorcio}*\n"
        response += f"💰 Valor solicitado: *R$ {valor_solicitado:,.2f}*\n\n"
        
        if not simulation_results or len(simulation_results) == 0:
            response += "❌ Não foi possível gerar simulações para os valores solicitados.\n"
            response += "Tente com um valor diferente."
            return response
        
        response += f"✅ Encontrei *{len(simulation_results)} opções* para você:\n\n"
        
        # Adiciona cada resultado
        for idx, resultado in enumerate(simulation_results, 1):
            response += await self._format_single_result(idx, resultado)
            response += "\n"
        
        # Mensagem especial se algum resultado tiver
        mensagem_especial = self._get_special_message(simulation_results)
        if mensagem_especial:
            response += f"ℹ️ *Informação importante:*\n{mensagem_especial}\n\n"
        
        # Rodapé
        response += self._get_footer()
        
        return response
    
    async def _format_single_result(self, numero: int, resultado: Dict[str, Any]) -> str:
        """Formata um único resultado de simulação."""
        grupo = resultado.get('grupo', 'N/A')
        valor_credito = resultado.get('valor_credito', 'N/A')
        meses = resultado.get('meses', 'N/A')
        valor_parcela = resultado.get('valor_parcela', 'N/A')
        
        response = f"📋 *Opção {numero}*\n"
        response += f"🟢 Status do Grupo: {grupo}\n"
        response += f"💵 Crédito: *{valor_credito}*\n"
        response += f"📅 Prazo: {meses}\n"
        response += f"💳 Parcela: *{valor_parcela}*\n"
        
        return response
    
    async def _format_individual_cards(self, simulation_results: List[Dict[str, Any]]) -> List[str]:
        """Formata cada resultado como uma mensagem individual (para envios separados)."""
        cards = []
        
        for idx, resultado in enumerate(simulation_results, 1):
            card = f"🎯 *Simulação {idx}*\n\n"
            card += await self._format_single_result(1, resultado)  # Sempre usa número 1 para cards individuais
            card += "\n" + self._get_footer()
            cards.append(card)
        
        return cards
    
    def _get_special_message(self, simulation_results: List[Dict[str, Any]]) -> str:
        """Extrai mensagem especial se algum resultado tiver."""
        for resultado in simulation_results:
            mensagem = resultado.get('mensagem_especial')
            if mensagem:
                return mensagem
        return ""
    
    def _get_footer(self) -> str:
        """Retorna o rodapé padrão das mensagens."""
        return ("🏠 *Ademicon - Consórcio há mais de 30 anos*\n"
                "✨ Sem juros | 🏦 Use seu FGTS | 📈 Parcelas reduzidas\n\n"
                "🔥 *GARANTE JÁ A SUA COTA!*\n"
                "💰 Condições especiais por tempo limitado\n"
                "🚀 Aprovação rápida e sem burocracia\n\n"
                "📞 *FALE AGORA COM NOSSO CONSULTOR*\n"
                "✅ Tire suas dúvidas e contrate 100% digital!")
    
    async def _format_error_response(self, error_message: str) -> str:
        """Formata uma resposta de erro amigável."""
        response = "❌ *Ops! Algo deu errado*\n\n"
        response += f"Não consegui processar sua simulação no momento.\n"
        response += f"Motivo: {error_message}\n\n"
        response += "🔄 Tente novamente em alguns instantes ou\n"
        response += "💬 Fale diretamente com nosso especialista!\n\n"
        response += self._get_footer()
        return response
    
    async def _format_summary_response(self, context: Dict[str, Any]) -> str:
        """Formata uma resposta resumida (para casos com muitos resultados)."""
        simulation_results = context.get('simulation_results', [])
        tipo_consorcio = context.get('type', 'Consórcio')
        
        if not simulation_results:
            return await self._format_error_response("Nenhum resultado encontrado")
        
        # Pega o resultado com menor e maior valor
        menor_parcela = min(simulation_results, 
                           key=lambda x: float(x.get('valor_parcela', '0').replace('R$ ', '').replace('.', '').replace(',', '.')))
        maior_credito = max(simulation_results,
                           key=lambda x: float(x.get('valor_credito', '0').replace('R$ ', '').replace('.', '').replace(',', '.')))
        
        response = f"🎯 *Resumo - {tipo_consorcio}*\n\n"
        response += f"💰 Maior crédito: *{maior_credito.get('valor_credito')}*\n"
        response += f"💳 Menor parcela: *{menor_parcela.get('valor_parcela')}*\n"
        response += f"📊 Total de opções: *{len(simulation_results)}*\n\n"
        response += "💬 Quer ver todas as opções detalhadas?\n"
        response += "Responda 'sim' para ver a simulação completa!\n\n"
        response += self._get_footer()
        
        return response 