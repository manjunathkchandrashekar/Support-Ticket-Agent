from src.safety.policy_checker import contains_abusive_content
from src.utils.constants import Action


class PolicyAgent:
    def decide(self, ticket, evidence):
        text = f"{ticket.subject} {ticket.message}".lower()
        if contains_abusive_content(text):
            return Action.REFUSE, 0.99, "The request contains abusive or threatening language."
        if any(term in text for term in ("fraud", "hacked", "legal", "chargeback", "security breach", "data loss")):
            return Action.ESCALATE, 0.95, "This issue requires specialist or human review."
        if not evidence:
            return Action.MORE_INFORMATION, 0.58, "No relevant policy or FAQ was found."
        if len(ticket.message.split()) < 5:
            return Action.MORE_INFORMATION, 0.64, "The ticket does not contain enough detail to resolve it."
        return Action.AUTO_RESOLVE, min(0.86, 0.70 + evidence[0][1] * 0.25), "The request matches a supported policy or FAQ."
