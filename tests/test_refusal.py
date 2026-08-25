import pytest

from src.agents.response_agent import ResponseAgent
from src.safety.refusal_templates import refusal_response
from src.utils.constants import Action
from src.utils.schemas import Ticket


def test_refusal_response_is_respectful():
    response = ResponseAgent().draft(Ticket('1', '1', 'x', 'y'), Action.REFUSE, [])
    assert 'cannot assist' in response


def test_refusal_templates_cover_known_reasons_and_default_unknowns():
    assert "abusive" in refusal_response()
    assert "safe" in refusal_response("unsafe")
    assert "support question" in refusal_response("unsupported")
    assert refusal_response("unknown") == refusal_response()


def test_refusal_reason_must_be_text():
    with pytest.raises(TypeError):
        refusal_response(None)
