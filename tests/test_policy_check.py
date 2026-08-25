from src.safety.policy_checker import contains_abusive_content


def test_abusive_content_is_detected():
    assert contains_abusive_content('This is an abusive threat')
    assert not contains_abusive_content('Please help with my refund')
