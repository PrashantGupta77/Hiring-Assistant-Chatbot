from config.constants import EXIT_KEYWORDS
from src.core.state_machine import ConversationState
from src.models.session import ChatSession
from src.services.candidate_service import CandidateService
from src.services.question_service import QuestionService
from src.services.scoring_service import ScoringService
from src.utils.tech_normalizer import normalize_tech_stack
from src.utils.validators import (
    is_non_empty_text,
    validate_email,
    validate_experience,
    validate_phone,
)


class ConversationManager:
    def __init__(self, session: ChatSession):
        self.session = session
        self.question_service = QuestionService()
        self.scoring_service = ScoringService()

    def get_bot_response(self, user_input: str | None = None) -> str:
        if user_input is not None:
            cleaned_input = user_input.strip()
            self.session.add_message("user", cleaned_input)

            if cleaned_input.lower() in EXIT_KEYWORDS:
                self.session.exit_requested = True
                self.session.state = ConversationState.END
                farewell = (
                    "Thank you for your time. Your screening session has been closed. "
                    "Our team will review your profile and get back to you with the next steps."
                )
                self.session.add_message("assistant", farewell)
                return farewell

        current_state = self.session.state

        if current_state == ConversationState.GREETING:
            return self._handle_greeting()

        if current_state == ConversationState.COLLECT_NAME:
            return self._handle_name(user_input)

        if current_state == ConversationState.COLLECT_EMAIL:
            return self._handle_email(user_input)

        if current_state == ConversationState.COLLECT_PHONE:
            return self._handle_phone(user_input)

        if current_state == ConversationState.COLLECT_EXPERIENCE:
            return self._handle_experience(user_input)

        if current_state == ConversationState.COLLECT_POSITION:
            return self._handle_position(user_input)

        if current_state == ConversationState.COLLECT_LOCATION:
            return self._handle_location(user_input)

        if current_state == ConversationState.COLLECT_TECH_STACK:
            return self._handle_tech_stack(user_input)

        if current_state == ConversationState.CONFIRM_INFO:
            return self._handle_confirmation()

        if current_state == ConversationState.GENERATE_QUESTIONS:
            return self._handle_generate_questions()

        if current_state == ConversationState.ASK_QUESTIONS:
            return self._handle_ask_questions()

        if current_state == ConversationState.EVALUATE_ANSWER:
            return self._handle_evaluate_answer(user_input)

        if current_state == ConversationState.SCREENING_SUMMARY:
            return self._handle_screening_summary()

        if current_state == ConversationState.END:
            end_message = "The conversation has already ended."
            self.session.add_message("assistant", end_message)
            return end_message

        fallback = "I’m sorry, something went wrong in the conversation flow."
        self.session.add_message("assistant", fallback)
        return fallback

    def advance_to_next_missing_step(self) -> str:
        candidate = self.session.candidate

        if not candidate.full_name:
            self.session.state = ConversationState.COLLECT_NAME
            message = "Please enter your full name."
        elif not candidate.email:
            self.session.state = ConversationState.COLLECT_EMAIL
            message = "Please enter your email address."
        elif not candidate.phone:
            self.session.state = ConversationState.COLLECT_PHONE
            message = "Please enter your phone number."
        elif candidate.years_of_experience is None:
            self.session.state = ConversationState.COLLECT_EXPERIENCE
            message = "How many years of professional experience do you have?"
        elif not candidate.desired_position:
            self.session.state = ConversationState.COLLECT_POSITION
            message = "What position(s) are you applying for?"
        elif not candidate.current_location:
            self.session.state = ConversationState.COLLECT_LOCATION
            message = "Please share your current location."
        elif not candidate.tech_stack:
            self.session.state = ConversationState.COLLECT_TECH_STACK
            message = (
                "Now please enter your tech stack.\n"
                "You can include programming languages, frameworks, databases, and tools.\n"
                "Example: Python, Django, PostgreSQL, Docker, Git"
            )
        else:
            self.session.state = ConversationState.CONFIRM_INFO
            return self._handle_confirmation()

        self.session.add_message("assistant", message)
        return message

    def _handle_greeting(self) -> str:
        self.session.state = ConversationState.COLLECT_NAME
        message = (
            "Hello! Welcome to TalentScout Hiring Assistant.\n"
            "I’ll help with your initial screening by collecting your details and tech stack.\n\n"
            "You may also upload your resume before answering the questions.\n\n"
            "Let’s begin.\n"
            "Please enter your full name."
        )
        self.session.add_message("assistant", message)
        return message

    def _handle_name(self, user_input: str | None) -> str:
        if not user_input or not is_non_empty_text(user_input):
            message = "Please enter a valid full name."
            self.session.add_message("assistant", message)
            return message

        self.session.candidate.full_name = user_input.strip()
        return self.advance_to_next_missing_step()

    def _handle_email(self, user_input: str | None) -> str:
        if not user_input or not validate_email(user_input.strip()):
            message = "Please enter a valid email address."
            self.session.add_message("assistant", message)
            return message

        self.session.candidate.email = user_input.strip()
        return self.advance_to_next_missing_step()

    def _handle_phone(self, user_input: str | None) -> str:
        if not user_input or not validate_phone(user_input.strip()):
            message = "Please enter a valid phone number with 10 to 15 digits."
            self.session.add_message("assistant", message)
            return message

        self.session.candidate.phone = user_input.strip()
        return self.advance_to_next_missing_step()

    def _handle_experience(self, user_input: str | None) -> str:
        if not user_input:
            message = "Please enter your years of experience."
            self.session.add_message("assistant", message)
            return message

        is_valid, years = validate_experience(user_input.strip())
        if not is_valid or years is None:
            message = "Please enter a valid number for years of experience, for example: 2 or 3.5"
            self.session.add_message("assistant", message)
            return message

        self.session.candidate.years_of_experience = years
        return self.advance_to_next_missing_step()

    def _handle_position(self, user_input: str | None) -> str:
        if not user_input or not is_non_empty_text(user_input):
            message = "Please enter your desired position."
            self.session.add_message("assistant", message)
            return message

        self.session.candidate.desired_position = user_input.strip()
        return self.advance_to_next_missing_step()

    def _handle_location(self, user_input: str | None) -> str:
        if not user_input or not is_non_empty_text(user_input):
            message = "Please enter your current location."
            self.session.add_message("assistant", message)
            return message

        self.session.candidate.current_location = user_input.strip()
        return self.advance_to_next_missing_step()

    def _handle_tech_stack(self, user_input: str | None) -> str:
        if not user_input or not is_non_empty_text(user_input):
            message = "Please enter at least one technology in your tech stack."
            self.session.add_message("assistant", message)
            return message

        normalized_stack = normalize_tech_stack(user_input.strip())

        if not normalized_stack:
            message = (
                "I could not identify the technologies clearly. "
                "Please enter your stack like: Python, Flask, MySQL, Docker"
            )
            self.session.add_message("assistant", message)
            return message

        self.session.candidate.tech_stack = normalized_stack
        self.session.state = ConversationState.CONFIRM_INFO
        return self._handle_confirmation()

    def _handle_confirmation(self) -> str:
        summary = CandidateService.build_summary(self.session.candidate)

        message = (
            "Thank you. I have collected your basic details successfully.\n"
            f"{summary}\n"
            "Next, I will generate technical screening questions based on your tech stack."
        )

        self.session.state = ConversationState.GENERATE_QUESTIONS
        self.session.add_message("assistant", message)
        return message

    def _handle_generate_questions(self) -> str:
        try:
            questions = self.question_service.generate_questions(self.session.candidate)
            self.session.candidate.technical_questions = questions
            self.session.state = ConversationState.ASK_QUESTIONS
            self.session.current_question_index = 0

            return self._handle_ask_questions()

        except Exception:
            message = (
                "I encountered an issue while generating technical questions. "
                "Please try again later or restart the screening session."
            )
            self.session.add_message("assistant", message)
            return message

    def _handle_ask_questions(self) -> str:
        questions = self.session.candidate.technical_questions
        index = self.session.current_question_index

        if index >= len(questions):
            self.session.state = ConversationState.SCREENING_SUMMARY
            return self._handle_screening_summary()

        question = questions[index]
        self.session.state = ConversationState.EVALUATE_ANSWER

        message = (
            f"Technical Question {index + 1} of {len(questions)}:\n"
            f"{question}\n\n"
            "Please provide your answer."
        )
        self.session.add_message("assistant", message)
        return message

    def _handle_evaluate_answer(self, user_input: str | None) -> str:
        if not user_input or not is_non_empty_text(user_input):
            message = "Please provide a valid answer to continue."
            self.session.add_message("assistant", message)
            return message

        index = self.session.current_question_index
        question = self.session.candidate.technical_questions[index]
        answer = user_input.strip()

        self.session.candidate.answers[question] = answer

        try:
            score, feedback = self.scoring_service.evaluate_answer(
                candidate=self.session.candidate,
                question=question,
                answer=answer,
            )
        except Exception:
            score, feedback = 0.0, "Evaluation could not be completed at this time."

        self.session.candidate.answer_scores[question] = score
        self.session.candidate.answer_feedback[question] = feedback
        self.session.current_question_index += 1

        evaluation_text = (
            "Evaluation Result:\n"
            f"- Score: {score}/10\n"
            f"- Feedback: {feedback}\n\n"
        )

        if self.session.current_question_index < len(self.session.candidate.technical_questions):
            next_index = self.session.current_question_index
            next_question = self.session.candidate.technical_questions[next_index]

            self.session.state = ConversationState.EVALUATE_ANSWER
            message = (
                evaluation_text
                + f"Technical Question {next_index + 1} of {len(self.session.candidate.technical_questions)}:\n"
                + f"{next_question}\n\n"
                + "Please provide your answer."
            )
            self.session.add_message("assistant", message)
            return message

        result = CandidateService.build_final_screening_result(self.session.candidate)
        self.session.screening_complete = True
        self.session.state = ConversationState.END

        strengths_text = "\n".join([f"- {item}" for item in result.strengths]) or "- None identified"
        improvements_text = "\n".join([f"- {item}" for item in result.improvement_areas]) or "- None identified"

        summary_text = (
            "Screening Summary:\n"
            f"- Candidate Name: {result.candidate_name}\n"
            f"- Desired Position: {result.desired_position}\n"
            f"- Average Score: {result.average_score}/10\n"
            f"- Final Recommendation: {result.final_recommendation}\n"
            f"- Decision Status: {result.decision_status}\n"
            f"- Next Step: {result.next_step}\n\n"
            f"Strengths:\n{strengths_text}\n\n"
            f"Improvement Areas:\n{improvements_text}\n\n"
            "Thank you for completing the screening. Our team will review your profile and reach out regarding the next steps."
        )

        message = evaluation_text + summary_text
        self.session.add_message("assistant", message)
        return message

    def _handle_screening_summary(self) -> str:
        result = CandidateService.build_final_screening_result(self.session.candidate)
        self.session.screening_complete = True
        self.session.state = ConversationState.END

        strengths_text = "\n".join([f"- {item}" for item in result.strengths]) or "- None identified"
        improvements_text = "\n".join([f"- {item}" for item in result.improvement_areas]) or "- None identified"

        message = (
            "Screening Summary:\n"
            f"- Candidate Name: {result.candidate_name}\n"
            f"- Desired Position: {result.desired_position}\n"
            f"- Average Score: {result.average_score}/10\n"
            f"- Final Recommendation: {result.final_recommendation}\n"
            f"- Decision Status: {result.decision_status}\n"
            f"- Next Step: {result.next_step}\n\n"
            f"Strengths:\n{strengths_text}\n\n"
            f"Improvement Areas:\n{improvements_text}\n\n"
            "Thank you for completing the screening. Our team will review your profile and reach out regarding the next steps."
        )

        self.session.add_message("assistant", message)
        return message