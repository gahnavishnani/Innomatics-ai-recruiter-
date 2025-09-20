# core/preprocessor.py
import re
import spacy
from typing import List

# Load the spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise ImportError("spaCy English model not found. Run: python -m spacy download en_core_web_sm")

def clean_text(text: str) -> str:
    """
    Clean and preprocess text: remove extra spaces, special chars, etc.
    Basic cleaning that preserves structure for LLM analysis.
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove non-ASCII characters but keep basic punctuation
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

def preprocess_for_skills(text: str) -> str:
    """More aggressive preprocessing for skill extraction: lowercasing, lemmatization."""
    if not text:
        return ""
    
    doc = nlp(text.lower())
    # Lemmatize and remove stop words and punctuation
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
    return " ".join(tokens)