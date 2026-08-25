from src.main import build_agent
from src.utils.helpers import load_json
from src.utils.schemas import Ticket
from src.graph.edges import is_terminal, requires_human_review, route_from_decision
from src.graph.graph_state import GraphState
from src.utils.constants import Action
from src.utils.schemas import TicketDecision


def test_all_routes(tmp_path):
    root = __import__('pathlib').Path(__file__).parents[1]
    agent = build_agent(root)
    tickets = [Ticket(**item) for item in load_json(root / 'data/tickets/sample_ticket_batch.json')]
    actions = [agent.process(ticket).action.value for ticket in tickets]
    assert actions == ['Auto-Resolve', 'Escalate', 'Ask for More Information', 'Refuse']


def make_state(action=None):
    ticket = Ticket("T-graph", "C-1", "Subject", "Message")
    decision = None
    if action is not None:
        decision = TicketDecision("T-graph", action, 0.8, "Draft", "Reason")
    return GraphState(ticket=ticket, decision=decision)


def test_route_without_decision_is_unknown_and_not_terminal():
    state = make_state()

    assert route_from_decision(state) == "unknown"
    assert not is_terminal(state)
    assert not requires_human_review(state)


def test_all_decision_routes_are_terminal():
    for action in Action:
        state = make_state(action)
        assert route_from_decision(state) == action.value
        assert is_terminal(state)


def test_escalation_and_refusal_require_human_review():
    assert requires_human_review(make_state(Action.ESCALATE))
    assert requires_human_review(make_state(Action.REFUSE))
    assert not requires_human_review(make_state(Action.AUTO_RESOLVE))
