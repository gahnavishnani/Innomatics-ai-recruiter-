i# core/parser.py
def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """
    Mock text extraction for testing
    """
    if filename.endswith('.pdf'):
        return "Mock PDF content: Python developer with 5 years experience. Skills: Python, SQL, Machine Learning."
    elif filename.endswith('.docx'):
        return "Mock DOCX content: Data Scientist with expertise in statistical analysis and predictive modeling."
    elif filename.endswith('.txt'):
        return file_content.decode('utf-8') if isinstance(file_content, bytes) else file_content
    else:
        return "Mock file content for analysis."