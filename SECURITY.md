## Security & data handling

This project is intended for operational automations. Treat all mailbox content and related metadata as sensitive.

### Secrets and credentials

- **Never commit** real credentials, OAuth tokens, client secrets, or private exports.
- Store secrets only in environment variables or a secure secret manager.
- Prefer **revocable** credentials and least-privilege scopes.
- Rotate keys immediately if you suspect leakage.

### Contractor-safe development workflow

If you are working with contractors (or running a paid trial):

- **Use sanitized data** first. Do not provide raw mailboxes, full exports, or production logs.
- Provide a limited, scoped dataset:
  - redacted sender/recipient emails
  - redacted names/addresses/phone numbers
  - remove attachments, links, and signatures
  - keep only the minimum text needed to reproduce behavior
- Do not share:
  - OAuth client secrets (`secrets.json`)
  - OAuth tokens
  - personal Google accounts or shared logins
  - production deployment URLs or dashboards unless access-controlled

### Logging and PII

- Logs should avoid storing full email bodies or headers by default.
- When debugging, prefer:
  - message IDs / thread IDs
  - timestamps
  - redacted subject lines
- If you must log content temporarily, ensure it is **disabled by default** and never enabled in production.

### Threat model (practical)

- Email content can contain: PII, financial details, contracts, credentials, or phishing attempts.
- Treat inbound email as untrusted input:
  - avoid executing links/attachments
  - validate tool arguments
  - keep strict boundaries around “send” actions

### Production deployment

- Production deployments should be owned and operated by the account holder.
- Keep access incremental: read-only first, then limited write access, then production deploy rights (if ever).
