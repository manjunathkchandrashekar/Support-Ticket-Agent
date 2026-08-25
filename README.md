# Support-Ticket-Agent

A self-contained Python AI-powered support ticket triage and resolution agent. It processes a synthetic queue, retrieves relevant policy/FAQ evidence, checks safety, analyzes sentiment, and selects exactly one action:

- Auto-Resolve
- Escalate
- Refuse
- Ask for More Information

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH = "."
python -m src.main
pytest -q
```

The default engine is local and deterministic: lexical retrieval plus policy rules. `config/model_config.yaml` is the extension point for a hosted model or embedding provider. Decisions include confidence, rationale, sentiment, and retrieved source filenames. Audit records are written under `outputs/audit_logs` when an `AuditLogger` is attached.

See `docs/architecture.md` for the flow and `docs/demo_script.md` for a short walkthrough.
