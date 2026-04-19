from enum import Enum


class ConversationState(str, Enum):
    GREETING = "greeting"
    COLLECT_NAME = "collect_name"
    COLLECT_EMAIL = "collect_email"
    COLLECT_PHONE = "collect_phone"
    COLLECT_EXPERIENCE = "collect_experience"
    COLLECT_POSITION = "collect_position"
    COLLECT_LOCATION = "collect_location"
    COLLECT_TECH_STACK = "collect_tech_stack"
    CONFIRM_INFO = "confirm_info"
    GENERATE_QUESTIONS = "generate_questions"
    ASK_QUESTIONS = "ask_questions"
    EVALUATE_ANSWER = "evaluate_answer"
    SCREENING_SUMMARY = "screening_summary"
    END = "end"