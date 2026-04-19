from src.models.candidate import Candidate


def build_question_generation_prompt(candidate: Candidate) -> str:
    """
    Creates a structured prompt for generating technical screening questions
    based on the candidate's tech stack and experience.
    """
    tech_stack = ", ".join(candidate.tech_stack) if candidate.tech_stack else "Not Provided"
    experience = candidate.years_of_experience if candidate.years_of_experience is not None else 0
    desired_position = candidate.desired_position or "Not Provided"

    return f"""
You are an expert technical hiring assistant for a recruitment agency called TalentScout.

Your task is to generate technical screening questions for a candidate.

Candidate details:
- Desired Position: {desired_position}
- Years of Experience: {experience}
- Tech Stack: {tech_stack}

Instructions:
1. Generate between 3 and 5 technical screening questions.
2. Questions must be based only on the declared tech stack.
3. Questions should be clear, concise, and relevant for an interview screening round.
4. Adjust the difficulty according to the candidate's years of experience.
5. Include a mix of conceptual and practical questions.
6. Do not ask HR questions.
7. Do not include answers or explanations.
8. Return the output as a numbered list only.

Example output:
1. What is the difference between list and tuple in Python?
2. How does Django ORM help in database operations?
3. What are database indexes and why are they useful?

Now generate the questions.
""".strip()