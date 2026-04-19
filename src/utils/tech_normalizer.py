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
    """
    if not raw_input or not raw_input.strip():
        return []

    text = raw_input.lower()

    # Split on commas, slashes, semicolons, pipes
    parts = re.split(r"[,/;|]+", text)

    normalized = []
    seen = set()

    for part in parts:
        cleaned = part.strip()

        if not cleaned:
            continue

        # direct match
        if cleaned in SUPPORTED_TECH_KEYWORDS:
            tech = SUPPORTED_TECH_KEYWORDS[cleaned]
            if tech not in seen:
                normalized.append(tech)
                seen.add(tech)
            continue

        # partial keyword match
        for keyword, standard_name in SUPPORTED_TECH_KEYWORDS.items():
            if keyword in cleaned:
                if standard_name not in seen:
                    normalized.append(standard_name)
                    seen.add(standard_name)
                break

    return normalized