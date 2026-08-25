from src.utils.constants import DEFAULT_CONFIDENCE_THRESHOLD


def _validate_confidence(confidence):
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
        raise TypeError("confidence must be numeric")
    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")


def average_confidence(decisions) -> float:
    if not decisions:
        return 0.0
    for item in decisions:
        _validate_confidence(item.confidence)
    return sum(item.confidence for item in decisions) / len(decisions)


def confidence_report(decisions, threshold=DEFAULT_CONFIDENCE_THRESHOLD):
    """Summarize confidence distribution and threshold compliance."""
    _validate_confidence(threshold)
    values = []
    for item in decisions:
        _validate_confidence(item.confidence)
        values.append(item.confidence)
    if not values:
        return {"count": 0, "average": 0.0, "minimum": 0.0, "maximum": 0.0, "above_threshold": 0}
    return {
        "count": len(values),
        "average": sum(values) / len(values),
        "minimum": min(values),
        "maximum": max(values),
        "above_threshold": sum(value >= threshold for value in values),
    }
