from src.utils.constants import Action
from src.safety.refusal_templates import refusal_response


class ResponseAgent:
    def draft(self, ticket, action: Action, evidence) -> str:
        if action == Action.REFUSE:
            return refusal_response()
        if action == Action.ESCALATE:
            return "Thanks for reporting this. I have escalated your ticket to our specialist support team for review."
        if action == Action.MORE_INFORMATION:
            return "Please share the exact error message, the affected account or order, and the steps you already tried."
        source = evidence[0][0].source if evidence else "our support guidance"
        return f"Thanks for contacting us. Based on {source}, please follow the documented steps in the relevant policy or FAQ. If the issue continues, reply with the result and we will continue helping."
