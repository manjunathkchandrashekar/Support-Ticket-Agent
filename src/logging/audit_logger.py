from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from src.utils.helpers import load_json, write_json


class AuditLogger:
    def __init__(self, path="outputs/audit_logs/decisions.json"):
        self.path = Path(path)
        self.records = self._load_records()

    def _load_records(self):
        if not self.path.exists():
            return []
        records = load_json(self.path)
        if not isinstance(records, list):
            raise ValueError("audit log must contain a JSON list")
        return records

    @staticmethod
    def _event_fields(event_type, ticket_id=None, metadata=None):
        if not isinstance(event_type, str) or not event_type.strip():
            raise ValueError("event_type is required")
        if metadata is not None and not isinstance(metadata, dict):
            raise TypeError("metadata must be a dictionary")
        return {
            "event_id": uuid4().hex,
            "event_type": event_type.strip(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ticket_id": ticket_id,
            "metadata": metadata or {},
        }

    def log(self, decision, event_type="decision_created", metadata=None):
        if not is_dataclass(decision):
            raise TypeError("decision must be a dataclass instance")
        record = asdict(decision)
        record.update(self._event_fields(event_type, decision.ticket_id, metadata))
        self.records.append(record)
        write_json(self.path, self.records)
        return record

    def log_event(self, event_type, ticket_id=None, metadata=None):
        record = self._event_fields(event_type, ticket_id, metadata)
        self.records.append(record)
        write_json(self.path, self.records)
        return record

    def for_ticket(self, ticket_id):
        return [record for record in self.records if record.get("ticket_id") == ticket_id]

    def clear(self):
        self.records.clear()
        write_json(self.path, self.records)
