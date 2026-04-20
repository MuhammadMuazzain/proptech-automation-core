from types import SimpleNamespace

import pytest

from eaia.main.routing import route_after_triage, take_action, bad_tool_name


def test_route_after_triage_email_routes_to_draft_response():
    state = {"triage": SimpleNamespace(response="email")}
    assert route_after_triage(state) == "draft_response"


def test_route_after_triage_no_routes_to_mark_as_read():
    state = {"triage": SimpleNamespace(response="no")}
    assert route_after_triage(state) == "mark_as_read_node"


def test_route_after_triage_notify_routes_to_notify():
    state = {"triage": SimpleNamespace(response="notify")}
    assert route_after_triage(state) == "notify"


def test_take_action_routes_based_on_tool_name():
    def mk_state(tool_name: str):
        msg = SimpleNamespace(tool_calls=[{"name": tool_name, "args": {}, "id": "1"}])
        return {"messages": [msg]}

    assert take_action(mk_state("Question")) == "send_message"
    assert take_action(mk_state("ResponseEmailDraft")) == "rewrite"
    assert take_action(mk_state("Ignore")) == "mark_as_read_node"
    assert take_action(mk_state("MeetingAssistant")) == "find_meeting_time"
    assert take_action(mk_state("SendCalendarInvite")) == "send_cal_invite"
    assert take_action(mk_state("SomethingElse")) == "bad_tool_name"


def test_bad_tool_name_strips_colons_and_returns_tool_message():
    # Minimal message shape: needs `tool_calls` and `id` accessed in `bad_tool_name`.
    last = SimpleNamespace(
        id="msg1",
        tool_calls=[{"id": "tc1", "name": "ResponseEmailDraft:", "args": {}}],
    )
    state = {"messages": [last]}
    out = bad_tool_name(state)

    assert "messages" in out
    assert out["messages"][0].tool_calls[0]["name"] == "ResponseEmailDraft"
    # Second message should be a ToolMessage with an error string.
    assert "Could not find tool with name" in out["messages"][1].content


def test_take_action_requires_single_tool_call():
    msg = SimpleNamespace(tool_calls=[{"name": "Question", "args": {}, "id": "1"}, {"name": "Question", "args": {}, "id": "2"}])
    with pytest.raises(ValueError):
        take_action({"messages": [msg]})
