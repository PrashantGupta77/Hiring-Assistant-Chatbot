import re
from typing import List

from config.constants import SUPPORTED_TECH_KEYWORDS


def normalize_tech_stack(raw_input: str) -> List[str]:
    """
    Converts user-entered tech stack into a clean, deduplicated list.

    Example:
    'python, django, postgres, docker'
    ->
    ['Python', 'Django', 'PostgreSQL', 'Docker']

    Improvements:
    - More conservative matching
    - Exact token/phrase matching preferred
    - Reduces false positives from long resume text
    """
    if not raw_input or not raw_input.strip():
        return []

    text = raw_input.lower()

    # Split on common delimiters and line breaks
    parts = re.split(r"[,/;|\n]+", text)

    normalized: List[str] = []
    seen = set()

    for part in parts:
        cleaned = part.strip()
        if not cleaned:
            continue

        # Normalize internal spacing
        cleaned = re.sub(r"\s+", " ", cleaned)

        # 1. Direct exact match
        if cleaned in SUPPORTED_TECH_KEYWORDS:
            tech = SUPPORTED_TECH_KEYWORDS[cleaned]
            if tech not in seen:
                normalized.append(tech)
                seen.add(tech)
            continue

        # 2. Conservative phrase match using word boundaries
        for keyword, standard_name in SUPPORTED_TECH_KEYWORDS.items():
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, cleaned):
                if standard_name not in seen:
                    normalized.append(standard_name)
                    seen.add(standard_name)
                break

    return normalized[:12]