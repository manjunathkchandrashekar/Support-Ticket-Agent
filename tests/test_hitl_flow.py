from src.hitl.approval_queue import ApprovalQueue
from src.hitl.approval_ui_stub import render
from src.hitl.reviewer_actions import approve, override, reject
from src.utils.constants import Action
from src.utils.schemas import TicketDecision


def test_approval_queue():
    queue = ApprovalQueue()
    queue.add('decision')
    assert queue.pending() == ['decision']


def make_decision(ticket_id="T-1"):
    return TicketDecision(ticket_id, Action.AUTO_RESOLVE, 0.91, "Draft", "FAQ match")


def test_approve_removes_decision_from_pending_queue():
    queue = ApprovalQueue()
    decision = queue.add(make_decision())

    approve(decision, reviewer="sam", note="Evidence is sufficient")

    assert queue.pending() == []
    assert decision.review_status == "approved"
    assert decision.reviewer == "sam"


def test_reject_keeps_original_action_but_marks_decision_unusable():
    decision = make_decision()

    reject(decision, reviewer="sam", note="Needs account verification")

    assert decision.action == Action.AUTO_RESOLVE
    assert decision.review_status == "rejected"


def test_override_preserves_original_action_for_audit():
    decision = make_decision()

    override(decision, Action.ESCALATE, reviewer="sam", note="High-value account")

    assert decision.action == Action.ESCALATE
    assert decision.original_action == Action.AUTO_RESOLVE
    assert decision.review_status == "overridden"


def test_queue_rejects_duplicate_ticket_and_can_find_or_remove_item():
    queue = ApprovalQueue()
    queue.add(make_decision("T-2"))

    try:
        queue.add(make_decision("T-2"))
        assert False, "duplicate ticket should fail"
    except ValueError:
        pass

    assert queue.get("T-2").ticket_id == "T-2"
    assert queue.remove("T-2").ticket_id == "T-2"
    assert queue.pending() == []


def test_ui_status_changes_when_review_is_completed():
    queue = ApprovalQueue()
    decision = queue.add(make_decision("T-3"))
    assert render(queue) == {"pending_count": 1, "status": "review required"}

    approve(decision)

    assert render(queue) == {"pending_count": 0, "status": "clear"}
