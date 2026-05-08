
from pydantic import BaseModel


class PersonalInfo(BaseModel):
    """Personal information section of a resume."""
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str | None = ""
    website: str | None = ""
    github: str | None = ""
    summary: str = ""


class Education(BaseModel):
    """Education entry in a resume."""
    id: str
    school: str = ""
    degree: str = ""
    field: str = ""
    startDate: str = ""
    endDate: str = ""
    grade: str | None = ""
    description: str = ""


class WorkExperience(BaseModel):
    """Work experience entry in a resume."""
    id: str
    company: str = ""
    position: str = ""
    location: str = ""
    startDate: str = ""
    endDate: str = ""
    current: bool = False
    description: str = ""


class Project(BaseModel):
    """Project entry in a resume."""
    id: str
    name: str = ""
    technologies: list[str] = []
    startDate: str = ""
    endDate: str = ""
    ongoing: bool = False
    description: str = ""
    link: str | None = ""


class Skill(BaseModel):
    """Skill category in a resume."""
    id: str
    category: str = ""
    items: str = ""


class Custom(BaseModel):
    """Any section in the parsed resume goes to custom section"""
    id: str
    title: str = ""
    description: str = ""


class ResumeData(BaseModel):
    """Complete resume data structure matching frontend types."""
    personalInfo: PersonalInfo
    education: list[Education] = []
    workExperience: list[WorkExperience] = []
    projects: list[Project] = []
    skills: list[Skill] = []
    customSections: list[Custom] = []