from src.utils.constants import Action


def _action_value(action):
    return getattr(action, "value", action)


def route_accuracy(actual: list[Action], expected: list[str]) -> float:
    if not expected:
        return 1.0 if not actual else 0.0
    matches = sum(
        _action_value(item) == _action_value(target)
        for item, target in zip(actual, expected)
    )
    return matches / max(len(actual), len(expected))


def route_report(actual, expected):
    """Return accuracy details, including missing and unexpected predictions."""
    actual_values = [_action_value(item) for item in actual]
    expected_values = [_action_value(item) for item in expected]
    size = max(len(actual_values), len(expected_values))
    comparisons = [
        {
            "index": index,
            "actual": actual_values[index] if index < len(actual_values) else None,
            "expected": expected_values[index] if index < len(expected_values) else None,
            "match": index < len(actual_values)
            and index < len(expected_values)
            and actual_values[index] == expected_values[index],
        }
        for index in range(size)
    ]
    return {
        "accuracy": route_accuracy(actual, expected),
        "total": size,
        "correct": sum(item["match"] for item in comparisons),
        "missing": max(len(expected_values) - len(actual_values), 0),
        "unexpected": max(len(actual_values) - len(expected_values), 0),
        "comparisons": comparisons,
    }
