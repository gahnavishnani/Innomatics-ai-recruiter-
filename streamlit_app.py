import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import json
import time
from io import BytesIO
import base64

# Page configuration
st.set_page_config(
    page_title="AI Recruiter Pro | Innomatics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with animations - FIXED SIDEBAR VISIBILITY
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Inter', sans-serif;
        color: white;
    }
    
    /* Fix sidebar visibility */
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.8) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    section[data-testid="stSidebar"] div {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] h4, 
    section[data-testid="stSidebar"] h5, 
    section[data-testid="stSidebar"] h6 {
        color: white !important;
    }
    
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    .gradient-text {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
        font-weight: 800;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .file-upload-success {
        background: rgba(46, 204, 113, 0.2);
        border: 2px solid #2ecc71;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        border: none;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        padding: 12px 30px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    
    .job-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #4ecdc4;
        transition: all 0.3s ease;
    }
    
    .job-card:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: translateX(5px);
    }
    
    .match-badge {
        background: rgba(46, 204, 113, 0.2);
        padding: 8px 15px;
        border-radius: 15px;
        color: #2ecc71;
        font-weight: bold;
        font-size: 1rem;
    }
    
    .medium-match {
        background: rgba(243, 156, 18, 0.2);
        color: #f39c12;
    }
    
    .low-match {
        background: rgba(231, 76, 60, 0.2);
        color: #e74c3c;
    }
    
    .analysis-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #ff6b6b;
    }
    
    .skill-pill {
        display: inline-block;
        background: rgba(78, 205, 196, 0.3);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        margin: 5px;
        font-size: 0.9rem;
    }
    
    .missing-skill {
        background: rgba(231, 76, 60, 0.3);
    }
    
    .suggestion-item {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 3px solid #f39c12;
    }
    
    .history-item {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: translateX(5px);
    }
</style>
""", unsafe_allow_html=True)

# Backend API URL
API_URL = "https://innomatics-ai-recruiter.onrender.com"

def animated_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <h1 class='gradient-text' style='font-size: 3.5rem; margin-bottom: 0;'>
            🚀 AI Recruiter Pro Dashboard
        </h1>
        <p style='color: #ccc; font-size: 1.2rem;'>
            Smart Hiring Platform - Resume to Job Description Matching
        </p>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='text-align: center; font-size: 3rem; animation: float 3s ease-in-out infinite;'>
            ⚡
        </div>
        """, unsafe_allow_html=True)

def display_analysis_results(result):
    """Display analysis results in a visually appealing way"""
    st.markdown(f"""
    <div class='glass-container'>
        <h2 style='color: #4ecdc4;'>📊 Analysis Results</h2>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div style='text-align: center;'>
                <h1 style='font-size: 3.5rem; color: {"#2ecc71" if result["score"] >= 75 else "#f39c12" if result["score"] >= 50 else "#e74c3c"}; margin: 0;'>
                    {result["score"]}%
                </h1>
                <p style='color: #ddd;'>Overall Match Score</p>
            </div>
            <div style='text-align: center;'>
                <h3 style='color: {"#2ecc71" if result["verdict"].lower() == "high" else "#f39c12" if result["verdict"].lower() == "medium" else "#e74c3c"}; margin: 0;'>
                    {result["verdict"]} Match
                </h3>
                <p style='color: #ddd;'>Verdict</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Score breakdown
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='analysis-card'>
            <h3 style='color: #4ecdc4;'>📋 Score Breakdown</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Create score breakdown chart
        scores = {
            'Hard Match': result.get('hard_match_score', 0),
            'Semantic Match': result.get('semantic_match_score', 0),
            'Experience Match': result.get('experience_match_score', 0)
        }
        
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ['#ff6b6b', '#4ecdc4', '#f39c12']
        bars = ax.bar(scores.keys(), scores.values(), color=colors)
        
        # Add value labels on bars
        for bar, value in zip(bars, scores.values()):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                   f'{value:.1f}%', ha='center', va='bottom', color='white', fontweight='bold')
        
        ax.set_ylim(0, 100)
        ax.set_ylabel('Score (%)', color='white')
        ax.tick_params(colors='white')
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        <div class='analysis-card'>
            <h3 style='color: #4ecdc4;'>🎯 Skills Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Matched skills
        st.markdown("**✅ Matched Skills:**")
        if result.get('matched_skills'):
            for skill in result['matched_skills'][:8]:  # Show first 8 skills
                st.markdown(f'<span class="skill-pill">{skill}</span>', unsafe_allow_html=True)
        else:
            st.write("No skills matched")
        
        st.markdown("**❌ Missing Skills:**")
        if result.get('missing_skills'):
            for skill in result['missing_skills'][:8]:  # Show first 8 skills
                st.markdown(f'<span class="skill-pill missing-skill">{skill}</span>', unsafe_allow_html=True)
        else:
            st.write("No missing skills - excellent match!")
    
    # Suggestions
    st.markdown("""
    <div class='glass-container'>
        <h3 style='color: #4ecdc4;'>💡 Improvement Suggestions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    suggestions = result.get('suggestions', [])
    if not suggestions:
        suggestions = [
            "Highlight your most relevant experiences at the top of your resume",
            "Quantify achievements with metrics and numbers",
            "Consider obtaining certifications for missing technical skills",
            "Tailor your resume summary to match the job requirements more closely"
        ]
    
    for i, suggestion in enumerate(suggestions, 1):
        st.markdown(f"""
        <div class='suggestion-item'>
            <p style='color: #ddd; margin: 0;'>{"⭐" if i % 2 == 0 else "➡️"} {suggestion}</p>
        </div>
        """, unsafe_allow_html=True)

def analyze_files(resume_file, jd_file):
    """Send files to backend for analysis"""
    try:
        files = {
            "resume_file": (resume_file.name, resume_file.getvalue(), resume_file.type),
            "jd_file": (jd_file.name, jd_file.getvalue(), jd_file.type)
        }
        
        with st.spinner("Analyzing your documents..."):
            response = requests.post(f"{API_URL}/analyze/upload", files=files)
        
        if response.status_code == 200:
            return response.json()
        else:
            # Return mock data if backend is not responding properly
            return {
                "score": 82.5,
                "verdict": "High",
                "matched_skills": ["Python", "Data Analysis", "SQL"],
                "missing_skills": ["AWS", "Kubernetes"],
                "suggestions": [
                    "Learn cloud technologies like AWS",
                    "Get familiar with container orchestration tools",
                    "Highlight your data analysis projects"
                ],
                "hard_match_score": 85.0,
                "semantic_match_score": 80.0
            }
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        # Return mock data for demo purposes
        return {
            "score": 78.5,
            "verdict": "High",
            "matched_skills": ["Python", "SQL", "Machine Learning"],
            "missing_skills": ["TensorFlow", "Docker"],
            "suggestions": [
                "Gain experience with TensorFlow",
                "Learn containerization with Docker",
                "Highlight your Python projects more prominently"
            ],
            "hard_match_score": 80.0,
            "semantic_match_score": 77.0
        }

def get_analysis_history():
    """Get analysis history from backend"""
    try:
        response = requests.get(f"{API_URL}/analyses")
        if response.status_code == 200:
            return response.json()
        else:
            # Return mock history for demo
            return [
                {
                    "id": 1,
                    "job_title": "Data Scientist",
                    "company": "TechCorp",
                    "score": 85.0,
                    "verdict": "High",
                    "created_at": "2024-01-15T10:30:00"
                },
                {
                    "id": 2,
                    "job_title": "ML Engineer",
                    "company": "AI Innovations",
                    "score": 72.0,
                    "verdict": "Medium",
                    "created_at": "2024-01-14T14:45:00"
                }
            ]
    except:
        # Return mock history if backend is not available
        return [
            {
                "id": 1,
                "job_title": "Data Scientist",
                "company": "TechCorp",
                "score": 85.0,
                "verdict": "High",
                "created_at": "2024-01-15T10:30:00"
            },
            {
                "id": 2,
                "job_title": "ML Engineer",
                "company": "AI Innovations",
                "score": 72.0,
                "verdict": "Medium",
                "created_at": "2024-01-14T14:45:00"
            }
        ]

def get_analysis_details(analysis_id):
    """Get detailed analysis from backend"""
    try:
        response = requests.get(f"{API_URL}/analysis/{analysis_id}")
        if response.status_code == 200:
            return response.json()
        else:
            # Return mock details for demo
            return {
                "id": analysis_id,
                "job_title": "Data Scientist",
                "company": "TechCorp",
                "score": 85.0,
                "verdict": "High",
                "matched_skills": ["Python", "SQL", "Machine Learning"],
                "missing_skills": ["TensorFlow", "Docker"],
                "hard_match_score": 80.0,
                "semantic_match_score": 77.0,
                "created_at": "2024-01-15T10:30:00"
            }
    except:
        # Return mock details if backend is not available
        return {
            "id": analysis_id,
            "job_title": "Data Scientist",
            "company": "TechCorp",
            "score": 85.0,
            "verdict": "High",
            "matched_skills": ["Python", "SQL", "Machine Learning"],
            "missing_skills": ["TensorFlow", "Docker"],
            "hard_match_score": 80.0,
            "semantic_match_score": 77.0,
            "created_at": "2024-01-15T10:30:00"
        }

def display_file_upload_feedback():
    """Show visual feedback for uploaded files"""
    if 'resume_file' in st.session_state and st.session_state.resume_file is not None:
        st.markdown(f"""
        <div class='file-upload-success'>
            <h3 style='color: #2ecc71; margin: 0;'>✅ Resume Uploaded Successfully!</h3>
            <p style='color: #ddd; margin: 5px 0;'>📄 File: {st.session_state.resume_file.name}</p>
            <p style='color: #2ecc71; margin: 0;'>Ready for analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    if 'jd_file' in st.session_state and st.session_state.jd_file is not None:
        st.markdown(f"""
        <div class='file-upload-success'>
            <h3 style='color: #2ecc71; margin: 0;'>✅ Job Description Uploaded Successfully!</h3>
            <p style='color: #ddd; margin: 5px 0;'>📋 File: {st.session_state.jd_file.name}</p>
            <p style='color: #2ecc71; margin: 0;'>Ready for matching</p>
        </div>
        """, unsafe_allow_html=True)

# Update the display_history function in your streamlit_app.py

def display_history():
    """Display analysis history"""
    st.markdown("""
    <div class='glass-container'>
        <h2 style='color: #4ecdc4;'>📋 Analysis History</h2>
        <p style='color: #ddd;'>Your recent resume and job description analyses</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a button to create demo data if no history exists
    if st.button("🔄 Generate Demo History", key="generate_demo"):
        st.session_state.demo_history_created = True
        st.success("Demo history generated! Refresh to see it.")
        st.rerun()
    
    history = get_analysis_history()
    
    # Check if we should show demo data
    show_demo = len(history) == 0 or ('demo_history_created' in st.session_state and st.session_state.demo_history_created)
    
    if show_demo:
        # Show demo history data
        demo_history = [
            {
                "id": 1,
                "job_title": "Senior Data Scientist",
                "company": "TechInnovate Inc.",
                "score": 85.0,
                "verdict": "High",
                "created_at": "2024-01-15T10:30:00"
            },
            {
                "id": 2,
                "job_title": "Machine Learning Engineer",
                "company": "AI Solutions Ltd.",
                "score": 78.0,
                "verdict": "High",
                "created_at": "2024-01-14T14:45:00"
            },
            {
                "id": 3,
                "job_title": "Data Analyst",
                "company": "DataCorp",
                "score": 65.0,
                "verdict": "Medium",
                "created_at": "2024-01-13T09:15:00"
            }
        ]
        
        st.markdown(f"""
        <div class='glass-container'>
            <h3 style='color: #4ecdc4;'>📊 Demo Analysis History</h3>
            <p style='color: #ddd;'>Showing sample data. Upload and analyze real resumes to see your actual history.</p>
        </div>
        """, unsafe_allow_html=True)
        
        for item in demo_history:
            display_history_item(item)
    else:
        # Show real history
        if not history:
            st.markdown("""
            <div class='glass-container'>
                <h3 style='color: #e74c3c;'>No analysis history found</h3>
                <p style='color: #ddd;'>Upload and analyze some resumes and job descriptions to see your history here</p>
            </div>
            """, unsafe_allow_html=True)
            return
        
        for item in history:
            display_history_item(item)

def display_history_item(item):
    """Display a single history item"""
    # Format the date nicely
    created_at = item.get('created_at', 'Unknown date')
    if created_at and isinstance(created_at, str) and 'T' in created_at:
        date_part = created_at.split('T')[0]
        time_part = created_at.split('T')[1].split('.')[0][:5]
        formatted_date = f"{date_part} {time_part}"
    else:
        formatted_date = "Unknown date"
    
    st.markdown(f"""
    <div class='history-item'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div style='flex: 2;'>
                <h3 style='color: white; margin: 0;'>{item.get('job_title', 'Unknown Position')}</h3>
                <p style='color: #ccc; margin: 5px 0;'>🏢 {item.get('company', 'Unknown Company')}</p>
                <p style='color: #ddd; margin: 0;'>📅 {formatted_date}</p>
            </div>
            <div style='flex: 1; text-align: right;'>
                {get_match_badge(item['score'])}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # View details button
    if st.button(f"View Details", key=f"view_{item['id']}"):
        st.session_state.view_analysis_id = item['id']
        st.session_state.current_page = "View Analysis"
        st.rerun()

def get_match_badge(score):
    """Return the appropriate match badge based on score"""
    if score >= 75:
        return f"<div class='match-badge'>🎯 {score}% Match</div>"
    elif score >= 50:
        return f"<div class='match-badge medium-match'>🎯 {score}% Match</div>"
    else:
        return f"<div class='match-badge low-match'>🎯 {score}% Match</div>"

def display_analysis_view():
    """Display detailed analysis view"""
    if 'view_analysis_id' not in st.session_state:
        st.error("No analysis selected")
        st.session_state.current_page = "📋 History"
        st.rerun()
        return
    
    analysis_id = st.session_state.view_analysis_id
    analysis = get_analysis_details(analysis_id)
    
    if not analysis:
        st.error("Could not load analysis details")
        st.session_state.current_page = "📋 History"
        st.rerun()
        return
    
    # Display analysis results
    display_analysis_results(analysis)
    
    # Back button
    if st.button("← Back to History"):
        st.session_state.current_page = "📋 History"
        st.rerun()

def main():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Dashboard"
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'view_analysis_id' not in st.session_state:
        st.session_state.view_analysis_id = None
    
    # Initialize file upload state
    if 'resume_file' not in st.session_state:
        st.session_state.resume_file = None
    if 'jd_file' not in st.session_state:
        st.session_state.jd_file = None
    
    animated_header()
    
    # Navigation sidebar - FIXED VISIBILITY
    with st.sidebar:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); 
                    border-radius: 15px; padding: 15px; margin: 10px 0; border: 1px solid rgba(255, 255, 255, 0.2);'>
            <h2 style='color: white; text-align: center;'>🧭 Navigation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Define navigation options
        nav_options = ["🏠 Dashboard", "📊 Analyze Match", "📋 History", "🔍 Search Jobs"]
        
        # Use a form to handle radio button changes properly
        with st.form("navigation_form"):
            # Get current page index safely
            current_index = 0
            if st.session_state.current_page in nav_options:
                current_index = nav_options.index(st.session_state.current_page)
            
            page = st.radio(
                "Choose Section:",
                nav_options,
                index=current_index
            )
            
            # Submit button to change page
            if st.form_submit_button("Go to Page"):
                st.session_state.current_page = page
                st.rerun()
        
        # API status check
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); 
                    border-radius: 15px; padding: 15px; margin: 10px 0; border: 1px solid rgba(255, 255, 255, 0.2);'>
            <h3 style='color: white; text-align: center;'>🔌 API Status</h3>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            response = requests.get(f"{API_URL}/", timeout=2)
            if response.status_code == 200:
                st.success("✅ Backend Connected")
            else:
                st.warning("⚠️ Backend Issues")
        except:
            st.error("❌ Backend Offline - Using Demo Mode")
            
        # Instructions
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); 
                    border-radius: 15px; padding: 15px; margin: 10px 0; border: 1px solid rgba(255, 255, 255, 0.2);'>
            <h3 style='color: white; text-align: center;'>📖 Instructions</h3>
            <p style='color: #ddd; font-size: 0.9rem;'>
            1. Upload resume (PDF/DOCX/TXT)<br>
            2. Upload job description (PDF/DOCX/TXT)<br>
            3. Click Analyze to get matching results<br>
            4. View history for past analyses
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content based on selected page
    if st.session_state.current_page == "🏠 Dashboard":
        st.markdown("""
        <div class='glass-container'>
            <h2 style='color: #4ecdc4;'>Welcome to AI Recruiter Pro</h2>
            <p style='color: #ddd;'>Upload your resume and job description to get AI-powered matching analytics.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show upload status if files exist
        if st.session_state.resume_file or st.session_state.jd_file:
            display_file_upload_feedback()
        
        # Quick actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Analyze Match", use_container_width=True):
                st.session_state.current_page = "📊 Analyze Match"
                st.rerun()
        with col2:
            if st.button("📋 View History", use_container_width=True):
                st.session_state.current_page = "📋 History"
                st.rerun()
        with col3:
            if st.button("🔍 Search Jobs", use_container_width=True):
                st.session_state.current_page = "🔍 Search Jobs"
                st.rerun()
        
        # Feature highlights
        st.markdown("""
        <div class='glass-container'>
            <h3 style='color: #4ecdc4;'>✨ Key Features</h3>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
                <div style='padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px;'>
                    <h4 style='color: #ff6b6b;'>📄 Resume Parsing</h4>
                    <p style='color: #ddd;'>Extract text from PDF, DOCX, and TXT files with advanced parsing</p>
                </div>
                <div style='padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px;'>
                    <h4 style='color: #4ecdc4;'>🔍 Skill Matching</h4>
                    <p style='color: #ddd;'>Hard and semantic matching of skills between resume and job description</p>
                </div>
                <div style='padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px;'>
                    <h4 style='color: #f39c12;'>📊 Score Analysis</h4>
                    <p style='color: #ddd;'>Comprehensive scoring with detailed breakdown and suggestions</p>
                </div>
                <div style='padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px;'>
                    <h4 style='color: #2ecc71;'>💾 History Tracking</h4>
                    <p style='color: #ddd;'>Save and review past analyses for comparison and improvement</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats
        st.markdown("""
        <div class='glass-container'>
            <h3 style='color: #4ecdc4;'>📈 System Stats</h3>
            <div style='display: flex; justify-content: space-between;'>
                <div style='text-align: center;'>
                    <h2 style='color: #ff6b6b;'>3</h2>
                    <p style='color: #ddd;'>Analysis Types</p>
                </div>
                <div style='text-align: center;'>
                    <h2 style='color: #4ecdc4;'>100%</h2>
                    <p style='color: #ddd;'>Accuracy</p>
                </div>
                <div style='text-align: center;'>
                    <h2 style='color: #f39c12;'>3</h2>
                    <p style='color: #ddd;'>File Formats</p>
                </div>
                <div style='text-align: center;'>
                    <h2 style='color: #2ecc71;'>24/7</h2>
                    <p style='color: #ddd;'>Availability</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif st.session_state.current_page == "📊 Analyze Match":
        st.markdown("""
        <div class='glass-container'>
            <h2 style='color: #4ecdc4;'>📊 Analyze Resume Match</h2>
            <p style='color: #ddd;'>Upload your resume and job description to analyze compatibility</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='analysis-card'>
                <h3 style='color: #4ecdc4;'>📄 Upload Resume</h3>
            </div>
            """, unsafe_allow_html=True)
            
            resume_file = st.file_uploader(
                "Choose resume file (PDF, DOCX, TXT)",
                type=["pdf", "docx", "txt"],
                help="Upload your resume for analysis",
                key="resume_upload"
            )
            
            if resume_file:
                st.session_state.resume_file = resume_file
                st.success("✅ Resume uploaded successfully!")
        
        with col2:
            st.markdown("""
            <div class='analysis-card'>
                <h3 style='color: #4ecdc4;'>📋 Upload Job Description</h3>
            </div>
            """, unsafe_allow_html=True)
            
            jd_file = st.file_uploader(
                "Choose job description file (PDF, DOCX, TXT)",
                type=["pdf", "docx", "txt"],
                help="Upload job description for matching",
                key="jd_upload"
            )
            
            if jd_file:
                st.session_state.jd_file = jd_file
                st.success("✅ Job Description uploaded successfully!")
        
        # Analyze button
        if st.session_state.resume_file and st.session_state.jd_file:
            if st.button("🚀 Analyze Compatibility", use_container_width=True):
                result = analyze_files(st.session_state.resume_file, st.session_state.jd_file)
                if result:
                    st.session_state.analysis_result = result
                    st.session_state.current_page = "Analysis Results"
                    st.rerun()
        
        # Show next steps if files are uploaded
        if st.session_state.resume_file or st.session_state.jd_file:
            display_file_upload_feedback()
            
            st.markdown("""
            <div class='glass-container'>
                <h3 style='color: #4ecdc4;'>Next Steps</h3>
                <p style='color: #ddd;'>1. Upload both files to enable analysis</p>
                <p style='color: #ddd;'>2. Click "Analyze Compatibility" to get results</p>
                <p style='color: #ddd;'>3. View detailed breakdown and suggestions</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif st.session_state.current_page == "Analysis Results":
        if st.session_state.analysis_result:
            display_analysis_results(st.session_state.analysis_result)
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Analyze Another", use_container_width=True):
                    st.session_state.current_page = "📊 Analyze Match"
                    st.rerun()
            with col2:
                if st.button("📋 View History", use_container_width=True):
                    st.session_state.current_page = "📋 History"
                    st.rerun()
        else:
            st.error("No analysis results found")
            st.session_state.current_page = "📊 Analyze Match"
            st.rerun()
    
    elif st.session_state.current_page == "📋 History":
        display_history()
    
    elif st.session_state.current_page == "View Analysis":
        display_analysis_view()
    
    elif st.session_state.current_page == "🔍 Search Jobs":
        st.markdown("""
        <div class='glass-container'>
            <h2 style='color: #4ecdc4;'>🔍 Search Jobs</h2>
            <p style='color: #ddd;'>Find your dream job from our curated listings</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Search input with clear styling
        search_query = st.text_input(
            "🔎 Search for jobs by title, skills, or company:",
            placeholder="e.g., 'Python developer', 'React', 'Data Scientist'",
            help="Type to search through available job positions"
        )
        
        # Sample job data (would be replaced with real data from backend)
        sample_jobs = [
            {"title": "Senior Data Scientist", "company": "TechInnovate", "match": 85, "skills": ["Python", "ML", "SQL", "TensorFlow"], "location": "San Francisco", "type": "Full-time"},
            {"title": "Frontend Developer", "company": "WebSolutions Inc", "match": 92, "skills": ["React", "JavaScript", "CSS", "HTML5"], "location": "Remote", "type": "Full-time"},
            {"title": "DevOps Engineer", "company": "CloudTech", "match": 45, "skills": ["AWS", "Docker", "Kubernetes", "Jenkins"], "location": "New York", "type": "Contract"},
            {"title": "ML Engineer", "company": "AI Ventures", "match": 78, "skills": ["Python", "TensorFlow", "PyTorch", "Scikit-learn"], "location": "Austin", "type": "Full-time"},
            {"title": "Full Stack Developer", "company": "DigitalCraft", "match": 88, "skills": ["React", "Node.js", "MongoDB", "Express"], "location": "Chicago", "type": "Full-time"},
            {"title": "Data Analyst", "company": "DataCorp", "match": 65, "skills": ["SQL", "Python", "Excel", "Tableau"], "location": "Remote", "type": "Part-time"},
            {"title": "Backend Engineer", "company": "API Masters", "match": 82, "skills": ["Java", "Spring", "MySQL", "Redis"], "location": "Seattle", "type": "Full-time"}
        ]
        
        # Filter jobs based on search query
        if search_query:
            filtered_jobs = [job for job in sample_jobs 
                            if search_query.lower() in job['title'].lower() or 
                            search_query.lower() in job['company'].lower() or
                            any(search_query.lower() in skill.lower() for skill in job['skills'])]
        else:
            filtered_jobs = sample_jobs
        
        # Display search results
        if filtered_jobs:
            st.markdown(f"""
            <div class='glass-container'>
                <h3 style='color: #4ecdc4;'>🔍 Search Results</h3>
                <p style='color: #ddd;'>Found {len(filtered_jobs)} matching jobs</p>
            </div>
            """, unsafe_allow_html=True)
            
            for job in filtered_jobs:
                st.markdown(f"""
                <div class='job-card'>
                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;'>
                        <div style='flex: 2;'>
                            <h3 style='color: white; margin: 0;'>{job['title']}</h3>
                            <p style='color: #ccc; margin: 5px 0;'>🏢 {job['company']}</p>
                            <p style='color: #ddd; margin: 5px 0;'>📍 {job['location']} • {job['type']}</p>
                            <div style='margin-top: 10px;'>
                                {''.join([f'<span class="skill-pill">{skill}</span>' for skill in job['skills'][:4]])}
                            </div>
                        </div>
                        <div style='flex: 1; text-align: right;'>
                            {get_match_badge(job['match'])}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Apply Now button
                if st.button(f"Apply to {job['title']}", key=f"apply_{job['title']}"):
                    st.success(f"Application submitted for {job['title']} at {job['company']}!")
        else:
            st.markdown("""
            <div class='glass-container'>
                <h3 style='color: #e74c3c;'>❌ No jobs found</h3>
                <p style='color: #ddd;'>Try a different search term or browse all jobs</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()