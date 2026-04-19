import io
import re
from typing import Any, Dict, List

from src.utils.tech_normalizer import normalize_tech_stack


class ResumeService:
    def extract_candidate_data(self, uploaded_file: Any) -> Dict[str, Any]:
        text = self._extract_text(uploaded_file)
        normalized_text = self._clean_text(text)

        extracted = {
            "resume_file_name": getattr(uploaded_file, "name", None),
            "resume_text": normalized_text,
            "resume_uploaded": bool(normalized_text),
            "full_name": self._extract_name(normalized_text),
            "email": self._extract_email(normalized_text),
            "phone": self._extract_phone(normalized_text),
            "years_of_experience": self._extract_experience(normalized_text),
            "desired_position": self._extract_desired_position(normalized_text),
            "tech_stack": self._extract_tech_stack(normalized_text),
        }

        return extracted

    def _extract_text(self, uploaded_file: Any) -> str:
        file_name = getattr(uploaded_file, "name", "").lower()

        if file_name.endswith(".txt"):
            return uploaded_file.getvalue().decode("utf-8", errors="ignore")

        if file_name.endswith(".pdf"):
            return self._extract_pdf_text(uploaded_file)

        if file_name.endswith(".docx"):
            return self._extract_docx_text(uploaded_file)

        return uploaded_file.getvalue().decode("utf-8", errors="ignore")

    @staticmethod
    def _extract_pdf_text(uploaded_file: Any) -> str:
        try:
            import pdfplumber

            pdf_bytes = io.BytesIO(uploaded_file.getvalue())
            extracted_pages = []

            with pdfplumber.open(pdf_bytes) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_pages.append(page_text)

            return "\n".join(extracted_pages)

        except Exception:
            return ""

    @staticmethod
    def _extract_docx_text(uploaded_file: Any) -> str:
        try:
            from docx import Document

            doc = Document(io.BytesIO(uploaded_file.getvalue()))
            paragraphs = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
            return "\n".join(paragraphs)
        except Exception:
            return ""

    @staticmethod
    def _clean_text(text: str) -> str:
        if not text:
            return ""

        text = text.replace("\xa0", " ")
        text = re.sub(r"\r", "\n", text)
        text = re.sub(r"\n{2,}", "\n", text)
        return text.strip()

    @staticmethod
    def _extract_email(text: str) -> str | None:
        match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        return match.group(0) if match else None

    @staticmethod
    def _extract_phone(text: str) -> str | None:
        match = re.search(r"(\+?\d[\d\s\-\(\)]{8,}\d)", text)
        return match.group(1).strip() if match else None

    @staticmethod
    def _extract_name(text: str) -> str | None:
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        for line in lines[:10]:
            if (
                len(line.split()) in {2, 3}
                and not any(char.isdigit() for char in line)
                and "@" not in line
                and len(line) < 50
            ):
                return line.title()

        return None

    @staticmethod
    def _extract_experience(text: str) -> float | None:
        patterns = [
            r"(\d+(?:\.\d+)?)\+?\s+years?\s+of\s+experience",
            r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\+?\s+years?",
            r"(\d+(?:\.\d+)?)\+?\s+years?\s+experience",
        ]

        lowered = text.lower()
        for pattern in patterns:
            match = re.search(pattern, lowered)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    return None

        return None

    @staticmethod
    def _extract_desired_position(text: str) -> str | None:
        patterns = [
            r"(?:desired position|position applied|role applied|applying for)\s*[:\-]?\s*([A-Za-z /-]+)",
            r"(data scientist|data analyst|machine learning engineer|software engineer|backend developer|frontend developer|full stack developer)",
        ]

        lowered = text.lower()
        for pattern in patterns:
            match = re.search(pattern, lowered)
            if match:
                return match.group(1).strip().title()

        return None

    @staticmethod
    def _extract_tech_stack(text: str) -> List[str]:
        lines = text.splitlines()

        possible_stack_lines = []
        for line in lines:
            lowered = line.lower()
            if any(
                keyword in lowered
                for keyword in ["skills", "technical skills", "tech stack", "technologies", "tools"]
            ):
                possible_stack_lines.append(line)

        combined_text = text
        if possible_stack_lines:
            combined_text = "\n".join(possible_stack_lines) + "\n" + text

        return normalize_tech_stack(combined_text)