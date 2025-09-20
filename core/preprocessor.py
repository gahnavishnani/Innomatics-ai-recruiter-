# core/preprocessor.py
import re

def preprocess_text(text: str) -> str:
    """
    Simple text preprocessing
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text