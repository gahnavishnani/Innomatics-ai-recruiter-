# core/skills_extractor.py
from core.preprocessor import preprocess_for_skills

# Expanded skills lists - ADD MORE AS NEEDED
HARD_SKILLS = {
    'python', 'java', 'javascript', 'sql', 'html', 'css', 'c++', 'r', 'ruby',
    'php', 'swift', 'kotlin', 'go', 'rust', 'typescript', 'bash', 'shell',
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
    'django', 'flask', 'react', 'angular', 'vue', 'node', 'express',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
    'linux', 'unix', 'windows', 'mongodb', 'mysql', 'postgresql', 'redis',
    'tableau', 'powerbi', 'excel', 'spark', 'hadoop', 'kafka'
}

SOFT_SKILLS = {
    'communication', 'leadership', 'teamwork', 'problem solving', 'creativity',
    'time management', 'adaptability', 'critical thinking', 'project management',
    'analytical', 'negotiation', 'presentation', 'mentoring', 'collaboration',
    'decision making', 'strategic planning', 'innovation', 'flexibility'
}

def extract_skills(text: str) -> dict:
    """
    Extract hard and soft skills from text using keyword matching.
    Returns a dictionary with 'hard_skills' and 'soft_skills' lists.
    """
    if not text:
        return {'hard_skills': [], 'soft_skills': []}
    
    processed_text = preprocess_for_skills(text)
    found_hard_skills = []
    found_soft_skills = []

    # Check for hard skills
    for skill in HARD_SKILLS:
        if skill in processed_text:
            found_hard_skills.append(skill)

    # Check for soft skills
    for skill in SOFT_SKILLS:
        if skill in processed_text:
            found_soft_skills.append(skill)

    return {
        'hard_skills': sorted(list(set(found_hard_skills))),
        'soft_skills': sorted(list(set(found_soft_skills)))
    }

def calculate_skill_match(resume_skills: dict, jd_skills: dict) -> dict:
    """Calculate skill match between resume and job description."""
    resume_all = set(resume_skills['hard_skills'] + resume_skills['soft_skills'])
    jd_all = set(jd_skills['hard_skills'] + jd_skills['soft_skills'])
    
    matching_skills = list(resume_all.intersection(jd_all))
    missing_skills = list(jd_all - resume_all)
    
    return {
        'matching_skills': sorted(matching_skills),
        'missing_skills': sorted(missing_skills),
        'resume_skills': resume_skills,
        'jd_skills': jd_skills
    }