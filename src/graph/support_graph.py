from src.graph.graph_state import GraphState
from src.graph.edges import route_from_decision
from src.graph.nodes import triage_node


class SupportGraph:
    def __init__(self, triage_agent, audit_logger=None):
        self.triage_agent = triage_agent
        self.audit_logger = audit_logger

    def invoke_state(self, ticket):
        state = GraphState(ticket=ticket)
        triage_node(state, self.triage_agent)
        state.route_decision = route_from_decision(state)
        if self.audit_logger:
            self.audit_logger.log(state.decision)
        return state

    def invoke(self, ticket):
        state = self.invoke_state(ticket)
        return state.decision
