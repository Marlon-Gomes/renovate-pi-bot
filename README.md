# Renovate Pi Bot

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A self-hosted, containerized Renovate instance. This bot automates dependency
updates for all GitHub repositories (public and private) associated with a
dedicated bot account.

## Features

- **Privacy-First**: Personal info (email, username, tokens) is stored in a
local `.env`.
- **Portable**: Uses environment variables for UIDs/GIDs to work across
different Linux hosts.
- **Efficient**: Persists repository data and cache in `./data` to reduce SD
card wear and network usage.
- **Safe**: Includes `.dockerignore` to prevent accidental credential leakage.

## Directory Structure

The main files and folders of this project are listed below.

- `config.js`: Global logic (modularized via environment variables).
- `docker-compose.yml`: Container definition.
- `.env`: Contains your secrets and personal settings (untracked).
- `data/`: Local cache and git clones (untracked).
- `run-renovate.sh`: Automation script for cron

## Setup

1. **Bot account (optional):**
    Create a dedicated GitHub account for your bot. Generate a Personal Access
    token (PAT) with `repo` and `workflow` scope. Add the bot as a collaborator
    (with write access) to the repositories you want to manage.

2. **Initialize:**

    ```bash
    git clone <your-repo-url> /opt/renovate
    cd /opt/renovate

    # Create a data directory and set ownership to current user/group
    mkdir -p data
    sudo chown -R $(id -u):$(id -g) data

    # Prepare environment and script
    cp sample.env .env
    chmod +x run-renovate.sh
    ```

3. **Configure environment:**
    Edit the newly created `.env` file with the PAT, git author, and
    autodiscover filter. Note that if you created a dedicated bot account,
    the token and author refer to the bot, while the filter uses your own
    username.

    You can obtain your timezone's IANA code with:

    ```bash
    timedatectl
    ```

    You can get user id and group id information with:

    ```bash
    id -u
    id -g
    ```

## Usage

- Manual run (all repos matching filter):
    `./run-renovate.sh`
- Manual run (single repo):
    `docker compose run --rm -e RENOVATE_AUTODISCOVER_FILTER="your-username/specific-repo" renovate`
- Dry run (no changes to GitHub):
    `docker compose run --rm -e RENOVATE_DRY_RUN=full renovate`
- Debug mode:
    `docker compose run --rm -e RENOVATE_LOG_LEVEL=debug renovate`

## Automation (Cron)

To automate the bot, add the script to your crontab by running `crontab -e`.
The general format is:
`MINUTE HOUR * * * /opt/renovate/run-renovate.sh`

### Examples

- **Nightly at 3:00 AM:**
    `0 3 * * * /opt/renovate/run-renovate.sh`
- **Weekly on sundays at 11:00 PM:**
    `0 23 * * 0 /opt/renovate/run-renovate.sh`
- **Twice daily (6 AM and 6 PM):**
    `0 6,18 * * * /opt/renovate/run-renovate.sh`

> **Note:** Ensure you use the full absolute path to the script so cron can
locate it regardless of the execution environment.

## Contributing

To maintain code hygiene, this repository uses the
[pre-commit](https://pre-commit.com) framework.

### Set up Pre-commit

1. **Install pre-commit:**

    ```bash
    pip install pre-commit
    ```

2. **Install the git hooks:**

    ```bash
    pre-commit install
    ```

Now, every time you run `git commit`, these hooks will automatically run to:

- Fix trailing whitespace and end-of-file issues
- Validate YAML and JSON syntax
- Lint markdown files using **markdownlint-cli2**
- Lint shell scripts using **ShellCheck**
- Check if you accidentally commited secrets with **Gitleaks**

Note that markdownlint-cli2 does not offer fixes for all issues. You may need
to make changes manually for some checks.

## License

This project is licensed under the **MIT License**.
