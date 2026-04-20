import pytest

from eaia.gmail_utils import get_recipients, parse_time


def test_parse_time_parses_rfc2822ish_dates():
    dt = parse_time("Mon, 20 Apr 2026 10:15:00 -0400")
    assert dt.year == 2026
    assert dt.month == 4
    assert dt.day == 20


def test_parse_time_raises_on_invalid_value():
    with pytest.raises(ValueError):
        parse_time(None)  # type: ignore[arg-type]


def test_get_recipients_excludes_self_and_includes_sender():
    headers = [
        {"name": "To", "value": "a@example.com, me@example.com"},
        {"name": "Cc", "value": "c@example.com"},
        {"name": "From", "value": "Sender <sender@example.com>"},
    ]
    recipients = set(get_recipients(headers, email_address="me@example.com"))
    assert "a@example.com" in recipients
    assert "c@example.com" in recipients
    assert "Sender <sender@example.com>" in recipients
    # Self should be removed.
    assert all("me@example.com" not in r for r in recipients)
