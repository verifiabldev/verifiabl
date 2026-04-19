# Security Policy

## Reporting a Vulnerability

Please do not open public GitHub issues for suspected security problems.

Report vulnerabilities privately to `security@verifiabl.dev` with:

- a short description of the issue
- steps to reproduce it
- the affected route, file, or integration if known
- any proof-of-concept details needed to verify the report

We will acknowledge valid reports as quickly as we can and coordinate remediation before any public disclosure.

## Scope

This project includes:

- the public site and dashboard
- authentication and API routing in `main.py`
- tier and credential handling in `auth.py`
- storage behavior in `store.py`
- individual mock integrations in `mocks/`

## Secrets

Do not include live secrets, API keys, webhook URLs, or production tokens in reports or pull requests.
