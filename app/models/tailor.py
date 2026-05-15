from typing import Any, Optional
from pydantic import BaseModel
from app.models.resume import ResumeData

class TailorRequest(BaseModel):
    resume_data: ResumeData
    job_description: str
    sections_to_tailor: Optional[list[str]] = None

class TailoredSection(BaseModel):
    sectionId: str
    sectionName: str
    originalContent: Any
    tailoredContent: Any

class TailorResponse(BaseModel):
    tailoredSections: list[TailoredSection]
