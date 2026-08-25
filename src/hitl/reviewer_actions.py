from datetime import datetime, timezone

from src.utils.constants import Action


def _record_review(decision, status, reviewer, note):
    if not reviewer or not reviewer.strip():
        raise ValueError("reviewer is required")
    decision.review_status = status
    decision.reviewer = reviewer.strip()
    decision.review_note = note.strip() if note else None
    decision.reviewed_at = datetime.now(timezone.utc).isoformat()
    return decision


def approve(decision, reviewer="human", note=None):
    """Approve the generated response without changing its action."""
    return _record_review(decision, "approved", reviewer, note)


def reject(decision, reviewer="human", note=None):
    """Reject a response so it cannot be treated as an approved decision."""
    return _record_review(decision, "rejected", reviewer, note)


def override(decision, action, reviewer="human", note=None):
    """Replace the proposed action while retaining the original for auditing."""
    try:
        action = Action(action)
    except ValueError as error:
        raise ValueError(f"unsupported action: {action!r}") from error
    if decision.original_action is None:
        decision.original_action = decision.action
    decision.action = action
    return _record_review(decision, "overridden", reviewer, note)
