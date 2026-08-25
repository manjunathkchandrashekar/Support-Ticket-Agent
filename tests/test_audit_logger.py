import json

import pytest

from src.logging.audit_logger import AuditLogger
from src.utils.constants import Action
from src.utils.schemas import TicketDecision


def make_decision(ticket_id="T-audit"):
    return TicketDecision(ticket_id, Action.ESCALATE, 0.95, "Draft", "Specialist review")


def test_log_writes_structured_decision_event(tmp_path):
    logger = AuditLogger(tmp_path / "audit.json")

    record = logger.log(make_decision(), metadata={"source": "support_graph"})

    assert record["ticket_id"] == "T-audit"
    assert record["event_type"] == "decision_created"
    assert record["metadata"] == {"source": "support_graph"}
    assert record["event_id"]
    assert record["timestamp"]
    assert json.loads((tmp_path / "audit.json").read_text()) == [record]


def test_new_logger_preserves_existing_records_and_filters_by_ticket(tmp_path):
    path = tmp_path / "audit.json"
    AuditLogger(path).log(make_decision("T-1"))
    logger = AuditLogger(path)
    logger.log_event("review_approved", "T-1", {"reviewer": "sam"})
    logger.log_event("processing_failed", "T-2", {"error": "timeout"})

    assert len(logger.records) == 3
    assert [record["event_type"] for record in logger.for_ticket("T-1")] == [
        "decision_created",
        "review_approved",
    ]


def test_invalid_event_data_is_rejected(tmp_path):
    logger = AuditLogger(tmp_path / "audit.json")

    with pytest.raises(ValueError):
        logger.log_event("", "T-1")
    with pytest.raises(TypeError):
        logger.log_event("processing_failed", "T-1", ["not", "a", "dict"])
    with pytest.raises(TypeError):
        logger.log("not a decision")


def test_corrupt_or_non_list_log_fails_loudly(tmp_path):
    path = tmp_path / "audit.json"
    path.write_text("{}")

    with pytest.raises(ValueError, match="JSON list"):
        AuditLogger(path)