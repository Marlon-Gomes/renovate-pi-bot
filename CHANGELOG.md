# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com),
and this project adheres to [Semantic Versioning](https://semver.org).

## [Unreleased]

## [0.3.1] - 2026-03-30

### Added

- Documentation for migrating to Systemd `.service` and `.timer` units.
- Unbuffered Perl-based log filtering in `run-renovate.sh` for clean
`LVL [repo] msg` output.
- Conditional timestamping logic to prevent duplication in system journals.

### Changed

- Optimized `docker-compose.yml` with persistent volume caching.
- Refactored `run-renovate.sh` to support dual-stream logging (JSON to file,
plain-text to console).

## [0.3.0] - 2026-03-19

### Changed

- Suppress security labels in PRs and Dashboards to avoid disclosing security
vulnerabilities in client code.

## [0.2.0] - 2026-03-16

### Added

- Centralized status tracking and manual PR triggers via Dependency Dashboard.
- Automatic resolution of simple merge conflicts via
`rebaseWhen: 'conflicted'`.
- Dual-source security vulnerability scanning (GitHub/OSV) with rate-limit
bypass.
- Persistent tool cache via `containerbaseDir`.

### Fixed

- Migrated to the `full` Docker image to resolve slim image `arm64` lockfile
artifact upload failures.

### Changed

- Include version number in changelog anchors.

## [0.1.0] - 2026-03-15

### Added

- Initial automated Renovate bot setup for Raspberry Pi 4.
- Docker Compose configuration with pinned Renovate version.
- Modular `config.js` using environment variables for privacy.
- Dedicated `run-renovate.sh` script for cron automation.
- Pre-commit hooks for `shellcheck`, `markdownlint-cli2`, and basic hygiene.
- `LICENSE` (MIT) and `README.md` with setup instructions.
- `.dockerignore` safety mechanism to prevent credential leaks.

[0.3.1]: https://github.com/Marlon-Gomes/renovate-pi-bot/releases/tag/v0.3.1
[0.3.0]: https://github.com/Marlon-Gomes/renovate-pi-bot/releases/tag/v0.3.0
[0.2.0]: https://github.com/Marlon-Gomes/renovate-pi-bot/releases/tag/v0.2.0
[0.1.0]: https://github.com/Marlon-Gomes/renovate-pi-bot/releases/tag/v0.1.0
