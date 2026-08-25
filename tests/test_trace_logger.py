import logging

import pytest

from src.logging.trace_logger import TraceLogger


def test_log_error_records_context_and_traceback(tmp_path, caplog):
    trace = TraceLogger(tmp_path / "trace.json")
    error = ValueError("invalid customer input")

    with caplog.at_level(logging.ERROR, logger="support_ticket_agent"):
        record = trace.log_error(
            error,
            stage="validation",
            ticket_id="T-error",
            trace_id="trace-1",
            context={"field": "customer_id"},
        )

    assert record["error_type"] == "ValueError"
    assert record["message"] == "invalid customer input"
    assert "ValueError: invalid customer input" in record["traceback"]
    assert trace.for_ticket("T-error") == [record]
    assert "invalid customer input" in caplog.text


def test_capture_logs_chained_exception_and_reraises(tmp_path):
    trace = TraceLogger(tmp_path / "trace.json")

    with pytest.raises(RuntimeError, match="retrieval failed"):
        with trace.capture(stage="retrieval", ticket_id="T-chain", context={"query": "refund"}):
            try:
                raise TimeoutError("vector store timeout")
            except TimeoutError as error:
                raise RuntimeError("retrieval failed") from error

    record = trace.records[0]
    assert record["error_type"] == "RuntimeError"
    assert "vector store timeout" in record["traceback"]


def test_trace_logger_persists_across_instances_and_clears(tmp_path):
    path = tmp_path / "trace.json"
    TraceLogger(path).log_error(KeyError("missing"), ticket_id="T-1")
    trace = TraceLogger(path)

    assert len(trace.records) == 1
    trace.clear()
    assert TraceLogger(path).records == []


def test_invalid_error_and_context_are_rejected(tmp_path):
    trace = TraceLogger(tmp_path / "trace.json")

    with pytest.raises(TypeError):
        trace.log_error("not an exception")
    with pytest.raises(TypeError):
        trace.log_error(RuntimeError("failure"), context=["unsafe"])