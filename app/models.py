# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.database import Base
import datetime

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_text = Column(Text)
    jd_text = Column(Text)
    job_title = Column(String(255))
    company = Column(String(255))
    score = Column(Float)
    verdict = Column(String(50))
    matched_skills = Column(Text)
    missing_skills = Column(Text)
    hard_match_score = Column(Float)
    semantic_match_score = Column(Float)
    experience_match_score = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)