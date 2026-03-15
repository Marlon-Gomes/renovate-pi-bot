# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com),
and this project adheres to [Semantic Versioning](https://semver.org).

## - 2026-03-15

### Added

- Initial automated Renovate bot setup for Raspberry Pi 4.
- Docker Compose configuration with pinned Renovate version.
- Modular `config.js` using environment variables for privacy.
- Dedicated `run-renovate.sh` script for cron automation.
- Pre-commit hooks for `shellcheck`, `markdownlint-cli2`, and basic hygiene.
- `LICENSE` (MIT) and `README.md` with setup instructions.
- `.dockerignore` safety mechanism to prevent credential leaks.
