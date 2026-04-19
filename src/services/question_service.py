import re
from typing import List

from config.settings import settings
from src.models.candidate import Candidate
from src.prompts.question_generation_prompt import build_question_generation_prompt
from src.services.llm_service import LLMService


class QuestionService:
    def __init__(self) -> None:
        self.llm_service = LLMService()

    def generate_questions(self, candidate: Candidate) -> List[str]:
        """
        Generate technical screening questions using Groq.
        """
        prompt = build_question_generation_prompt(candidate)
        raw_response = self.llm_service.generate_response(prompt)
        questions = self._parse_numbered_questions(raw_response)

        if len(questions) < settings.MIN_TECH_QUESTIONS:
            raise ValueError(
                f"Expected at least {settings.MIN_TECH_QUESTIONS} valid questions, "
                f"but got {len(questions)}."
            )

        return questions[: settings.MAX_TECH_QUESTIONS]

    @staticmethod
    def _parse_numbered_questions(response_text: str) -> List[str]:
        """
        Extract only numbered questions from an LLM response.

        Example:
        1. Question one?
        2. Question two?
        """
        questions = []

        for line in response_text.splitlines():
            line = line.strip()
            if not line:
                continue

            if re.match(r"^\d+[\).\s-]+", line):
                cleaned = re.sub(r"^\d+[\).\s-]+", "", line).strip()
                if cleaned:
                    questions.append(cleaned)

        return questions