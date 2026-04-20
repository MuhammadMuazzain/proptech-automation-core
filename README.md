# Executive AI Assistant

Executive AI Assistant (EAIA) is an **agentic AI automation** for email operations:

- **Ingest** recent emails from Gmail
- **Triage**: ignore vs notify vs draft a reply
- **Draft responses** with tool use (ask a question, schedule a meeting, send an invite)
- **Human-in-the-loop** approval/editing before sending
- **Run continuously** via a scheduled ingest job (cron)

This repo is intended to be worked on like a real production automation system: **tests, logging, error handling, and careful data/security practices**.

## What this is (and isn’t)

- **Not a generic chatbot**: it’s a workflow-driven automation with explicit routing and tool execution.
- **Safe-by-default**: designed to run against **sanitized data** first and avoid exposing credentials.
- **Built for iterative improvement**: supports learning/preferences via the LangGraph store.

## Table of contents

- [Quick start](#quick-start)
- [Configuration](#configuration)
- [Running locally](#running-locally)
- [Ingesting emails](#ingesting-emails)
- [Testing](#testing)
- [Security & data handling](#security--data-handling)
  - [Contractor-safe workflow](#contractor-safe-workflow)

## Quick start

### Environment

1. Create and activate a virtualenv.
2. Install dependencies:

```shell
pip install -e .
```

### Credentials

Set these environment variables (see `.env.example`):

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY` (optional, used by some reflection paths)
- `LANGSMITH_API_KEY` (required for the OAuth helper client)

Then set up Google OAuth:

   1. [Enable the API](https://developers.google.com/gmail/api/quickstart/python#enable_the_api)
      - Enable Gmail API if not already by clicking the blue button `Enable the API`
   2. [Authorize credentials for a desktop application](https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application)
  
> Note: If you're using a personal email (non-Google Workspace), select "External" as the User Type in the OAuth consent screen. With "External" selected, you must add your email as a test user in the Google Cloud Console under "OAuth consent screen" > "Test users" to avoid the "App has not completed verification" error. The "Internal" option only works for Google Workspace accounts.

Download the client secret and run:

```shell
mkdir eaia/.secrets
mv ${PATH-TO-CLIENT-SECRET.JSON} eaia/.secrets/secrets.json
python scripts/setup_gmail.py
```

**Authentication Flow**: EAIA uses LangChain Auth for OAuth management. The setup script creates a Google OAuth provider that handles token storage and refresh automatically. When you first run the application, you'll be prompted to complete OAuth authentication if needed.

## Configuration

The default configuration lives at `eaia/main/config.yaml`.

This file is intentionally **generic** by default. Customize it for your environment before running against real mailboxes.

Core config keys:

- `email`: Email to monitor and send emails as. This should match the credentials you loaded above.
- `full_name`: Full name of user
- `name`: First name of user
- `background`: Basic info on who the user is
- `timezone`: Default timezone where the user is
- `schedule_preferences`: Any preferences for how calendar meetings are scheduled. E.g. length, name of meetings, etc
- `background_preferences`: Any background information that may be needed when responding to emails. E.g. coworkers to loop in, etc.
- `response_preferences`: Any preferences for what information to include in emails. E.g. whether to send calendly links, etc.
- `rewrite_preferences`: Any preferences for the tone of your emails
- `triage_no`: Guidelines for when emails should be ignored
- `triage_notify`: Guidelines for when user should be notified of emails (but EAIA should not attempt to draft a response)
- `triage_email`: Guidelines for when EAIA should try to draft a response to an email

## Running locally

Run the local LangGraph dev server:

```shell
langgraph dev
```

## Ingesting emails

Let's now kick off an ingest job to ingest some emails and run them through our local EAIA.

Leave the `langgraph dev` command running, and open a new terminal. From there, get back into this directory and virtual environment. To kick off an ingest job, run:

```shell
python scripts/run_ingest.py --minutes-since 120 --rerun 1 --early 0
```

This will ingest all emails in the last 120 minutes (`--minutes-since`). It will NOT break early if it sees an email it already saw (`--early 0`) and it will
rerun ones it has seen before (`--rerun 1`). It will run against the local instance we have running.

## Human-in-the-loop review

EAIA is designed to support human review/approval before actions (sending email / sending invites). The “human inbox” integration is handled via LangGraph interrupts.

## Testing

Run the unit tests:

```shell
pytest -q
```

## Security & data handling

See `SECURITY.md` for guidance on:

- handling sensitive operational data
- sanitized/safe exports for contractor work
- credential management and what should never be shared

### Contractor-safe workflow

- Start with **sanitized data** (exported emails with redaction) and a limited-scope task.
- No shared personal logins; production credentials stay with the owner.
- Prefer least-privilege API keys and revocable accounts as access expands.

## Advanced Options

If you want to control more of EAIA besides what the configuration allows, you can modify parts of the code base.

**Reflection Logic**
To control the prompts used for reflection (e.g. to populate memory) you can edit `eaia/reflection_graphs.py`

**Triage Logic**
To control the logic used for triaging emails you can edit `eaia/main/triage.py`

**Calendar Logic**
To control the logic used for looking at available times on the calendar you can edit `eaia/main/find_meeting_time.py`

**Tone & Style Logic**
To control the logic used for the tone and style of emails you can edit `eaia/main/rewrite.py`

**Email Draft Logic**
To control the logic used for drafting emails you can edit `eaia/main/draft_response.py`


