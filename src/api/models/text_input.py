from pydantic import BaseModel, Field
from typing import List, Dict

class TextInput(BaseModel):
    text: str = Field(..., min_length=1, description="Texto a ser analisado")

class FrequentWord(BaseModel):
    word: str
    count: int

class TextAnalysisResponse(BaseModel):
    word_count: int = Field(..., ge=0, description="Total de palavras")
    frequent_words: List[FrequentWord] = Field(..., description="Top 5 palavras mais frequentes")
    sentiment: Dict[str, float] = Field(..., description="Análise de sentimento")

class SearchTermResponse(BaseModel):
    term: str = Field(..., description="Termo pesquisado")
    found: bool = Field(..., description="Indica se o termo foi encontrado no texto")