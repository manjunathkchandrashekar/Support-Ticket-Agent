from collections import Counter

from .confidence_eval import average_confidence
from .groundedness_eval import groundedness_report


def evaluate(decisions):
    """Build a provider-neutral evaluation payload suitable for export."""
    actions = [getattr(decision.action, "value", decision.action) for decision in decisions]
    return {
        "count": len(decisions),
        "average_confidence": average_confidence(decisions),
        "groundedness": groundedness_report(decisions),
        "actions": dict(Counter(actions)),
        "review_required": sum(action in {"Escalate", "Refuse"} for action in actions),
    }


def evaluate_one(decision):
    """Evaluate one decision using the same batch schema."""
    result = evaluate([decision])
    result["ticket_id"] = decision.ticket_id
    result["action"] = getattr(decision.action, "value", decision.action)
    result["groundedness_score"] = groundedness_report([decision])["average"]
    return result
