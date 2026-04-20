import base64
import email.utils
from datetime import datetime
from typing import Any


def extract_message_part(msg: dict[str, Any]) -> str:
    """Recursively walk through the email parts to find a message body."""
    if msg.get("mimeType") == "text/plain":
        body_data = msg.get("body", {}).get("data")
        if body_data:
            return base64.urlsafe_b64decode(body_data).decode("utf-8")
    elif msg.get("mimeType") == "text/html":
        body_data = msg.get("body", {}).get("data")
        if body_data:
            return base64.urlsafe_b64decode(body_data).decode("utf-8")
    if "parts" in msg:
        for part in msg["parts"]:
            body = extract_message_part(part)
            if body:
                return body
    return "No message body available."


def parse_time(send_time: str):
    try:
        # Prefer stdlib parsing for RFC 2822 style dates.
        dt = email.utils.parsedate_to_datetime(send_time)
        if dt is not None:
            return dt
        # Fallback: ISO-8601-like strings.
        return datetime.fromisoformat(send_time)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Error parsing time: {send_time} - {e}")


def get_recipients(headers, email_address: str, addn_receipients=None):
    recipients = set(addn_receipients or [])
    sender = None
    for header in headers:
        if header["name"].lower() in ["to", "cc"]:
            recipients.update(header["value"].replace(" ", "").split(","))
        if header["name"].lower() == "from":
            sender = header["value"]
    if sender:
        recipients.add(sender)
    for r in list(recipients):
        if email_address in r:
            recipients.remove(r)
    return list(recipients)
