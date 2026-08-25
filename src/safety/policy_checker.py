import re

ABUSE_TERMS = {"hate", "threaten", "kill", "slur", "abusive"}


def contains_abusive_content(text: str) -> bool:
    terms = set(re.findall(r"[a-z0-9]+", text.lower()))
    return bool(terms & ABUSE_TERMS)
