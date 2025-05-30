from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..exceptions.simulation_exceptions import NavigationError
from simulation.config.settings import get_settings

from playwright.async_api import async_playwright, Browser, Page

class NavigatorAgent(BaseAgent):
    """
    Agente responsável por navegar no site, preencher o formulário de simulação e extrair os resultados.
    """
    async def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # 1. Abrir navegador e acessar página
            await self._open_browser(context)
            # 2. Selecionar tipo de consórcio
            await self._select_type(context)
            # 3. Selecionar "Crédito"
            await self._select_credit_option(context)
            # 4. Ajustar slider para valor
            await self._set_credit_value(context)
            # 5. Clicar em "Simular Consórcio"
            await self._click_simulate(context)
            # 6. Preencher formulário
            await self._fill_form(context)
            # 7. Aceitar termos
            await self._accept_terms(context)
            # 8. Clicar em "Resultado"
            await self._click_result(context)
            # 9. Extrair resultados dos cartões
            context['simulation_results'] = await self._extract_results(context)
            # 10. Fechar navegador
            await self._close_browser(context)
            # 11. Passar para o próximo agente
            return await self._handle_next(context)
        except Exception as e:
            raise NavigationError(f"Erro na navegação: {e}")

    async def _open_browser(self, context: Dict[str, Any]) -> None:
        """Abre o navegador e acessa a página inicial."""
        settings = get_settings()
        playwright = await async_playwright().start()
        browser: Browser = await playwright.chromium.launch(headless=False)
        page: Page = await browser.new_page()
        await page.goto(settings.SITE_URL, timeout=60000)
        context['playwright'] = playwright
        context['browser'] = browser
        context['page'] = page

    async def _close_browser(self, context: Dict[str, Any]) -> None:
        """Fecha o navegador e encerra o Playwright."""
        try:
            if 'browser' in context:
                await context['browser'].close()
            if 'playwright' in context:
                await context['playwright'].stop()
        except Exception:
            pass

    async def _select_type(self, context: Dict[str, Any]) -> None:
        """Seleciona o tipo de consórcio no dropdown."""
        page = context['page']
        tipo = context.get('type')
        if not tipo:
            raise NavigationError("Tipo de consórcio não informado no contexto.")
        # Espera o dropdown estar disponível
        await page.wait_for_selector('select', timeout=10000)
        # Seleciona o tipo de consórcio
        await page.select_option('select', label=tipo.capitalize())

    async def _select_credit_option(self, context: Dict[str, Any]) -> None:
        """Seleciona a opção 'Crédito' usando o método moderno do Playwright."""
        page = context['page']
        print("Esperando botão Crédito...")
        credito_button = page.get_by_text("Crédito", exact=True)
        await credito_button.click()
        print("Botão Crédito clicado!")

    async def _set_credit_value(self, context: Dict[str, Any]) -> None:
        """Ajusta o slider para o valor de crédito desejado."""
        page = context['page']
        valor = context.get('credit_value')
        if not valor:
            raise NavigationError("Valor de crédito não informado no contexto.")

        # Espera o handle do slider estar disponível
        handle = await page.wait_for_selector('.irs-handle', timeout=10000)
        box = await handle.bounding_box()
        if not box:
            raise NavigationError("Não foi possível obter a posição do handle do slider.")

        # Valores mínimo e máximo do slider (ajuste conforme necessário)
        min_val = 464  # valor mínimo do slider (exemplo)
        max_val = 5671 # valor máximo do slider (exemplo)
        slider_width = 300  # largura do slider em pixels (ajuste conforme necessário)
        deslocamento = int((valor - min_val) / (max_val - min_val) * slider_width)

        await handle.hover()
        await page.mouse.down()
        await page.mouse.move(box['x'] + deslocamento, box['y'] + box['height'] // 2)
        await page.mouse.up()
        print(f"Slider ajustado para o valor: {valor}")

    async def _click_simulate(self, context: Dict[str, Any]) -> None:
        """Clica no botão 'Simular Consórcio'."""
        page = context['page']
        # Espera o botão estar disponível
        await page.wait_for_selector('button:has-text("Simular Consórcio")', timeout=10000)
        button = await page.query_selector('button:has-text("Simular Consórcio")')
        if not button:
            raise NavigationError("Botão 'Simular Consórcio' não encontrado.")
        await button.click()
        # Aguarda o formulário de dados aparecer
        await page.wait_for_selector('input[type="text"]', timeout=10000)

    async def _fill_form(self, context: Dict[str, Any]) -> None:
        """Preenche o formulário com os dados aleatórios."""
        page = context['page']
        form_data = context.get('form_data')
        if not form_data:
            raise NavigationError("Dados do formulário não encontrados no contexto.")

        # Preencher nome
        await page.get_by_role("textbox", name="Nome:").fill(form_data['nome'])
        # Preencher email
        await page.get_by_role("textbox", name="E-mail:").fill(form_data['email'])
        # Preencher telefone
        await page.get_by_role("textbox", name="Telefone:").fill(form_data['telefone'])
        # Preencher CEP
        await page.get_by_role("textbox", name="CEP:").fill(form_data['cep'])

    async def _accept_terms(self, context: Dict[str, Any]) -> None:
        """Marca o checkbox de aceitação dos termos de privacidade."""
        page = context['page']
        # Espera o checkbox estar disponível e clica no span do termo
        termo = page.locator('#cliente_form div').filter(has_text="Aceito os Termos de").locator("span")
        await termo.click()

    async def _click_result(self, context: Dict[str, Any]) -> None:
        """Clica no botão 'Resultado'."""
        page = context['page']
        # Usa o seletor moderno para o botão Resultado
        await page.get_by_role("button", name="Resultado").click()
        # Aguarda os cartões de simulação aparecerem (ajuste o seletor conforme necessário)
        await page.wait_for_selector('div:has-text("Grupo")', timeout=15000)

    async def _extract_results(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrai os resultados dos cartões de simulação."""
        return [] 