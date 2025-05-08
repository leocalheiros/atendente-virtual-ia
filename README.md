# Atende Virtual - IA

O projeto é uma POC de um chatbot baseado em inteligência artificial que utiliza a API da OpenAI, LangChain, e FAISS para fornecer respostas contextuais com base em uma base de conhecimento armazenada em um arquivo CSV. O histórico de conversas é gerenciado usando Redis, e a interação com usuários ocorre via um webhook integrado à Evolution API para envio de mensagens.

O projeto segue um Clean Architeture básico, organizando o código em camadas (domínio, aplicação, infraestrutura, e apresentação).

## Funcionalidades

- Processamento de mensagens de usuários via webhook.
- Geração de respostas contextuais usando LangChain e embeddings da OpenAI.
- Armazenamento do histórico de conversas no Redis com limite de 5 interações por usuário.
- Cache de índices FAISS para otimizar o carregamento da base de conhecimento.
- Tratamento de erros robusto e logging detalhado.
- Configurações centralizadas via variáveis de ambiente.

## Tecnologias Utilizadas

- **Python 3.8+**
- **Flask**: Framework web para o endpoint webhook.
- **LangChain**: Framework para integração com modelos de linguagem.
- **OpenAI**: API para embeddings e geração de respostas.
- **FAISS**: Biblioteca para busca eficiente de vetores (base de conhecimento).
- **Redis**: Banco de dados em memória para armazenamento do histórico.
- **Evolution API**: Integração para envio e recebimento de mensagens.
- **PostgreSQL**: Banco de dados usado pela Evolution API.
- **Docker Compose**: Orquestração de serviços (Evolution API, Redis, PostgreSQL).
- **Tenacity**: Biblioteca para retries em chamadas à API.
- **Python-dotenv**: Gerenciamento de variáveis de ambiente.

## Estrutura do Projeto

```
project_root/
│
├── src/
│   ├── config/          # Configurações e variáveis de ambiente
│   ├── domain/          # Entidades e serviços do domínio
│   ├── application/     # Casos de uso da aplicação
│   ├── infrastructure/  # Integrações com Redis, LangChain, OpenAI, etc.
│   ├── presentation/    # Endpoint Flask
│   └── utils/           # Utilitários (ex.: logging)
├── .env                 # Variáveis de ambiente
├── docker-compose.yml   # Configuração de serviços (Evolution API, Redis, PostgreSQL)
├── main.py              # Ponto de entrada da aplicação
├── requirements.txt     # Dependências
└── README.md            # Documentação do projeto
```

## Pré-requisitos

- Python 3.8 ou superior
- Docker e Docker Compose instalados
- Chave de API da OpenAI válida
- Arquivo `Q&A.csv` com a base de conhecimento (formato esperado: perguntas e respostas)

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/atendente-virtual-ia
   cd atendente-virtual-ia
   ```

2. **Crie e ative um ambiente virtual**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**:
   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
   ```
   REDIS_HOST=redis
   REDIS_PORT=6379
   REDIS_DB=0
   CONTEXT_EXPIRY_SECONDS=86400
   CSV_FILE_PATH=Q&A.csv
   FLASK_PORT=5000
   FAISS_INDEX_PATH=faiss_index
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Prepare a base de conhecimento**:
   - Coloque o arquivo `Q&A.csv` no diretório raiz ou especifique o caminho correto em `CSV_FILE_PATH`.
   - Formato esperado do CSV: colunas com perguntas e respostas (ex.: `question,answer`).

## Configurando os Serviços com Docker Compose

O projeto inclui um arquivo `docker-compose.yml` para orquestrar os serviços necessários: Evolution API, Redis, e PostgreSQL.

1. **Inicie os serviços**:
   ```bash
   docker-compose up -d
   ```
   Isso iniciará:
   - **Evolution API**: Disponível em `http://localhost:8080`.
   - **Redis**: Disponível em `redis:6379`.
   - **PostgreSQL**: Disponível em `localhost:5441` (mapeado para a porta 5432 internamente).

2. **Verifique os serviços**:
   - Confirme que o Redis está ativo:
     ```bash
     docker exec -it redis redis-cli ping
     ```
     Deve retornar `PONG`.
   - Acesse o painel da Evolution API (se disponível) em `http://localhost:8080` para verificar o status.

3. **Conecte a instância do whatsapp na Evolution API**:
   - Acesse a interface administrativa da Evolution API em `http://localhost:8080/manager`
   - Crie uma instância e deixe o channel como "Baileys"
   - Guarde o token

4. **Configure o webhook na Evolution API**:
   - Acesse a interface administrativa da Evolution API em `http://localhost:8080/manager`
   - Configure o webhook com a URL do seu aplicativo Flask em Events -> Webhook -> URL e ative as opções: "Enabled" e "Webhook Base64":
     ```
     http://host:5000/webhook
     ```
     Substitua `host` pelo endereço do seu servidor (ex.: `localhost` para testes locais ou o IP/nome do domínio em produção).
   - Habilite o evento `CHATS_UPSERT` nos eventos da Evolution API para garantir que as mensagens recebidas sejam enviadas ao webhook.

## Executando o Projeto

1. **Inicie a aplicação Python**:
   ```bash
   python main.py
   ```
   O servidor Flask estará rodando em `http://localhost:5000` (ou a porta especificada em `FLASK_PORT`).

2. **Teste o fluxo**:
   Envie mensagem para o número conectado na instância, e veja se o webhook é acionado com uma payload parecida com isso:
   ```json
   {
     "data": {
       "message": {
         "conversation": "Sua mensagem aqui"
       },
       "key": {
         "remoteJid": "123456789@s.whatsapp.net"
       }
     },
     "instance": "sua_instancia",
     "apikey": "apikey321"
   }
   ```

## Resolução de Problemas

- **Erro HTTP 429 (Too Many Requests)**:
  - Verifique os limites da sua chave de API da OpenAI no painel da OpenAI.
  - Certifique-se de que o índice FAISS está sendo reutilizado (diretório `faiss_index` existe).
  - Reduza o tamanho do arquivo `Q&A.csv` para testes iniciais.
  - Aumente o número de retries ou o tempo de espera em `llm_client.py` usando a biblioteca `tenacity`.

- **Redis não conecta**:
  - Confirme que o Redis está rodando no Docker (`docker-compose up -d`).
  - Verifique as configurações em `.env` (`REDIS_HOST=redis`, `REDIS_PORT=6379`, `REDIS_DB=0`).
  - Teste a conexão:
    ```bash
    docker exec -it redis redis-cli ping
    ```

- **Evolution API não envia mensagens ao webhook**:
  - Verifique se o webhook está configurado corretamente na Evolution API (`http://host:5000/webhook`).
  - Confirme que o evento `CHATS_UPSERT` está habilitado.
  - Cheque os logs do container da Evolution API:
    ```bash
    docker logs evolution_api
    ```

- **Aviso de depreciação do LangChain**:
  - Certifique-se de usar a versão mais recente do pacote `langchain-openai`:
    ```bash
    pip install -U langchain-openai
    ```

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
