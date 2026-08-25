import logging
import traceback
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from src.utils.helpers import load_json, write_json

logger = logging.getLogger("support_ticket_agent")


class TraceLogger:
	"""Capture diagnostic error events without hiding the original exception."""

	def __init__(self, path=None, log=logger):
		self.path = Path(path) if path else None
		self.logger = log
		self.records = self._load_records()

	def _load_records(self):
		if self.path is None or not self.path.exists():
			return []
		records = load_json(self.path)
		if not isinstance(records, list):
			raise ValueError("trace log must contain a JSON list")
		return records

	def log_error(self, error, *, stage=None, ticket_id=None, trace_id=None, context=None):
		if not isinstance(error, BaseException):
			raise TypeError("error must be an exception")
		if context is not None and not isinstance(context, dict):
			raise TypeError("context must be a dictionary")

		record = {
			"event_id": uuid4().hex,
			"trace_id": trace_id or uuid4().hex,
			"timestamp": datetime.now(timezone.utc).isoformat(),
			"event_type": "error",
			"ticket_id": ticket_id,
			"stage": stage,
			"error_type": type(error).__name__,
			"message": str(error),
			"traceback": "".join(traceback.TracebackException.from_exception(error).format()),
			"context": context or {},
		}
		self.records.append(record)
		if self.path:
			write_json(self.path, self.records)
		self.logger.error(
			"Support ticket processing failed: %s",
			record["message"],
			extra={"trace_id": record["trace_id"], "stage": stage, "ticket_id": ticket_id},
		)
		return record

	@contextmanager
	def capture(self, *, stage=None, ticket_id=None, trace_id=None, context=None):
		try:
			yield trace_id or uuid4().hex
		except Exception as error:
			self.log_error(
				error,
				stage=stage,
				ticket_id=ticket_id,
				trace_id=trace_id,
				context=context,
			)
			raise

	def for_ticket(self, ticket_id):
		return [record for record in self.records if record.get("ticket_id") == ticket_id]

	def clear(self):
		self.records.clear()
		if self.path:
			write_json(self.path, self.records)
