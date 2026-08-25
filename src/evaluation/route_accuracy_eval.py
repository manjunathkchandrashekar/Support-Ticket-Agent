from src.utils.constants import Action


def route_accuracy(actual: list[Action], expected: list[str]) -> float:
    return sum(item.value == target for item, target in zip(actual, expected)) / max(len(expected), 1)
