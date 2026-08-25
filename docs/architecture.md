# Architecture

`main.py` loads the knowledge base and queue, then invokes `SupportGraph` for each ticket.

1. `RAGAgent` retrieves relevant FAQ/policy chunks with `LexicalVectorStore`.
2. `PolicyAgent` applies safety, escalation, evidence, and completeness rules.
3. `TriageAgent` enforces the confidence threshold.
4. `ResponseAgent` drafts a grounded response.
5. `AuditLogger` and `ApprovalQueue` provide observability and human-in-the-loop extension points.

Safety and escalation rules take precedence over auto-resolution.
