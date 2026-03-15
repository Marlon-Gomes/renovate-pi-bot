# Security Policy

## Supported Versions

Only the latest stable version of this project is currently supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a potential security vulnerability (e.g., leaked tokens, credential exposure, or logic flaws), please report it responsibly by:

1. **Emailing:** [72144990+Marlon-Gomes@users.noreply.github.com](mailto:72144990+Marlon-Gomes@users.noreply.github.com)
2. **Details to include:**
   - A brief description of the vulnerability.
   - Steps to reproduce the issue.
   - Potential impact if exploited.

I will acknowledge your report within 48 hours and provide a timeline for a fix.

## Security Practices in this Repo

To keep this self-hosted instance secure, this project implements:

- **Environment Isolation:** All sensitive tokens are stored in an untracked `.env` file.
- **Dedicated Bot Account:** The bot operates under its own GitHub identity with limited permissions.
- **Pre-commit Hooks:** Automated checks to detect private keys and secrets before they are committed.
- **Minimal Docker Footprint:** Runs with a non-root user (UID 1000) and uses a `.dockerignore` safety net.

## Preferred Disclosure

This project follows a coordinated disclosure model. I ask that you do not share details of the vulnerability publicly until a fix has been pushed.
