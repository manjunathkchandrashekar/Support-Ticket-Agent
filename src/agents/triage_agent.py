from src.utils.schemas import TicketDecision


class TriageAgent:
    def __init__(self, rag_agent, policy_agent, sentiment_agent, response_agent, threshold=0.72):
        self.rag_agent = rag_agent
        self.policy_agent = policy_agent
        self.sentiment_agent = sentiment_agent
        self.response_agent = response_agent
        self.threshold = threshold

    def process(self, ticket) -> TicketDecision:
        evidence = self.rag_agent.retrieve(ticket)
        action, confidence, rationale = self.policy_agent.decide(ticket, evidence)
        if action.value == "Auto-Resolve" and confidence < self.threshold:
            action = type(action).MORE_INFORMATION
            rationale = "Resolution confidence is below the configured threshold."
        return TicketDecision(ticket.ticket_id, action, round(confidence, 2), self.response_agent.draft(ticket, action, evidence), rationale, [item[0].source for item in evidence], self.sentiment_agent.analyze(ticket.message))
