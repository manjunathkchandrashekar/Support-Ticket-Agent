from src.utils.constants import Action


def groundedness(decision) -> float:
    """Score whether an auto-resolution has supporting retrieval sources."""
    action = getattr(decision.action, "value", decision.action)
    return 1.0 if action != Action.AUTO_RESOLVE.value or decision.sources else 0.0


def groundedness_report(decisions):
    scores = [groundedness(decision) for decision in decisions]
    auto_resolutions = [
        decision for decision in decisions
        if getattr(decision.action, "value", decision.action) == Action.AUTO_RESOLVE.value
    ]
    grounded_auto_resolutions = [decision for decision in auto_resolutions if decision.sources]
    return {
        "count": len(decisions),
        "average": sum(scores) / len(scores) if scores else 0.0,
        "auto_resolutions": len(auto_resolutions),
        "grounded_auto_resolutions": len(grounded_auto_resolutions),
        "ungrounded_auto_resolutions": len(auto_resolutions) - len(grounded_auto_resolutions),
    }
