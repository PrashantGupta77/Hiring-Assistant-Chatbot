import re
from typing import Optional, Tuple

from pydantic import ValidationError
from src.models.candidate import Candidate


def validate_email(email: str) -> bool:
    try:
        Candidate(email=email)
        return True
    except ValidationError:
        return False


def validate_phone(phone: str) -> bool:
    """
    Basic phone validation:
    - allows +, spaces, dashes, parentheses
    - expects 10 to 15 digits total
    """
    digits_only = re.sub(r"\D", "", phone)
    return 10 <= len(digits_only) <= 15


def validate_experience(value: str) -> Tuple[bool, Optional[float]]:
    try:
        years = float(value.strip())
        if years < 0 or years > 50:
            return False, None
        return True, years
    except ValueError:
        return False, None


def is_non_empty_text(value: str) -> bool:
    return bool(value and value.strip())