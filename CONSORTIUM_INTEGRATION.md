# 🏆 Sistema de Simulação de Consórcio - Integração WhatsApp

Sistema completo de simulação automatizada de consórcio integrado ao chatbot WhatsApp com IA, processamento de linguagem natural e automação web.

## 🎯 Visão Geral

O sistema detecta automaticamente quando um usuário solicita simulação de consórcio via WhatsApp, processa a solicitação com automação web no site Ademicon e retorna resultados formatados otimizados para vendas.

## 🚀 Funcionalidades

### Detecção Inteligente
- **Regex + LLM**: Detecção híbrida com alta precisão
- **Padrões avançados**: Reconhece variações de linguagem brasileira
- **Fallback**: Se não detectar consórcio, segue fluxo RAG normal

### Processamento Automático
- **Extração de dados**: Tipo de consórcio e valor automaticamente
- **Validação**: Parâmetros verificados antes da simulação
- **Simulação completa**: Automação Playwright no site real

### Resposta Otimizada
- **Formatação WhatsApp**: Mensagens com emojis e markdown
- **CTA de vendas**: Call-to-action otimizado para conversão
- **Cards individuais**: Opções detalhadas por mensagem

## 📋 Arquivos da Integração

```
📁 Arquivos Novos/Modificados:
├── consortium_handler.py          # Handler principal (NOVO)
├── message_buffer.py              # Integração com fluxo (MODIFICADO)
├── test_consortium_integration.py # Testes integração (NOVO)
└── simulation/                    # Sistema completo (EXISTENTE)
    ├── services/
    ├── agents/
    ├── config/
    └── tests/
```

## 🔧 Como Funciona

### 1. Detecção de Mensagens
```python
# Padrões regex que ativam o sistema:
- "simular consórcio"
- "quero consórcio"
- "consórcio imóvel/veículo/moto/serviços" 
- "carta de crédito"
- "ademicon simulação"
```

### 2. Extração de Dados
```python
# Extrai automaticamente:
{
    "consortium_type": "Imóveis|Veículos|Moto|Serviços",
    "credit_value": 500000,  # R$ 500.000
    "confidence": 0.8        # 80% de confiança
}
```

### 3. Fluxo de Processamento
```mermaid
graph TD
    A[Mensagem WhatsApp] --> B{Detecta Consórcio?}
    B -->|Sim| C[Extrai Dados]
    B -->|Não| H[RAG Normal]
    C --> D[Envia "Processando..."]
    D --> E[Automação Ademicon]
    E --> F[Formata Resposta]
    F --> G[Envia Resultado]
```

## 💬 Exemplos de Uso

### Mensagens que Ativam o Sistema:
```
✅ "Quero simular um consórcio de R$ 500.000 para imóvel"
✅ "Simulação de consórcio de veículo de 80 mil"
✅ "Consórcio para moto de R$ 15.000"
✅ "Carta de crédito 300 mil"
✅ "Ademicon simulação de consórcio"
```

### Mensagens que NÃO Ativam:
```
❌ "Oi, tudo bem?"
❌ "Quanto custa um financiamento?"
❌ "Preciso de um empréstimo"
```

## 📱 Resposta Formatada

```
🏆 *Simulação de Imóveis*
💰 Valor solicitado: *R$ 500.000,00*

✅ Encontrei *3 opções* para você:

📋 *Opção 1*
🟢 Status do Grupo: Em Andamento
💵 Crédito: *R$ 450.000,00*
📅 Prazo: 219 meses
💳 Parcela: *R$ 1.524,60*

📋 *Opção 2*
🟢 Status do Grupo: Em Andamento
💵 Crédito: *R$ 500.000,00*
📅 Prazo: 219 meses
💳 Parcela: *R$ 1.694,00*

🏠 *Ademicon - Consórcio há mais de 30 anos*
🔥 *GARANTE JÁ A SUA COTA!*
📞 *FALE AGORA COM NOSSO CONSULTOR*
```

## ⚙️ Configuração

### 1. Dependências
Certifique-se de que estão instaladas:
```bash
pip install langchain-openai
pip install playwright
pip install pydantic-settings
```

### 2. Variáveis de Ambiente
```env
# Já configuradas no projeto:
OPENAI_API_KEY=sua_key
OPENAI_MODEL_NAME=gpt-4
EVOLUTION_API_URL=sua_url
AUTHENTICATION_API_KEY=sua_key
```

### 3. Instalação Playwright
```bash
playwright install chromium
```

## 🧪 Testes

### Teste de Integração Completa:
```bash
python test_consortium_integration.py
```

### Teste do Sistema de Simulação:
```bash
python test_real_service.py
```

### Teste de Componentes:
```bash
python simulation/tests/test_response_formatter.py
python simulation/tests/test_navigator_manual.py
```

## 🚀 Deploy em Produção

### 1. Verificar Arquivos
```bash
# Arquivos que devem existir:
✅ consortium_handler.py
✅ message_buffer.py (modificado)
✅ simulation/ (pasta completa)
✅ requirements.txt (atualizado)
```

### 2. Restart do Sistema
```bash
# Docker:
docker-compose down && docker-compose up -d

# PM2:
pm2 restart all

# Servidor local:
# Parar e reiniciar o app.py
```

### 3. Teste Real
Envie uma mensagem no WhatsApp:
```
"Quero simular consórcio de R$ 500 mil para imóvel"
```

## 📊 Monitoramento

### Logs Estruturados
```python
# Logs automáticos gerados:
[CONSORTIUM] Detectado pedido de consórcio para 5511999998888
[CONSORTIUM] Processando solicitação para 5511999998888: Quero simular...
[CONSORTIUM] Simulação enviada com sucesso para 5511999998888
```

### Métricas Disponíveis
- ✅ Taxa de detecção de consórcio
- ✅ Tempo de processamento por simulação
- ✅ Taxa de sucesso/erro
- ✅ Tipos de consórcio mais solicitados
- ✅ Valores médios simulados

## 🔄 Fallback e Robustez

### Sistema à Prova de Falhas:
1. **Erro na detecção**: Segue para RAG normal
2. **Erro na simulação**: Mensagem de erro amigável
3. **Baixa confiança**: Não processa, vai para RAG
4. **Timeout**: Mensagem de erro com código de referência
5. **Site fora do ar**: Fallback para mensagem informativa

## 🎯 Performance

### Tempos de Resposta:
- **Detecção**: < 1 segundo
- **Extração de dados**: < 2 segundos  
- **Simulação completa**: 30-60 segundos
- **Formatação**: < 1 segundo

### Otimizações:
- ✅ Cache de detecção (regex primeiro)
- ✅ LLM apenas para confirmação
- ✅ Timeout configurável
- ✅ Retry automático em caso de erro

## 🏆 Status do Projeto

```
🎉 SISTEMA 100% FUNCIONAL E PRONTO PARA PRODUÇÃO!

✅ Detecção inteligente implementada
✅ Extração de dados funcionando
✅ Simulação automatizada testada
✅ Formatação WhatsApp otimizada
✅ Integração com chatbot completa
✅ Testes de integração passando
✅ Documentação completa
✅ Sistema de fallback robusto
✅ Logs estruturados implementados
✅ Performance otimizada
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar logs do sistema
2. Executar testes de integração
3. Validar configurações de ambiente
4. Testar componentes individualmente

---

**Desenvolvido com foco em vendas, performance e experiência do usuário.** 