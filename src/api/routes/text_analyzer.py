from fastapi import APIRouter, HTTPException
from src.api.models.text_input import TextInput, TextAnalysisResponse, SearchTermResponse
from src.services.text_analyzer import TextAnalyzer
from src.services.sentiment_analyzer import SentimentAnalyzer
from src.services.storage import Storage

router = APIRouter()
text_analyzer = TextAnalyzer()
sentiment_analyzer = SentimentAnalyzer()
storage = Storage()

@router.post("/analyze-text", response_model=TextAnalysisResponse)
async def analyze_text(input_data: TextInput):
    try:
        word_count, frequent_words = text_analyzer.analyze_text(input_data.text)
        sentiment = sentiment_analyzer.analyze_sentiment(input_data.text)
        storage.save_text(input_data.text)
        return TextAnalysisResponse(
            word_count=word_count,
            frequent_words=frequent_words,
            sentiment=sentiment
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/search-term", response_model=SearchTermResponse)
async def search_term(term: str):
    if not term:
        raise HTTPException(status_code=400, detail="Term parameter is required")
    last_text = storage.get_last_text()
    if not last_text:
        raise HTTPException(status_code=404, detail="No text has been analyzed yet")
    found = term.lower() in last_text.lower()
    return SearchTermResponse(term=term, found=found)