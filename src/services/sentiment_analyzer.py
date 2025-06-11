from typing import Dict
import requests
from dotenv import load_dotenv
import os

class SentimentAnalyzer:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY not found in .env file")
        self.api_url = "https://api-inference.huggingface.co/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": text, "options": {"wait_for_model": True}}
            )
            if response.status_code == 403:
                raise Exception("Access forbidden: Verify HUGGINGFACE_API_KEY permissions")
            response.raise_for_status()
            results = response.json()
            if not isinstance(results, list) or not results or not isinstance(results[0], list):
                raise Exception(f"Invalid response format from Hugging Face API: {results}")
            return {item["label"].lower(): item["score"] for item in results[0]}
        except requests.RequestException as e:
            raise Exception(f"Failed to analyze sentiment: {str(e)}")