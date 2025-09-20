# app/models.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# SQLAlchemy Base for database models
Base = declarative_base()

# ========== SQLAlchemy Database Models ==========

class ResumeAnalysisDB(Base):
    __tablename__ = "resume_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, unique=True, index=True)
    resume_filename = Column(String)
    jd_filename = Column(String)
    match_score = Column(Float)
    matching_skills = Column(JSON)  # Store as JSON list
    missing_skills = Column(JSON)   # Store as JSON list
    resume_skills = Column(JSON)    # Store as JSON dict
    jd_skills = Column(JSON)        # Store as JSON dict
    llm_analysis = Column(JSON)     # Store as JSON dict
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ResumeAnalysisDB {self.analysis_id}>"

class AuditLogDB(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, index=True)
    action = Column(String)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AuditLogDB {self.action} for {self.analysis_id}>"

# ========== Pydantic Request/Response Models ==========

class AnalysisRequest(BaseModel):
    resume_text: str
    jd_text: str

class SkillMatchResult(BaseModel):
    matching_skills: List[str]
    missing_skills: List[str]
    hard_skills: List[str]
    soft_skills: List[str]

class BasicResponse(BaseModel):
    message: str
    data: Optional[Dict[str, Any]] = None
    success: bool = True

class AnalysisResponse(BaseModel):
    id: str
    resume_filename: str
    jd_filename: str
    match_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    resume_skills: Dict[str, List[str]]
    jd_skills: Dict[str, List[str]]
    llm_analysis: Dict[str, str]
    created_at: str

class AuditLogResponse(BaseModel):
    id: int
    analysis_id: str
    action: str
    details: str
    timestamp: str

# Optional: Helper models for database operations
class DBAnalysisCreate(BaseModel):
    analysis_id: str
    resume_filename: str
    jd_filename: str
    match_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    resume_skills: Dict[str, List[str]]
    jd_skills: Dict[str, List[str]]
    llm_analysis: Dict[str, str]

class DBAuditLogCreate(BaseModel):
    analysis_id: str
    action: str
    details: str