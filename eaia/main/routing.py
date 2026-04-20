from __future__ import annotations

from typing import Literal


def route_after_triage(state: dict) -> Literal["draft_response", "mark_as_read_node", "notify"]:
    if state["triage"].response == "email":
        return "draft_response"
    elif state["triage"].response == "no":
        return "mark_as_read_node"
    elif state["triage"].response == "notify":
        return "notify"
    elif state["triage"].response == "question":
        return "draft_response"
    else:
        raise ValueError(f"Unexpected triage response: {state['triage'].response!r}")


def take_action(
    state: dict,
) -> Literal[
    "send_message",
    "rewrite",
    "mark_as_read_node",
    "find_meeting_time",
    "send_cal_invite",
    "bad_tool_name",
]:
    prediction = state["messages"][-1]
    if len(prediction.tool_calls) != 1:
        raise ValueError("Expected exactly one tool call")
    tool_call = prediction.tool_calls[0]
    if tool_call["name"] == "Question":
        return "send_message"
    elif tool_call["name"] == "ResponseEmailDraft":
        return "rewrite"
    elif tool_call["name"] == "Ignore":
        return "mark_as_read_node"
    elif tool_call["name"] == "MeetingAssistant":
        return "find_meeting_time"
    elif tool_call["name"] == "SendCalendarInvite":
        return "send_cal_invite"
    else:
        return "bad_tool_name"


def bad_tool_name(state: dict):
    # Import lazily so unit tests can run without needing the full runtime stack.
    try:
        from langchain_core.messages import ToolMessage  # type: ignore
    except Exception:  # pragma: no cover
        class ToolMessage:  # minimal fallback for unit tests
            def __init__(self, content: str, tool_call_id: str):
                self.content = content
                self.tool_call_id = tool_call_id

    tool_call = state["messages"][-1].tool_calls[0]
    message = (
        f"Could not find tool with name `{tool_call['name']}`. "
        "Make sure you are calling one of the allowed tools!"
    )
    last_message = state["messages"][-1]
    last_message.tool_calls[0]["name"] = last_message.tool_calls[0]["name"].replace(":", "")
    return {
        "messages": [
            last_message,
            ToolMessage(content=message, tool_call_id=tool_call["id"]),
        ]
    }
