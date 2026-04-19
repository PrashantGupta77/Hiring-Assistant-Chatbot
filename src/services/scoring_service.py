import re
from typing import Tuple

from src.models.candidate import Candidate
from src.prompts.evaluation_prompt import build_answer_evaluation_prompt
from src.services.llm_service import LLMService


class ScoringService:
    def __init__(self) -> None:
        self.llm_service = LLMService()

    def evaluate_answer(self, candidate: Candidate, question: str, answer: str) -> Tuple[float, str]:
        prompt = build_answer_evaluation_prompt(
            question=question,
            answer=answer,
            tech_stack=candidate.tech_stack,
            years_of_experience=candidate.years_of_experience,
            desired_position=candidate.desired_position,
        )

        raw_response = self.llm_service.generate_response(prompt)
        return self._parse_evaluation(raw_response)

    @staticmethod
    def _parse_evaluation(response_text: str) -> Tuple[float, str]:
        score_match = re.search(r"Score:\s*([0-9]+(?:\.[0-9]+)?)", response_text, re.IGNORECASE)
        feedback_match = re.search(r"Feedback:\s*(.*)", response_text, re.IGNORECASE | re.DOTALL)

        score = 0.0
        feedback = "No feedback generated."

        if score_match:
            score = float(score_match.group(1))
            score = max(0.0, min(score, 10.0))

        if feedback_match:
            feedback = feedback_match.group(1).strip()

        return score, feedback