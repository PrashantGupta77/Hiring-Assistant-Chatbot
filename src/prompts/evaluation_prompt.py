def build_answer_evaluation_prompt(
    question: str,
    answer: str,
    tech_stack: list[str],
    years_of_experience: float | None,
    desired_position: str | None,
) -> str:
    stack_text = ", ".join(tech_stack) if tech_stack else "Not Provided"
    experience_text = str(years_of_experience) if years_of_experience is not None else "0"
    position_text = desired_position or "Not Provided"

    return f"""
You are an expert technical interviewer evaluating a candidate's screening answer.

Candidate context:
- Desired Position: {position_text}
- Years of Experience: {experience_text}
- Tech Stack: {stack_text}

Question:
{question}

Candidate Answer:
{answer}

Instructions:
1. Evaluate the answer for technical correctness, clarity, and completeness.
2. Give a score from 0 to 10.
3. Give short, professional feedback in 2 to 4 sentences.
4. Be fair for the candidate's experience level.
5. Return output in exactly this format:

Score: <number>
Feedback: <your feedback>

Example:
Score: 7.5
Feedback: Your answer demonstrates a good understanding of the concept and includes a practical explanation. However, it could be improved by mentioning performance trade-offs and a real-world use case.
""".strip()