def average_confidence(decisions) -> float:
    return sum(item.confidence for item in decisions) / max(len(decisions), 1)
