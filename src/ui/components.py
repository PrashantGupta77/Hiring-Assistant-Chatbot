import streamlit as st

from src.models.session import ChatSession


def render_sidebar(session: ChatSession) -> None:
    completed_questions = len(session.candidate.answers)
    total_questions = len(session.candidate.technical_questions)

    with st.sidebar:
        st.title("TalentScout")
        st.caption("AI Hiring Assistant")

        st.markdown("### Resume Upload")
        st.write(f"**Resume Uploaded:** {'Yes' if session.candidate.resume_uploaded else 'No'}")
        st.write(f"**Resume File:** {session.candidate.resume_file_name or '-'}")

        st.markdown("### Screening Status")
        st.write(f"**Current State:** `{session.state.value}`")
        st.write(f"**Questions Completed:** {completed_questions}")
        st.write(f"**Total Questions:** {total_questions}")
        st.write(f"**Screening Complete:** {'Yes' if session.screening_complete else 'No'}")

        st.markdown("### Candidate Snapshot")
        st.write(f"**Name:** {session.candidate.full_name or '-'}")
        st.write(f"**Email:** {session.candidate.email or '-'}")
        st.write(f"**Phone:** {session.candidate.phone or '-'}")
        st.write(f"**Experience:** {session.candidate.years_of_experience or '-'}")
        st.write(f"**Position:** {session.candidate.desired_position or '-'}")
        st.write(f"**Location:** {session.candidate.current_location or '-'}")
        st.write(
            f"**Tech Stack:** "
            f"{', '.join(session.candidate.tech_stack) if session.candidate.tech_stack else '-'}"
        )

        st.markdown("### Decision")
        st.write(f"**Decision Status:** {session.candidate.decision_status or '-'}")
        st.write(f"**Next Step:** {session.candidate.next_step or '-'}")


def render_chat_history(session: ChatSession) -> None:
    for msg in session.chat_history:
        with st.chat_message(msg.role):
            st.markdown(msg.content)


def render_header() -> None:
    st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖", layout="wide")

    st.title("🤖 TalentScout Hiring Assistant")
    st.markdown(
        "Welcome to the AI-powered candidate screening assistant. "
        "You can upload a resume, complete your details, and answer the generated technical questions."
    )