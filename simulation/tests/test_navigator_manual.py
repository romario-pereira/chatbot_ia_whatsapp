import asyncio
from simulation.agents.navigator_agent import NavigatorAgent
from simulation.agents.data_generator_agent import DataGeneratorAgent
from typing import Dict, Any

async def main():
    # Exemplo de contexto
    context = {
        "type": "Imóveis",  # ou "Serviços", "Moto", "Veículos"
        "credit_value": 540000
    }
    # Gera dados aleatórios
    data_agent = DataGeneratorAgent()
    context = await data_agent.handle(context)
    # Executa o fluxo de navegação até o clique em Resultado
    nav_agent = NavigatorAgent()
    try:
        await nav_agent._open_browser(context)
        await nav_agent._select_type(context)
        await nav_agent._select_credit_option(context)
        await nav_agent._set_credit_value(context)
        await nav_agent._click_simulate(context)
        await nav_agent._fill_form(context)
        await nav_agent._accept_terms(context)
        await nav_agent._click_result(context)
        # Extrai e imprime os resultados
        resultados = await nav_agent._extract_results(context)
        print("Resultados extraídos:")
        for r in resultados:
            print(r)
    finally:
        await nav_agent._close_browser(context)

if __name__ == "__main__":
    asyncio.run(main()) 