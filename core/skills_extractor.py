# core/skills_extractor.py
def extract_skills(text: str) -> List[str]:
    """
    Simple skill extraction for testing
    """
    skills = []
    
    # Common skills to look for
    common_skills = [
        'python', 'java', 'javascript', 'sql', 'html', 'css', 
        'machine learning', 'data analysis', 'aws', 'docker',
        'react', 'node.js', 'tensorflow', 'pytorch', 'excel'
    ]
    
    text_lower = text.lower()
    for skill in common_skills:
        if skill in text_lower:
            skills.append(skill)
    
    return skills if skills else ["python", "sql", "data analysis"]