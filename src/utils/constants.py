from enum import StrEnum


class Action(StrEnum):
    AUTO_RESOLVE = "Auto-Resolve"
    ESCALATE = "Escalate"
    REFUSE = "Refuse"
    MORE_INFORMATION = "Ask for More Information"


DEFAULT_CONFIDENCE_THRESHOLD = 0.72
