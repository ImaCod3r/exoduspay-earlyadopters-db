# Early Adopters Database

Um painel web para gerenciar registros de emails com análise por gráficos, usando **Flask** e **SQLite Cloud**.

## Recursos

- 📧 Formulário para adicionar emails
- 📊 Gráficos de análise (por dia e por hora)
- 📋 Tabela responsiva com busca, paginação e ordenação
- 🗑️ Remover emails
- 📥 Exportar dados em CSV
- ☁️ 100% integrado com SQLite Cloud
- ⚡ Sem dependências de ORM pesadas (apenas sqlitecloud nativo)

## Stack Tecnológico

### Backend
- **Flask 3.0.0** - Framework web
- **flask-cors 4.0.0** - Suporte CORS
- **python-dotenv 1.0.0** - Configuração via `.env`
- **sqlitecloud 1.0.37** - Driver nativo para SQLite Cloud

### Frontend
- **Bootstrap 5.3.2** - CSS framework (via CDN)
- **Chart.js 4.4.0** - Gráficos (via CDN)

## Setup

### Pré-requisitos
- Python 3.8+
- Uma conta em [SQLite Cloud](https://sqlitecloud.io)
- Uma database criada no SQLite Cloud

### 1. Clonar o repositório

```powershell
git clone <repo-url>
cd early-adopters-db
```

### 2. Criar e ativar ambiente virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
CONNECTION_STRING=sqlitecloud://api-key@host:8860/dbname?apikey=your_api_key
```

**Obter a connection string:**
1. Acesse o painel do SQLite Cloud
2. Selecione sua database
3. Copie a connection string (geralmente começa com `sqlitecloud://`)
4. Cole no arquivo `.env`

### 5. Executar a aplicação

```powershell
cd source
python main.py
```

A aplicação estará disponível em: **http://127.0.0.1:5000**

## Estrutura do Projeto

```
early-adopters-db/
├── source/
│   ├── main.py              # Aplicação Flask com rotas da API
│   ├── database.py          # Classe Email + conexão sqlitecloud
│   └── templates/
│       └── index.html       # Interface Bootstrap + gráficos Chart.js
├── requirements.txt         # Dependências Python
├── .env.example            # Exemplo de variáveis de ambiente
├── test_connection.py      # Script para testar conexão
├── README.md               # Este arquivo
└── venv/                   # Ambiente virtual (criado após setup)
```

## API Endpoints

### GET `/`
Serve a página principal (HTML).

### GET `/api/emails`
Retorna lista de todos os emails registrados.

**Response:**
```json
[
  {
    "email": "user@example.com",
    "time": "07/12/2025 14:30:45"
  },
  {
    "email": "another@example.com",
    "time": "07/12/2025 14:25:10"
  }
]
```

### POST `/api/emails`
Adiciona um novo email.

**Request:**
```json
{
  "email": "novo@example.com"
}
```

**Response:**
```json
{
  "message": "Email added successfully",
  "email": "novo@example.com",
  "time": "07/12/2025 14:30:45"
}
```

### DELETE `/api/emails`
Remove um email.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Email deleted successfully"
}
```

### GET `/api/emails/stats`
Retorna estatísticas de registros.

**Response:**
```json
{
  "total": 42,
  "byDay": [
    {"date": "2025-12-07", "count": 15},
    {"date": "2025-12-08", "count": 27}
  ],
  "byHour": [
    {"hour": "00", "count": 0},
    {"hour": "01", "count": 1},
    {"hour": "14", "count": 8},
    ...
    {"hour": "23", "count": 2}
  ]
}
```

## Como Funciona

### Banco de Dados (SQLite Cloud)

A classe `Email` em `database.py` oferece uma interface simples para interagir com o SQLite Cloud:

```python
# Criar um novo email
new_email = Email.create("user@example.com")

# Listar todos os emails
emails = Email.select()

# Remover um email
Email.delete("user@example.com")

# Obter estatísticas
stats = Email.get_stats()
```

### Frontend

O arquivo `index.html` implementa:
- **Tabela** com busca, paginação e ordenação
- **Gráficos** (linha e barra) usando Chart.js
- **Botões** de ação (copiar, remover)
- **Export** para CSV

Todos os dados são carregados dynamicamente via API REST.

## Troubleshooting

### Erro: "CONNECTION_STRING environment variable must be set"
- Verifique se o arquivo `.env` existe na raiz do projeto
- Verifique se `CONNECTION_STRING` está configurada corretamente
- Use `.env.example` como referência

### Erro: "ModuleNotFoundError: No module named 'sqlitecloud'"
```powershell
pip install sqlitecloud
```

### Erro: "Connection refused" ou timeout
- Verifique se a connection string está correta
- Verifique se tem acesso à rede (firewall, VPN, etc.)
- Verifique se a API key é válida
- Verifique se a database existe no SQLite Cloud

### Tabela vazia no painel
- Verifique se está conectado à database correta
- Verifique se a tabela `emails` foi criada (deve ser automático)
- Verifique os logs no terminal da aplicação

## Desenvolvimento

### Rodar com debug ativado

```powershell
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
cd source
python main.py
```

### Testar conexão ao banco

```powershell
python test_connection.py
```

### Rodar testes (se disponíveis)

```powershell
pytest tests/
```

## Environment Variables

| Variável | Obrigatória | Exemplo |
|----------|-----------|---------|
| `CONNECTION_STRING` | Sim | `sqlitecloud://api-key@host:8860/db?apikey=key` |
| `FLASK_ENV` | Não | `development` ou `production` |
| `FLASK_DEBUG` | Não | `1` ou `0` |

## Deployed com Sucesso? 🎉

Se conseguiu rodar a aplicação:
1. Abra http://127.0.0.1:5000
2. Adicione alguns emails
3. Veja os gráficos se atualizarem
4. Teste a busca, paginação e export

## Contribuindo

Feel free to fork, modify, and improve!

## Licença

MIT