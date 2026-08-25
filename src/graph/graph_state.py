from dataclasses import dataclass, field
from src.utils.schemas import Ticket, TicketDecision, Sentiment, RagAnswer, RouteDecision


@dataclass
class GraphState:
    ticket: Ticket
    evidence: list = field(default_factory=list)
    decision: TicketDecision | None = None
    sentiment: Sentiment | None = None
    rag_answer: RagAnswer | None = None
    route_decision: RouteDecision | None = None
