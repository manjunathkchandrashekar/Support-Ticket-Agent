"""Consistent, respectful responses for requests that need to be refused."""

REFUSAL_RESPONSE = (
    "I cannot assist with abusive or threatening requests. "
    "Please rephrase your request respectfully."
)

REFUSAL_TEMPLATES = {
    "abusive": REFUSAL_RESPONSE,
    "unsafe": "I cannot help with that request. Please provide a safe, legitimate support need.",
    "unsupported": "I cannot assist with that request, but I can help with an account or product support question.",
}


def refusal_response(reason="abusive"):
    """Return a known refusal response, falling back to the default wording."""
    if not isinstance(reason, str):
        raise TypeError("reason must be a string")
    return REFUSAL_TEMPLATES.get(reason.strip().lower(), REFUSAL_RESPONSE)