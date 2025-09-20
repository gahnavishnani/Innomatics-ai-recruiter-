# chains/llm_analysis.py
from typing import Dict, List

def analyze_with_llm(
    resume_text: str, 
    jd_text: str, 
    matched_skills: List[str], 
    missing_skills: List[str]
) -> Dict[str, List[str]]:
    """
    Mock LLM analysis for testing
    """
    return {
        "suggestions": [
            "Consider taking an online course in the missing technologies",
            "Highlight your most relevant projects at the top of your resume",
            "Add metrics to quantify your achievements",
            "Customize your resume for each job application"
        ]
    }