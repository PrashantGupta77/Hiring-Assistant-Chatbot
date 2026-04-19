import streamlit as st

from src.core.conversation_manager import ConversationManager
from src.core.state_machine import ConversationState
from src.models.session import ChatSession
from src.services.resume_service import ResumeService
from src.ui.components import render_chat_history, render_header, render_sidebar


def _initialize_session() -> None:
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = ChatSession()

    if "conversation_manager" not in st.session_state:
        st.session_state.conversation_manager = ConversationManager(st.session_state.chat_session)

    if "chat_initialized" not in st.session_state:
        st.session_state.chat_initialized = False

    if "processed_resume_name" not in st.session_state:
        st.session_state.processed_resume_name = None


def _reset_session() -> None:
    st.session_state.chat_session = ChatSession()
    st.session_state.conversation_manager = ConversationManager(st.session_state.chat_session)
    st.session_state.chat_initialized = False
    st.session_state.processed_resume_name = None


def _merge_resume_data_into_candidate(session: ChatSession, extracted_data: dict) -> None:
    candidate = session.candidate

    candidate.resume_uploaded = extracted_data.get("resume_uploaded", False)
    candidate.resume_file_name = extracted_data.get("resume_file_name")
    candidate.resume_text = extracted_data.get("resume_text")

    if extracted_data.get("full_name") and not candidate.full_name:
        candidate.full_name = extracted_data["full_name"]

    if extracted_data.get("email") and not candidate.email:
        candidate.email = extracted_data["email"]

    if extracted_data.get("phone") and not candidate.phone:
        candidate.phone = extracted_data["phone"]

    if extracted_data.get("years_of_experience") is not None and candidate.years_of_experience is None:
        candidate.years_of_experience = extracted_data["years_of_experience"]

    if extracted_data.get("desired_position") and not candidate.desired_position:
        candidate.desired_position = extracted_data["desired_position"]

    if extracted_data.get("tech_stack") and not candidate.tech_stack:
        candidate.tech_stack = extracted_data["tech_stack"]


def _handle_resume_upload(session: ChatSession, manager: ConversationManager) -> None:
    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"],
        help="Upload PDF, DOCX, or TXT resume to prefill candidate details.",
    )

    if not uploaded_file:
        return

    if st.session_state.processed_resume_name == uploaded_file.name:
        return

    resume_service = ResumeService()
    extracted_data = resume_service.extract_candidate_data(uploaded_file)
    _merge_resume_data_into_candidate(session, extracted_data)
    st.session_state.processed_resume_name = uploaded_file.name

    extracted_stack = extracted_data.get("tech_stack") or []
    extracted_name = extracted_data.get("full_name") or "Not detected"
    extracted_email = extracted_data.get("email") or "Not detected"
    upload_status = "successfully" if extracted_data.get("resume_uploaded") else "with limited extraction"

    session.add_message(
        "assistant",
        (
            f"Resume uploaded {upload_status}.\n\n"
            f"- File: {uploaded_file.name}\n"
            f"- Extracted Name: {extracted_name}\n"
            f"- Extracted Email: {extracted_email}\n"
            f"- Extracted Tech Stack: {', '.join(extracted_stack) if extracted_stack else 'Not detected'}\n\n"
            "You can continue the screening and update any information manually if needed."
        ),
    )

    if session.state in {
        ConversationState.COLLECT_NAME,
        ConversationState.COLLECT_EMAIL,
        ConversationState.COLLECT_PHONE,
        ConversationState.COLLECT_EXPERIENCE,
        ConversationState.COLLECT_POSITION,
        ConversationState.COLLECT_LOCATION,
        ConversationState.COLLECT_TECH_STACK,
    }:
        manager.advance_to_next_missing_step()
        st.rerun()


def run_streamlit_app() -> None:
    render_header()
    _initialize_session()

    session: ChatSession = st.session_state.chat_session
    manager: ConversationManager = st.session_state.conversation_manager

    render_sidebar(session)

    col1, col2 = st.columns([6, 1])
    with col1:
        _handle_resume_upload(session, manager)

    with col2:
        if st.button("🔄 Restart"):
            _reset_session()
            st.rerun()

    if not st.session_state.chat_initialized:
        manager.get_bot_response()
        st.session_state.chat_initialized = True
        st.rerun()

    render_chat_history(session)

    if session.state != ConversationState.END:
        user_input = st.chat_input("Type your response here...")

        if user_input:
            manager.get_bot_response(user_input)

            if session.state == ConversationState.GENERATE_QUESTIONS and not session.exit_requested:
                manager.get_bot_response()

            st.rerun()
    else:
        st.success("Screening session completed.")
        st.info("You can restart the session using the Restart button.")