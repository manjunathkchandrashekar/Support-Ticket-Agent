from dataclasses import dataclass, field
from .constants import Action


@dataclass
class Ticket:
    ticket_id: str
    customer_id: str
    subject: str
    message: str
    priority: str = "normal"
    metadata: dict = field(default_factory=dict)


@dataclass
class TicketDecision:
    ticket_id: str
    action: Action
    confidence: float
    response: str
    rationale: str
    sources: list[str] = field(default_factory=list)
    sentiment: str = "neutral"
    review_status: str = "pending"
    reviewer: str | None = None
    review_note: str | None = None
    reviewed_at: str | None = None
    original_action: Action | None = None


@dataclass
class RagAnswer:
    answer: str
    sources: list[str] = field(default_factory=list)


@dataclass
class RouteDecision:
    action: Action
    requires_human_review: bool = False


Sentiment = str
