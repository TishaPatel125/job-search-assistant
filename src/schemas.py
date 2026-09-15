from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class CompanyResearch(BaseModel):
    company_size: Optional[str] = None
    industry: Optional[str] = None
    recent_news: list[str] = Field(default_factory=list)
    culture_signals: list[str] = Field(default_factory=list)
    summary: str = ''

class JobPosting(BaseModel):
    job_title: str
    company_name: str
    location: Optional[str] = None
    remote_status: Optional[str] = None  # 'remote', 'hybrid', 'onsite', 'not listed'
    posting_age_days: Optional[int] = None
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    experience_level: Optional[str] = None
    years_experience: Optional[int] = None
    education_requirements: Optional[str] = None
    salary_range: Optional[str] = None
    key_responsibilities: list[str] = Field(default_factory=list)
    company_research: Optional[CompanyResearch] = None
    source_file: Optional[str] = None

class WorkExperience(BaseModel):
    title: str
    company: str
    duration: str
    responsibilities: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)

class Education(BaseModel):
    degree: str
    institution: str
    graduation_date: Optional[str] = None
    relevant_coursework: list[str] = Field(default_factory=list)

class Project(BaseModel):
    name: str
    description: str
    technologies: list[str] = Field(default_factory=list)

class Resume(BaseModel):
    name: str
    hard_skills: list[str] = Field(default_factory=list)
    soft_skills: list[str] = Field(default_factory=list)
    work_experience: list[WorkExperience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)

class SkillGap(BaseModel):
    skill: str
    level: str  # 'quick_win', 'short_term', 'medium_term', 'long_term'
    description: str
    action: str

class GapAnalysis(BaseModel):
    strengths: list[str] = Field(default_factory=list)
    gaps: list[SkillGap] = Field(default_factory=list)
    unique_value: list[str] = Field(default_factory=list)

class MarketAnalysis(BaseModel):
    total_postings_analyzed: int = 0
    most_common_skills: list[str] = Field(default_factory=list)
    typical_experience_levels: list[str] = Field(default_factory=list)
    education_requirements: list[str] = Field(default_factory=list)
    salary_ranges: list[str] = Field(default_factory=list)
    common_responsibilities: list[str] = Field(default_factory=list)
    trends: list[str] = Field(default_factory=list)
    industry_expectations: list[str] = Field(default_factory=list)

class LegitimacySignal(BaseModel):
    signal_type: str  # 'red_flag' or 'green_flag'
    category: str
    description: str
    evidence: str

class LegitimacyVerdict(Enum):
    GREEN = 'green'
    YELLOW = 'yellow'
    RED = 'red'

class LegitimacyAssessment(BaseModel):
    verdict: str  # 'green', 'yellow', 'red'
    confidence_score: float = Field(ge=0, le=1)
    signals: list[LegitimacySignal] = Field(default_factory=list)
    recommendation: str = ''

class FitCategory(BaseModel):
    category: str
    score: float  # 0.0 to 1.0
    matches: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    notes: str = ''

class FitAssessment(BaseModel):
    overall_score: float = Field(ge=0, le=100)
    recommendation: str = ''
    categories: list[FitCategory] = Field(default_factory=list)
    resume_suggestions: list[str] = Field(default_factory=list)
    cover_letter_points: list[str] = Field(default_factory=list)
    interview_questions: list[str] = Field(default_factory=list)
    skills_to_review: list[str] = Field(default_factory=list)
    company_research_points: list[str] = Field(default_factory=list)
    talking_points: list[str] = Field(default_factory=list)
