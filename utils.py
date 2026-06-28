import json
import re
from pathlib import Path
from typing import List, Dict, Tuple

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class FAQChatbotEngine:
    """A lightweight NLP-based FAQ retrieval engine using TF-IDF and cosine similarity."""

    def __init__(self, faq_path: str, similarity_threshold: float = 0.4):
        self.faq_path = Path(faq_path)
        self.similarity_threshold = similarity_threshold
        self.faq_data: List[Dict[str, str]] = []
        self.questions: List[str] = []
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set()
        self._prepare_nltk_data()
        self._load_faqs()
        self._build_index()

    def _prepare_nltk_data(self) -> None:
        """Download required NLTK resources if they are not available."""
        # Ensure the NLP resources needed for tokenization, stopword removal, and lemmatization are present.
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt", quiet=True)
        try:
            nltk.data.find("corpora/stopwords")
        except LookupError:
            nltk.download("stopwords", quiet=True)
        try:
            nltk.data.find("corpora/wordnet")
        except LookupError:
            nltk.download("wordnet", quiet=True)
        try:
            nltk.data.find("corpora/omw-1.4")
        except LookupError:
            nltk.download("omw-1.4", quiet=True)
        self.stop_words = set(stopwords.words("english"))

    def _load_faqs(self) -> None:
        """Load FAQ entries from JSON file."""
        if not self.faq_path.exists():
            raise FileNotFoundError(f"FAQ file not found: {self.faq_path}")

        with self.faq_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        if not isinstance(data, list):
            raise ValueError("FAQ data must be a list of objects.")

        self.faq_data = data
        self.questions = [item.get("question", "") for item in self.faq_data if item.get("question")]

    def _build_index(self) -> None:
        """Create the TF-IDF matrix for FAQ questions."""
        if not self.questions:
            return
        self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)

    def preprocess_text(self, text: str) -> str:
        """Normalize user input using lowercase, punctuation removal, tokenization, stopword removal, and lemmatization."""
        # Convert raw user input into a clean token sequence suitable for vectorization.
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        tokens = text.split()
        tokens = [token for token in tokens if token not in self.stop_words]
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        return " ".join(tokens)

    def get_best_match(self, user_input: str) -> Tuple[str, str, float]:
        """Return the best matching answer and similarity score for the input question."""
        if not self.questions:
            return "", "No FAQ data available.", 0.0

        cleaned_input = self.preprocess_text(user_input)
        if not cleaned_input.strip():
            return "", "Please enter a valid question.", 0.0

        transformed_input = self.vectorizer.transform([cleaned_input])
        similarities = cosine_similarity(transformed_input, self.tfidf_matrix).flatten()
        best_index = int(similarities.argmax())
        best_score = float(similarities[best_index])

        if best_score < self.similarity_threshold:
            return "", "Sorry, I couldn't find an answer to that question.", best_score

        best_question = self.questions[best_index]
        answer = self.faq_data[best_index].get("answer", "")
        return best_question, answer, best_score

    def get_response(self, user_input: str) -> str:
        """Obtain a chatbot response for the given user input."""
        _, response, _ = self.get_best_match(user_input)
        return response
