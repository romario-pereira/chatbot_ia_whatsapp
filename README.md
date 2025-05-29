# 🤖 Chatbot IA WhatsApp

Um chatbot inteligente para WhatsApp que utiliza IA para processar e responder mensagens, com capacidade de RAG (Retrieval-Augmented Generation) para fornecer respostas baseadas em documentos específicos.

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Docker](#-docker)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

## ✨ Funcionalidades

- 🤖 Processamento de mensagens do WhatsApp via webhook
- 🧠 Integração com modelos de IA para processamento de linguagem natural
- 📚 Sistema RAG para respostas baseadas em documentos específicos
- 🔄 Buffer de mensagens para processamento assíncrono
- 🐳 Suporte a containerização com Docker
- 🔍 Sistema de busca vetorial para documentos

## 🛠 Tecnologias Utilizadas

- **FastAPI**: Framework web para construção da API
- **LangChain**: Framework para desenvolvimento de aplicações com IA
- **ChromaDB**: Banco de dados vetorial para armazenamento de embeddings
- **OpenAI**: Integração com modelos de IA
- **Docker**: Containerização da aplicação
- **Redis**: Sistema de buffer de mensagens
- **Python**: Linguagem principal do projeto

## 📋 Pré-requisitos

- Python 3.8+
- Docker e Docker Compose (opcional)
- Conta na OpenAI
- Acesso à API do WhatsApp (Evolution API)

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/chatbot_ia_whatsapp.git
cd chatbot_ia_whatsapp
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

1. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```env
OPENAI_API_KEY=sua_chave_api
WHATSAPP_API_URL=url_da_api_whatsapp
```

2. Configure os documentos para RAG:
   - Coloque seus documentos na pasta `rag_files/processed/`
   - Os documentos serão processados automaticamente

## 🎮 Uso

1. Inicie o servidor:
```bash
uvicorn app:app --reload
```

2. Configure o webhook no WhatsApp para apontar para:
```
http://seu-servidor/webhook
```

3. O chatbot responderá automaticamente às mensagens recebidas.

## 📁 Estrutura do Projeto

```
chatbot_ia_whatsapp/
├── app.py                 # Aplicação principal FastAPI
├── config.py             # Configurações do projeto
├── chains.py             # Definição das cadeias de processamento
├── message_buffer.py     # Sistema de buffer de mensagens
├── memory.py             # Gerenciamento de memória do chatbot
├── prompts.py            # Templates de prompts
├── vectorstore.py        # Configuração do banco de dados vetorial
├── evolution_api.py      # Integração com a API do WhatsApp
├── rag_files/           # Documentos para RAG
│   └── processed/       # Documentos processados
├── vectorstore_data/    # Dados do banco vetorial
├── requirements.txt     # Dependências do projeto
├── Dockerfile          # Configuração do Docker
└── docker-compose.yml  # Configuração do Docker Compose
```

## 🐳 Docker

Para executar com Docker:

1. Construa a imagem:
```bash
docker-compose build
```

2. Inicie os containers:
```bash
docker-compose up -d
```

## 🤝 Contribuição

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit das suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
