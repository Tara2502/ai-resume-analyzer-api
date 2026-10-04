from pydantic import BaseModel


class ResumeAnalysis(BaseModel):
    summary: str
    skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]