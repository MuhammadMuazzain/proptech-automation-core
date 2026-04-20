"""Script for testing a single run through an agent."""

import asyncio
import logging
from langgraph_sdk import get_client
import uuid
import hashlib

from eaia.schemas import EmailData
from eaia.logging_utils import configure_logging, log_kv

logger = logging.getLogger(__name__)


async def main():
    configure_logging()
    client = get_client(url="http://127.0.0.1:2024")

    email: EmailData = {
        "from_email": "Test",
        "to_email": "test@gmail.com",
        "subject": "Re: Hello!",
        "page_content": "Test",
        "id": "123",
        "thread_id": "123",
        "send_time": "2024-12-26T13:13:41-08:00",
    }
    log_kv(logger, "Creating test run", email_id=email["id"], thread_id=email["thread_id"])

    thread_id = str(
        uuid.UUID(hex=hashlib.md5(email["thread_id"].encode("UTF-8")).hexdigest())
    )
    try:
        await client.threads.delete(thread_id)
    except:
        pass
    await client.threads.create(thread_id=thread_id)
    await client.runs.create(
        thread_id,
        "main",
        input={"email": email},
        multitask_strategy="rollback",
    )


if __name__ == "__main__":
    asyncio.run(main())
