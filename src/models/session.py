from typing import List, Optional
from pydantic import BaseModel, Field

from src.core.state_machine import ConversationState
from src.models.candidate import Candidate


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatSession(BaseModel):
    candidate: Candidate = Field(default_factory=Candidate)
    state: ConversationState = ConversationState.GREETING
    chat_history: List[ChatMessage] = Field(default_factory=list)
    current_question_index: int = 0
    screening_complete: bool = False
    detected_language: Optional[str] = "en"
    exit_requested: bool = False

    def add_message(self, role: str, content: str) -> None:
        self.chat_history.append(ChatMessage(role=role, content=content))