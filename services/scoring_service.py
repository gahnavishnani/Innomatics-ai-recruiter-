# services/scoring_services.py
from typing import List, Dict, Any

def analyze_resume_jd_match(
    resume_text: str, 
    jd_text: str, 
    resume_skills: List[str], 
    jd_skills: List[str]
) -> Dict[str, Any]:
    """
    Mock analysis for testing
    """
    return {
        "score": 78.5,
        "verdict": "High",
        "matched_skills": ["python", "sql", "data analysis"],
        "missing_skills": ["aws", "docker", "kubernetes"],
        "hard_match_score": 80.0,
        "semantic_match_score": 77.0,
        "experience_match_score": 75.0
    }

def generate_suggestions(
    matched_skills: List[str],
    missing_skills: List[str],
    resume_text: str,
    jd_text: str
) -> List[str]:
    """
    Mock suggestions for testing
    """
    return [
        f"Develop skills in: {', '.join(missing_skills[:3])}",
        f"Highlight your expertise in: {', '.join(matched_skills[:3])}",
        "Add quantifiable achievements to your resume",
        "Tailor your resume summary to match the job requirements"
    ]