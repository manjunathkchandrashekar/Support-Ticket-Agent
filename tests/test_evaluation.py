import pytest

from src.evaluation.arize_evaluator import evaluate, evaluate_one
from src.evaluation.confidence_eval import average_confidence, confidence_report
from src.evaluation.groundedness_eval import groundedness, groundedness_report
from src.evaluation.route_accuracy_eval import route_accuracy, route_report
from src.utils.constants import Action
from src.utils.schemas import TicketDecision


def decision(action, confidence=0.8, sources=None, ticket_id="T-eval"):
    return TicketDecision(ticket_id, action, confidence, "Draft", "Reason", sources or [])


def test_route_accuracy_counts_missing_and_extra_predictions():
    assert route_accuracy([Action.AUTO_RESOLVE], ["Auto-Resolve", "Escalate"]) == 0.5
    report = route_report([Action.AUTO_RESOLVE, Action.REFUSE], ["Auto-Resolve"])
    assert report["correct"] == 1
    assert report["unexpected"] == 1


def test_confidence_report_handles_empty_and_distribution():
    assert average_confidence([]) == 0.0
    report = confidence_report([decision(Action.AUTO_RESOLVE, 0.9), decision(Action.ESCALATE, 0.6)])
    assert report["count"] == 2
    assert report["above_threshold"] == 1
    assert report["minimum"] == 0.6


def test_confidence_rejects_invalid_values():
    with pytest.raises(ValueError):
        average_confidence([decision(Action.AUTO_RESOLVE, 1.1)])
    with pytest.raises(TypeError):
        average_confidence([decision(Action.AUTO_RESOLVE, "high")])


def test_groundedness_only_requires_sources_for_auto_resolution():
    decisions = [
        decision(Action.AUTO_RESOLVE, sources=["faq.md"]),
        decision(Action.AUTO_RESOLVE, sources=[]),
        decision(Action.ESCALATE),
    ]
    assert [groundedness(item) for item in decisions] == [1.0, 0.0, 1.0]
    assert groundedness_report(decisions)["ungrounded_auto_resolutions"] == 1


def test_evaluation_payload_summarizes_actions_and_review_routes():
    decisions = [decision(Action.AUTO_RESOLVE, sources=["faq.md"]), decision(Action.REFUSE)]
    report = evaluate(decisions)
    single = evaluate_one(decisions[0])
    assert report["count"] == 2
    assert report["actions"] == {"Auto-Resolve": 1, "Refuse": 1}
    assert report["review_required"] == 1
    assert single["ticket_id"] == "T-eval"
    assert single["groundedness_score"] == 1.0