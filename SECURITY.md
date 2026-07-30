# Security Policy

## Reporting a vulnerability

Please do not open a public issue for a suspected vulnerability. Use [GitHub private vulnerability reporting](https://github.com/ctcac00/media_company_demo/security/advisories/new) and include:

- a clear description of the issue and its potential impact;
- steps to reproduce it safely;
- affected files, services, or versions; and
- any suggested mitigation.

We will acknowledge reports and coordinate remediation through the private advisory.

## Handling secrets and sensitive data

Never commit credentials, access tokens, private keys, connection strings, or sensitive warehouse extracts. Store deployment secrets in the configured secret manager or environment variables.
