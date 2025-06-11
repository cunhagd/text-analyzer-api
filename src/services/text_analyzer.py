from collections import Counter
from typing import List, Tuple
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class TextAnalyzer:
    def __init__(self):
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        self.stop_words = set(stopwords.words('english'))

    def analyze_text(self, text: str) -> Tuple[int, List[dict]]:
        tokens = word_tokenize(text.lower())
        words = [word for word in tokens if word.isalnum() and word not in self.stop_words]
        word_count = len(words)
        word_freq = Counter(words).most_common(5)
        frequent_words = [{"word": word, "count": count} for word, count in word_freq]
        return word_count, frequent_words