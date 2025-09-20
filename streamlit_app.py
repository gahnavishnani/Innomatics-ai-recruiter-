import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import json
import time
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="AI Recruiter Pro | Innomatics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with animations
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Inter', sans-serif;
        color: white;
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
    
    .sidebar .radio-group {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .sidebar .radio-group label {
        color: white !important;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        transition: all 0.3s ease;
    }
    
    .sidebar .radio-group label:hover {
        background: rgba(78, 205, 196, 0.2);
    }
    
    .sidebar .radio-group label[data-testid="stRadioLabel"] > div:first-child {
        background: rgba(255, 255, 255, 0.1) !important;
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
</style>
""", unsafe_allow_html=True)

# Sample data for demonstration
SAMPLE_JOBS = [
    {"title": "Senior Data Scientist", "company": "TechInnovate", "match": 85, "skills": ["Python", "ML", "SQL", "TensorFlow"], "location": "San Francisco", "type": "Full-time"},
    {"title": "Frontend Developer", "company": "WebSolutions Inc", "match": 92, "skills": ["React", "JavaScript", "CSS", "HTML5"], "location": "Remote", "type": "Full-time"},
    {"title": "DevOps Engineer", "company": "CloudTech", "match": 45, "skills": ["AWS", "Docker", "Kubernetes", "Jenkins"], "location": "New York", "type": "Contract"},
    {"title": "ML Engineer", "company": "AI Ventures", "match": 78, "skills": ["Python", "TensorFlow", "PyTorch", "Scikit-learn"], "location": "Austin", "type": "Full-time"},
    {"title": "Full Stack Developer", "company": "DigitalCraft", "match": 88, "skills": ["React", "Node.js", "MongoDB", "Express"], "location": "Chicago", "type": "Full-time"},
    {"title": "Data Analyst", "company": "DataCorp", "match": 65, "skills": ["SQL", "Python", "Excel", "Tableau"], "location": "Remote", "type": "Part-time"},
    {"title": "Backend Engineer", "company": "API Masters", "match": 82, "skills": ["Java", "Spring", "MySQL", "Redis"], "location": "Seattle", "type": "Full-time"}
]

def animated_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <h1 class='gradient-text' style='font-size: 3.5rem; margin-bottom: 0;'>
            🚀 AI Recruiter Pro Dashboard
        </h1>
        <p style='color: #ccc; font-size: 1.2rem;'>
            Smart Hiring Platform
        </p>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='text-align: center; font-size: 3rem; animation: float 3s ease-in-out infinite;'>
            ⚡
        </div>
        """, unsafe_allow_html=True)

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

def display_search_results(search_query=None):
    """Display job search results with clear visibility"""
    if search_query:
        filtered_jobs = [job for job in SAMPLE_JOBS 
                        if search_query.lower() in job['title'].lower() or 
                        search_query.lower() in job['company'].lower() or
                        any(search_query.lower() in skill.lower() for skill in job['skills'])]
        
        if filtered_jobs:
            st.markdown(f"""
            <div class='glass-container'>
                <h2 style='color: #4ecdc4;'>🔍 Search Results for "{search_query}"</h2>
                <p style='color: #ddd;'>Found {len(filtered_jobs)} matching jobs</p>
            </div>
            """, unsafe_allow_html=True)
            
            for job in filtered_jobs:
                display_job_card(job)
        else:
            st.markdown("""
            <div class='glass-container'>
                <h3 style='color: #e74c3c;'>❌ No jobs found</h3>
                <p style='color: #ddd;'>Try a different search term or browse all jobs</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Show all jobs with a clear header
        st.markdown("""
        <div class='glass-container'>
            <h2 style='color: #4ecdc4;'>🌟 All Available Jobs</h2>
            <p style='color: #ddd;'>Browse through our current job openings</p>
        </div>
        """, unsafe_allow_html=True)
        
        for job in SAMPLE_JOBS:
            display_job_card(job)

def display_job_card(job):
    """Display individual job card with Streamlit components instead of HTML"""
    # Create a container with custom styling
    with st.container():
        st.markdown(f"""
        <div class='job-card'>
            <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;'>
                <div style='flex: 2;'>
                    <h3 style='color: white; margin: 0;'>{job['title']}</h3>
                    <p style='color: #ccc; margin: 5px 0;'>🏢 {job['company']}</p>
                    <p style='color: #ddd; margin: 5px 0;'>📍 {job['location']} • {job['type']}</p>
                </div>
                <div style='flex: 1; text-align: right;'>
                    {get_match_badge(job['match'])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Apply Now button using Streamlit
        if st.button(f"Apply to {job['title']} at {job['company']}", key=f"apply_{job['title']}"):
            st.success(f"Application submitted for {job['title']} at {job['company']}!")
        
        st.markdown("---")

def get_match_badge(match_score):
    """Return the appropriate match badge based on score"""
    if match_score >= 70:
        return f"<div class='match-badge'>🎯 {match_score}% Match</div>"
    elif match_score >= 50:
        return f"<div class='match-badge medium-match'>🎯 {match_score}% Match</div>"
    else:
        return f"<div class='match-badge low-match'>🎯 {match_score}% Match</div>"

def main():
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Dashboard"
    
    animated_header()
    
    # Initialize file upload state
    if 'resume_file' not in st.session_state:
        st.session_state.resume_file = None
    if 'jd_file' not in st.session_state:
        st.session_state.jd_file = None
    
    # Navigation sidebar
    with st.sidebar:
        st.markdown("""
        <div class='glass-container'>
            <h2 style='color: white; text-align: center;'>🧭 Navigation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Use a form to handle radio button changes properly
        with st.form("navigation_form"):
            page = st.radio(
                "Choose Section:",
                ["🏠 Dashboard", "📝 Upload Resume", "📋 Upload Job", "🔍 Search Jobs", "📊 Analytics"],
                index=["🏠 Dashboard", "📝 Upload Resume", "📋 Upload Job", "🔍 Search Jobs", "📊 Analytics"].index(st.session_state.current_page)
            )
            
            # Submit button to change page
            if st.form_submit_button("Go to Page"):
                st.session_state.current_page = page
                st.rerun()
    
    # Main content based on selected page
    if st.session_state.current_page == "🏠 Dashboard":
        st.markdown("""
        <div class='glass-container'>
            <h2 style='color: #4ecdc4;'>Welcome to AI Recruiter Pro</h2>
            <p style='color: #ddd;'>Upload your resume, search for jobs, and get AI-powered matching analytics.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show upload status if files exist
        if st.session_state.resume_file or st.session_state.jd_file:
            display_file_upload_feedback()
        
        # Quick actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📝 Upload Resume", use_container_width=True):
                st.session_state.current_page = "📝 Upload Resume"
                st.rerun()
        with col2:
            if st.button("📋 Upload Job", use_container_width=True):
                st.session_state.current_page = "📋 Upload Job"
                st.rerun()
        with col3:
            if st.button("🔍 Search Jobs", use_container_width=True):
                st.session_state.current_page = "🔍 Search Jobs"
                st.rerun()
        
        # Show some stats or previews
        st.markdown("""
        <div class='glass-container'>
            <h3 style='color: #4ecdc4;'>📈 Quick Stats</h3>
            <div style='display: flex; justify-content: space-between;'>
                <div style='text-align: center;'>
                    <h2 style='color: #ff6b6b;'>7</h2>
                    <p style='color: #ddd;'>Available Jobs</p>
                </div>
                <div style='text-align: center;'>
                    <h2 style='color: #4ecdc4;'>3</h2>
                    <p style='color: #ddd;'>High Match Jobs</p>
                </div>
                <div style='text-align: center;'>
                    <h2 style='color: #f39c12;'>2</h2>
                    <p style='color: #ddd;'>New This Week</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif st.session_state.current_page == "📝 Upload Resume":
        st.markdown("""
        <div class='glass-container'>
            <h2 style='color: #4ecdc4;'>📝 Upload Your Resume</h2>
            <p style='color: #ddd;'>Upload your resume to get personalized job matches</p>
        </div>
        """, unsafe_allow_html=True)
        
        resume_file = st.file_uploader(
            "Choose resume file (PDF, DOCX, TXT)",
            type=["pdf", "docx", "txt"],
            help="Upload your resume for analysis"
        )
        
        if resume_file:
            st.session_state.resume_file = resume_file
            st.success("✅ Resume uploaded successfully!")
            display_file_upload_feedback()
            
            # Show next steps
            st.markdown("""
            <div class='glass-container'>
                <h3 style='color: #4ecdc4;'>Next Steps</h3>
                <p style='color: #ddd;'>1. Upload a job description to get matching analysis</p>
                <p style='color: #ddd;'>2. Browse jobs to see how well you match</p>
                <p style='color: #ddd;'>3. Check analytics for detailed insights</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif st.session_state.current_page == "📋 Upload Job":
        st.markdown("""
        <div class='glass-container'>
            <h2 style='color: #4ecdc4;'>📋 Upload Job Description</h2>
            <p style='color: #ddd;'>Upload a job description to find matching candidates</p>
        </div>
        """, unsafe_allow_html=True)
        
        jd_file = st.file_uploader(
            "Choose job description file (PDF, DOCX, TXT)",
            type=["pdf", "docx", "txt"],
            help="Upload job description for matching"
        )
        
        if jd_file:
            st.session_state.jd_file = jd_file
            st.success("✅ Job Description uploaded successfully!")
            display_file_upload_feedback()
            
            # Show next steps
            st.markdown("""
            <div class='glass-container'>
                <h3 style='color: #4ecdc4;'>Next Steps</h3>
                <p style='color: #ddd;'>1. Go to Analytics to see matching results</p>
                <p style='color: #ddd;'>2. Browse jobs to compare with your uploaded JD</p>
            </div>
            """, unsafe_allow_html=True)
    
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
        
        # Display search results
        display_search_results(search_query)
    
    elif st.session_state.current_page == "📊 Analytics":
        st.markdown("""
        <div class='glass-container'>
            <h2 style='color: #4ecdc4;'>📊 Analytics & Insights</h2>
            <p style='color: #ddd;'>Get detailed analysis of your resume-job match</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.resume_file and st.session_state.jd_file:
            st.success("✅ Both files uploaded! Ready for analysis.")
            
            # Simulate analysis with progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(101):
                progress_bar.progress(i)
                status_text.text(f"Analyzing... {i}%")
                time.sleep(0.02)
            
            status_text.text("✅ Analysis complete!")
            
            # Show analysis results
            st.markdown("""
            <div class='glass-container'>
                <h3 style='color: #4ecdc4;'>📈 Match Analysis</h3>
                <div style='display: flex; justify-content: space-between;'>
                    <div style='text-align: center;'>
                        <h2 style='color: #ff6b6b;'>78%</h2>
                        <p style='color: #ddd;'>Overall Match</p>
                    </div>
                    <div style='text-align: center;'>
                        <h2 style='color: #4ecdc4;'>12/15</h2>
                        <p style='color: #ddd;'>Skills Matched</p>
                    </div>
                    <div style='text-align: center;'>
                        <h2 style='color: #f39c12;'>4.2/5</h2>
                        <p style='color: #ddd;'>Experience Level</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show skill breakdown
            st.markdown("""
            <div class='glass-container'>
                <h3 style='color: #4ecdc4;'>🔧 Skills Analysis</h3>
                <p style='color: #ddd;'>✅ Strong match: Python, SQL, Machine Learning</p>
                <p style='color: #ddd;'>⚠️ Partial match: TensorFlow, Data Visualization</p>
                <p style='color: #ddd;'>❌ Missing: Kubernetes, Advanced Statistics</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please upload both resume and job description to see analytics")
            
            # Show what's missing
            if not st.session_state.resume_file:
                st.error("❌ Resume not uploaded")
            if not st.session_state.jd_file:
                st.error("❌ Job Description not uploaded")

if __name__ == "__main__":
    main()