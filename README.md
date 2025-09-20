# 🎯 AI Recruiter Pro - Smart Hiring Platform

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-streamlit-app.streamlit.app/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://your-backend.onrender.com)

## 🌟 Live Demo

- **Frontend (Streamlit)**: [https://your-streamlit-app.streamlit.app/](https://your-streamlit-app.streamlit.app/)
- **Backend (FastAPI)**: [https://innomatics-backend.onrender.com](https://innomatics-backend.onrender.com)
- **API Documentation**: [https://innomatics-backend.onrender.com/docs](https://innomatics-backend.onrender.com/docs)

## 📋 Features

- ✅ Resume Upload & Parsing (PDF/DOCX/TXT)
- ✅ Job Description Analysis
- ✅ AI-Powered Matching Algorithm
- ✅ Skills Gap Analysis
- ✅ Match Score with Detailed Breakdown
- ✅ Analysis History & Dashboard
- ✅ Real-time Analytics

## 🛠️ Tech Stack

- **Frontend**: Streamlit, Python
- **Backend**: FastAPI, Python
- **Database**: SQLite/PostgreSQL
- **NLP**: spaCy, NLTK, Scikit-learn
- **Deployment**: Streamlit Cloud, Render

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run frontend (in new terminal)
streamlit run streamlit_app.py

📁 Project Structure

innomatics-ai-recruiter/
├── app/
│   ├── main.py          # FastAPI backend
│   ├── database.py      # Database configuration
│   └── models.py        # SQLAlchemy models
├── chains/              # AI processing chains
├── core/                # Core utilities
├── services/            # Business logic services
├── streamlit_app.py     # Streamlit frontend
├── requirements.txt     # Python dependencies
└── README.md           # This file

📊 API Endpoints

GET / - Health check
POST /analyze - Analyze resume vs JD
POST /analyze/upload - Analyze uploaded files
GET /analyses - Get analysis history
GET /analysis/{id} - Get specific analysis
