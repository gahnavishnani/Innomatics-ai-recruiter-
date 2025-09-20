# services/scoring_service.py
# Change from relative to absolute imports
from core.skills_extractor import extract_skills, calculate_skill_match

def analyze_skills(resume_text: str, jd_text: str) -> dict:
    """
    Main function to analyze skills from resume and JD.
    Returns comprehensive skill analysis.
    """
    # Extract skills from both documents
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    
    # Calculate matches and gaps
    skill_analysis = calculate_skill_match(resume_skills, jd_skills)
    
    # Calculate match score (simple percentage)
    total_jd_skills = len(jd_skills['hard_skills'] + jd_skills['soft_skills'])
    match_count = len(skill_analysis['matching_skills'])
    
    skill_analysis['match_score'] = round((match_count / total_jd_skills * 100), 2) if total_jd_skills > 0 else 0
    skill_analysis['total_jd_skills'] = total_jd_skills
    skill_analysis['matched_count'] = match_count
    
    return skill_analysis