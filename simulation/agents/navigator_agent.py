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
        page = context['page']
        resultados = []
        
        try:
            # Lista de seletores possíveis para os cartões
            possible_selectors = [
                '[data-aos="fade-up"]',
                'div:has-text("Grupo:"):has-text("R$")',
                'div:has-text("Valor do crédito")',
                '.card:has-text("Grupo")',
                '.simulation-result',
                'div:has-text("meses"):has-text("R$")'
            ]
            
            cartoes = None
            selector_usado = None
            
            for selector in possible_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=3000)
                    cartoes_temp = await page.locator(selector).all()
                    if cartoes_temp and len(cartoes_temp) > 0:
                        # Filtra apenas cartões com conteúdo substancial
                        cartoes_validos = []
                        for cartao in cartoes_temp:
                            texto = await cartao.text_content()
                            if texto and len(texto.strip()) > 50 and 'R$' in texto:
                                cartoes_validos.append(cartao)
                        
                        if cartoes_validos:
                            cartoes = cartoes_validos
                            selector_usado = selector
                            print(f"Usando seletor: {selector} - {len(cartoes)} cartões encontrados")
                            break
                except:
                    continue
            
            if not cartoes:
                print("Nenhum seletor funcionou, usando método fallback...")
                return await self._extract_results_fallback(page)
            
            # Processa os cartões encontrados
            valores_processados = set()
            
            for idx, cartao in enumerate(cartoes):
                if len(resultados) >= 3:  # Máximo 3 resultados
                    break
                    
                try:
                    texto_completo = await cartao.text_content()
                    print(f"Analisando cartão {idx}...")
                    
                    if not texto_completo or len(texto_completo.strip()) < 50:
                        continue
                    
                    # Verifica se contém informações de simulação (removido % da verificação)
                    palavras_chave = ['R$', 'meses']
                    if not any(palavra in texto_completo for palavra in palavras_chave):
                        continue
                    
                    resultado = await self._parse_card_text(cartao, texto_completo)
                    
                    # Evita duplicatas baseadas no valor do crédito
                    if resultado['valor_credito'] in valores_processados or resultado['valor_credito'] == 'N/A':
                        continue
                    
                    valores_processados.add(resultado['valor_credito'])
                    resultados.append(resultado)
                    print(f"✓ Resultado válido: {resultado}")
                        
                except Exception as e:
                    print(f"Erro ao processar cartão {idx}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Erro geral na extração: {e}")
            return await self._extract_results_fallback(page)
        
        print(f"Total de resultados únicos extraídos: {len(resultados)}")
        return resultados if resultados else await self._extract_results_fallback(page)
    
    async def _parse_card_text(self, cartao, texto_completo: str) -> Dict[str, Any]:
        """Parseia o texto do cartão para extrair as informações."""
        import re
        
        # Inicializa resultado com estrutura simplificada
        resultado = {
            'grupo': 'Em Andamento',  # Sempre será "Em Andamento"
            'valor_credito': 'N/A',
            'meses': 'N/A',
            'valor_parcela': 'N/A',
            'mensagem_especial': None  # Para mensagens especiais como "Parcelas reduzidas"
        }
        
        # Busca por mensagem especial de parcelas reduzidas
        if 'Parcelas reduzidas calculadas' in texto_completo:
            # Extrai o parágrafo completo que contém essa mensagem
            mensagem_match = re.search(r'Parcelas reduzidas calculadas[^.]*\.?[^.]*\.?', texto_completo, re.IGNORECASE)
            if mensagem_match:
                resultado['mensagem_especial'] = mensagem_match.group(0).strip()
        
        # Valores em R$ - busca padrões mais específicos
        valores_pattern = r'R\$\s*([\d.,]+(?:\.\d{3})*(?:,\d{2})?)'
        valores_r = re.findall(valores_pattern, texto_completo)
        
        if len(valores_r) >= 2:
            # Primeiro valor é geralmente o crédito, segundo é a parcela
            resultado['valor_credito'] = f"R$ {valores_r[0]}"
            resultado['valor_parcela'] = f"R$ {valores_r[1]}"
        elif len(valores_r) == 1:
            # Se só tem um valor, assumir que é o crédito
            resultado['valor_credito'] = f"R$ {valores_r[0]}"
        
        # Meses - busca padrão específico
        meses_match = re.search(r'(\d+)\s*meses', texto_completo, re.IGNORECASE)
        if meses_match:
            resultado['meses'] = f"{meses_match.group(1)} meses"
        
        return resultado
    
    async def _extract_results_fallback(self, page: Page) -> List[Dict[str, Any]]:
        """Método fallback para extrair resultados quando os seletores primários falham."""
        print("Executando extração fallback...")
        resultados = []
        
        try:
            # Captura todo o HTML da página
            page_content = await page.content()
            page_text = await page.locator('body').text_content()
            
            import re
            
            print("Analisando texto da página...")
            
            # Busca por padrões específicos de valores em R$
            valores_credito = re.findall(r'R\$\s*([\d.,]+(?:\.\d{3})*(?:,\d{2})?)', page_text)
            
            # Busca por meses
            meses_encontrados = re.findall(r'(\d+)\s*meses', page_text, re.IGNORECASE)
            
            # Busca por mensagem especial
            mensagem_especial = None
            if 'Parcelas reduzidas calculadas' in page_text:
                mensagem_match = re.search(r'Parcelas reduzidas calculadas[^.]*\.?[^.]*\.?', page_text, re.IGNORECASE)
                if mensagem_match:
                    mensagem_especial = mensagem_match.group(0).strip()
            
            print(f"Encontrado: {len(valores_credito)} valores, {len(meses_encontrados)} meses")
            if mensagem_especial:
                print(f"Mensagem especial encontrada: {mensagem_especial}")
            
            # Se encontrou dados suficientes, monta os resultados
            if len(valores_credito) >= 6:  # Pelo menos 3 pares (crédito + parcela)
                valores_unicos = []
                
                # Agrupa valores em pares únicos
                for i in range(0, len(valores_credito)-1, 2):
                    if len(valores_unicos) >= 3:
                        break
                    
                    credito = f"R$ {valores_credito[i]}"
                    parcela = f"R$ {valores_credito[i+1]}"
                    
                    # Verifica se já existe esse valor de crédito
                    if not any(r['valor_credito'] == credito for r in valores_unicos):
                        resultado = {
                            'grupo': 'Em Andamento',  # Sempre será "Em Andamento"
                            'valor_credito': credito,
                            'meses': f"{meses_encontrados[len(valores_unicos)]} meses" if len(valores_unicos) < len(meses_encontrados) else 'N/A',
                            'valor_parcela': parcela,
                            'mensagem_especial': mensagem_especial  # Adiciona a mensagem especial se encontrada
                        }
                        valores_unicos.append(resultado)
                
                resultados = valores_unicos
            
            if not resultados:
                # Último recurso: resultado de erro
                resultados = [{
                    'grupo': 'Erro na extração',
                    'valor_credito': 'N/A',
                    'meses': 'N/A',
                    'valor_parcela': 'N/A',
                    'mensagem_especial': None
                }]
                
        except Exception as e:
            print(f"Erro no fallback: {e}")
            resultados = [{
                'grupo': 'Erro na extração',
                'valor_credito': 'N/A',
                'meses': 'N/A',
                'valor_parcela': 'N/A',
                'mensagem_especial': None
            }]
        
        print(f"Fallback retornou {len(resultados)} resultados")
        return resultados 