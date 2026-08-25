def groundedness(decision) -> float:
    return 1.0 if decision.action.value != 'Auto-Resolve' or decision.sources else 0.0
