from typing import List

from pydantic import BaseModel, Field


class EvaluatedAnswer(BaseModel):
    question: str
    answer: str
    score: float
    feedback: str


class ScreeningResult(BaseModel):
    candidate_name: str
    desired_position: str
    average_score: float
    strengths: List[str] = Field(default_factory=list)
    improvement_areas: List[str] = Field(default_factory=list)
    final_recommendation: str = "Needs Further Review"
    decision_status: str = "Pending Recruiter Review"
    next_step: str = "Manual recruiter review required"