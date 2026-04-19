from src.models.candidate import Candidate
from src.models.screening_result import ScreeningResult


class CandidateService:
    @staticmethod
    def build_summary(candidate: Candidate) -> str:
        return (
            "\nCandidate Information Summary:\n"
            f"- Full Name: {candidate.full_name}\n"
            f"- Email: {candidate.email}\n"
            f"- Phone: {candidate.phone}\n"
            f"- Years of Experience: {candidate.years_of_experience}\n"
            f"- Desired Position: {candidate.desired_position}\n"
            f"- Current Location: {candidate.current_location}\n"
            f"- Tech Stack: {', '.join(candidate.tech_stack) if candidate.tech_stack else 'Not Provided'}\n"
            f"- Resume Uploaded: {'Yes' if candidate.resume_uploaded else 'No'}\n"
            f"- Resume File: {candidate.resume_file_name or 'Not Provided'}\n"
        )

    @staticmethod
    def _derive_decision(average_score: float) -> tuple[str, str, str]:
        if average_score >= 8:
            return (
                "Strong Fit",
                "Shortlisted for Technical Interview",
                "Proceed to technical interview round",
            )

        if average_score >= 6:
            return (
                "Moderate Fit",
                "Needs Recruiter Review",
                "Schedule recruiter review or shortlist based on resume and role fit",
            )

        return (
            "Needs Further Review",
            "Rejected or On Hold",
            "Keep profile on hold or reject for current role",
        )

    @staticmethod
    def build_final_screening_result(candidate: Candidate) -> ScreeningResult:
        scores = list(candidate.answer_scores.values())
        average_score = round(sum(scores) / len(scores), 2) if scores else 0.0

        strengths = []
        improvement_areas = []

        for question, score in candidate.answer_scores.items():
            if score >= 7:
                strengths.append(f"Strong response in: {question}")
            else:
                improvement_areas.append(f"Needs improvement in: {question}")

        recommendation, decision_status, next_step = CandidateService._derive_decision(average_score)

        candidate.decision_status = decision_status
        candidate.next_step = next_step

        return ScreeningResult(
            candidate_name=candidate.full_name or "Unknown Candidate",
            desired_position=candidate.desired_position or "Not Specified",
            average_score=average_score,
            strengths=strengths[:3],
            improvement_areas=improvement_areas[:3],
            final_recommendation=recommendation,
            decision_status=decision_status,
            next_step=next_step,
        )