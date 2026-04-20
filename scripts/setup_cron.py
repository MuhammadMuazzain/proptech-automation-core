"""Set up a cron job that runs every 10 minutes to check for emails"""
import argparse
import asyncio
import logging
from typing import Optional
from langgraph_sdk import get_client
from eaia.logging_utils import configure_logging, log_kv

logger = logging.getLogger(__name__)


async def main(
    url: Optional[str] = None,
    minutes_since: int = 60,
):
    configure_logging()
    if url is None:
        client = get_client(url="http://127.0.0.1:2024")
    else:
        client = get_client(
            url=url
        )
    log_kv(logger, "Creating cron", schedule="*/10 * * * *", minutes_since=minutes_since, url=url or "http://127.0.0.1:2024")
    await client.crons.create("cron", schedule="*/10 * * * *", input={"minutes_since": minutes_since})



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        type=str,
        default=None,
        help="URL to run against",
    )
    parser.add_argument(
        "--minutes-since",
        type=int,
        default=60,
        help="Only process emails that are less than this many minutes old.",
    )

    args = parser.parse_args()
    asyncio.run(
        main(
            url=args.url,
            minutes_since=args.minutes_since,
        )
    )