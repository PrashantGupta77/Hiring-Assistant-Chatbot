from typing import Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


class Candidate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    years_of_experience: Optional[float] = None
    desired_position: Optional[str] = None
    current_location: Optional[str] = None

    tech_stack: List[str] = Field(default_factory=list)
    technical_questions: List[str] = Field(default_factory=list)
    answers: Dict[str, str] = Field(default_factory=dict)

    answer_scores: Dict[str, float] = Field(default_factory=dict)
    answer_feedback: Dict[str, str] = Field(default_factory=dict)

    resume_uploaded: bool = False
    resume_file_name: Optional[str] = None
    resume_text: Optional[str] = None

    decision_status: Optional[str] = None
    next_step: Optional[str] = None

    def missing_fields(self) -> List[str]:
        missing = []

        if not self.full_name:
            missing.append("full_name")
        if not self.email:
            missing.append("email")
        if not self.phone:
            missing.append("phone")
        if self.years_of_experience is None:
            missing.append("years_of_experience")
        if not self.desired_position:
            missing.append("desired_position")
        if not self.current_location:
            missing.append("current_location")
        if not self.tech_stack:
            missing.append("tech_stack")

        return missing