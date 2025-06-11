import pytest
import sqlite3
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.main import app
from src.services.text_analyzer import TextAnalyzer
from src.services.sentiment_analyzer import SentimentAnalyzer
from src.services.storage import Storage

@pytest.fixture
def client(storage):
    from src.api.routes import text_analyzer as text_analyzer_module
    text_analyzer_module.storage = storage
    return TestClient(app)

@pytest.fixture
def text_analyzer():
    return TextAnalyzer()

@pytest.fixture
def storage(tmp_path):
    db_path = tmp_path / "test.db"
    storage = Storage(db_path=str(db_path))
    # Limpar o banco antes de cada teste
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute("DELETE FROM analysis_history")
        conn.commit()
    return storage

def test_text_analyzer_analyze_text(text_analyzer):
    text = "This is a sample text with sample words"
    word_count, frequent_words = text_analyzer.analyze_text(text)
    assert word_count == 4
    assert frequent_words == [
        {"word": "sample", "count": 2},
        {"word": "text", "count": 1},
        {"word": "words", "count": 1}
    ]

def test_text_analyzer_empty_text(text_analyzer):
    word_count, frequent_words = text_analyzer.analyze_text("")
    assert word_count == 0
    assert frequent_words == []

@patch("src.services.sentiment_analyzer.requests.post")
def test_sentiment_analyzer_analyze_sentiment(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = [[
        {"label": "POSITIVE", "score": 0.9},
        {"label": "NEGATIVE", "score": 0.1}
    ]]
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_sentiment("Test text")
    assert result == {"positive": 0.9, "negative": 0.1}

@patch("src.services.sentiment_analyzer.requests.post")
def test_sentiment_analyzer_api_error(mock_post):
    mock_post.return_value.status_code = 403
    mock_post.return_value.json.return_value = {"error": "Forbidden"}
    analyzer = SentimentAnalyzer()
    with pytest.raises(Exception, match="Access forbidden"):
        analyzer.analyze_sentiment("Test text")

def test_storage_save_and_get_text(storage):
    text = "This is a test"
    storage.save_text(text)
    assert storage.get_last_text() == text

def test_storage_no_text(storage):
    assert storage.get_last_text() is None

@pytest.mark.asyncio
async def test_analyze_text_endpoint(client):
    response = client.post("/analyze-text", json={"text": "This is a sample text with sample words"})
    assert response.status_code == 200
    data = response.json()
    assert data["word_count"] == 4
    assert len(data["frequent_words"]) >= 3
    assert "positive" in data["sentiment"]
    assert "negative" in data["sentiment"]

@pytest.mark.asyncio
async def test_analyze_text_empty_input(client):
    response = client.post("/analyze-text", json={"text": ""})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_search_term_endpoint(client, storage):
    client.post("/analyze-text", json={"text": "This is a sample text"})
    response = client.get("/search-term?term=sample")
    assert response.status_code == 200
    assert response.json() == {"term": "sample", "found": True}

@pytest.mark.asyncio
async def test_search_term_not_found(client, storage):
    client.post("/analyze-text", json={"text": "This is a sample text"})
    response = client.get("/search-term?term=hello")
    assert response.status_code == 200
    assert response.json() == {"term": "hello", "found": False}

@pytest.mark.asyncio
async def test_search_term_no_text(client, storage):
    response = client.get("/search-term?term=sample")
    assert response.status_code == 404
    assert "No text has been analyzed" in response.json()["detail"]

@pytest.mark.asyncio
async def test_search_term_missing_param(client):
    response = client.get("/search-term")
    assert response.status_code == 422