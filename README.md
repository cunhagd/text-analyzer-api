# Text Analyzer API

API REST para consulta de palavras, que analisa textos fornecidos, contagem de palavras-chave e estatísticas de sentimento, usando FastAPI, NLTK, SQLite e a API do Hugging Face.

## Pré-requisitos

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (gerenciador de pacotes)
- Conta no [Hugging Face](https://huggingface.co/) com chave de API

## Configuração

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/cunhagd/text-analyzer-api.git
   cd text-analyzer-api
```

2. **Crie e ative o ambiente virtual**:

   ```bash
   uv venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**:

   ```bash
   uv pip install -r requirements.txt
   ```

4. **Configure a chave de API do Hugging Face**:

   - Crie um arquivo `.env` na raiz do projeto com:

     ```
     HUGGINGFACE_API_KEY=xxxxxxxxxx
     ```
   - Obtenha a chave em Hugging Face Settings.

5. **Baixe os recursos do NLTK**:

   ```bash
   python -m nltk.downloader stopwords punkt punkt_tab
   ```

## Executando a API

1. **Inicie o servidor FastAPI**:

   ```bash
   uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

2. **Acesse a documentação Swagger**:

   - Abra `http://localhost:8000/docs` no navegador para testar os endpoints interativamente.

## Endpoints

### POST /analyze-text

Analisa um texto, retornando contagem de palavras, palavras frequentes e sentimento.

- **Entrada**:

  ```json
  {
    "text": "This is a sample text with sample words"
  }
  ```
- **Saída (exemplo)**:

  ```json
  {
    "word_count": 4,
    "frequent_words": [
      {"word": "sample", "count": 2},
      {"word": "text", "count": 1},
      {"word": "words", "count": 1}
    ],
    "sentiment": {
      "positive": 0.106,
      "negative": 0.893
    }
  }
  ```

### GET /search-term

Verifica se um termo está no último texto analisado.

- **Parâmetro**: `term` (query string)
- **Exemplo**: `http://localhost:8000/search-term?term=sample`
- **Saída (exemplo)**:

  ```json
  {
    "term": "sample",
    "found": true
  }
  ```

## Executando Testes

1. **Execute os testes unitários**:

   ```bash
   pytest -v
   ```

2. **Verifique a cobertura**:

   - Instale `pytest-cov`:

     ```bash
     uv pip install pytest-cov
     ```
   - Execute:

     ```bash
     pytest --cov=src tests/
     ```

## Estrutura do Projeto

```
text-analyzer-api/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   │   └── text_analyzer.py
│   │   └── models/
│   │       └── text_input.py
│   ├── services/
│   │   ├── text_analyzer.py
│   │   ├── sentiment_analyzer.py
│   │   └── storage.py
│   └── main.py
├── tests/
│   └── test_text_analyzer.py
├── .env
├── .gitignore
├── pytest.ini
├── README.md
├── requirements.txt
└── test.db
└── text_analyzer.db
```

## Tecnologias Utilizadas

- **FastAPI**: Framework para construção da API.
- **Pydantic**: Validação de dados.
- **NLTK**: Processamento de texto (contagem de palavras, stopwords).
- **Hugging Face**: Análise de sentimento (modelo `distilbert-base-uncased-finetuned-sst-2-english`).
- **SQLite**: Armazenamento do último texto analisado.
- **pytest**: Testes unitários.

## Contato

Desenvolvido por:

```
Gustavo Cunha
cunhagdc@gmail.com
```
