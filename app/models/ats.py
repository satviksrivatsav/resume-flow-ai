# resume-flow-ai/app/models/ats.py
from pydantic import BaseModel, Field, ConfigDict, AliasChoices
from typing import Optional, Dict, List

class SectionScores(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    formatting: int = Field(default=0)
    keywords: int = Field(default=0)
    experience: int = Field(default=0)
    skills: int = Field(default=0)
    impact: int = Field(default=0)
    readability: int = Field(default=0)
    repetition: int = Field(default=0)
    grammar: int = Field(default=0)
    parse_rate: int = Field(default=0)

class RecruiterSimulation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    first_impression: str = Field(validation_alias=AliasChoices("first_impression", "First Impression"))
    likely_concerns: List[str] = Field(default_factory=list, validation_alias=AliasChoices("likely_concerns", "Likely Concerns"))
    likely_outcome: str = Field(validation_alias=AliasChoices("likely_outcome", "Likely Outcome"))

class JdMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    match_score: int = Field(default=0, validation_alias=AliasChoices("match_score", "Match Score"))
    missing_skills: List[str] = Field(default_factory=list, validation_alias=AliasChoices("missing_skills", "Missing Skills"))
    matched_skills: List[str] = Field(default_factory=list, validation_alias=AliasChoices("matched_skills", "Matched Skills"))

class BulletReview(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    original: str
    improved: str

class LlmAtsAnalysis(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    scores: SectionScores = Field(validation_alias=AliasChoices("scores", "Scores"))
    ats_warnings: List[str] = Field(default_factory=list, validation_alias=AliasChoices("ats_warnings", "ATS Warnings"))
    risks: List[str] = Field(default_factory=list, validation_alias=AliasChoices("risks", "Risks"))
    suggestions: List[str] = Field(default_factory=list, validation_alias=AliasChoices("suggestions", "Suggestions"))
    strong_keywords: List[str] = Field(default_factory=list, validation_alias=AliasChoices("strong_keywords", "Strong Keywords"))
    missing_keywords: List[str] = Field(default_factory=list, validation_alias=AliasChoices("missing_keywords", "Missing Keywords"))
    feedback: List[str] = Field(default_factory=list, validation_alias=AliasChoices("feedback", "Feedback"))
    bullet_reviews: List[BulletReview] = Field(default_factory=list, validation_alias=AliasChoices("bullet_reviews", "Bullet Reviews"))
    recruiter_simulation: RecruiterSimulation = Field(validation_alias=AliasChoices("recruiter_simulation", "Recruiter Simulation"))
    jd_match: Optional[JdMatch] = Field(default=None, validation_alias=AliasChoices("jd_match", "JD Match"))

class AtsReport(LlmAtsAnalysis):
    overall_score: int
    grade: str
    ats_essentials: Dict[str, bool]
