def route_from_decision(state):
    if state.decision is None:
        return "unknown"
    return getattr(state.decision.action, "value", state.decision.action)


def requires_human_review(state):
    return route_from_decision(state) in {"Escalate", "Refuse"}


def is_terminal(state):
    return route_from_decision(state) in {
        "Auto-Resolve",
        "Escalate",
        "Refuse",
        "Ask for More Information",
    }
