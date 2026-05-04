# Renovate Pi Bot

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Marlon-Gomes/renovate-pi-bot/main.svg)](https://results.pre-commit.ci/latest/github/Marlon-Gomes/renovate-pi-bot/main)
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

    Prefer the timezone name (e.g., `America/New_York`) rather than a code
    (e.g., `EDT`) or fixed offset (e.g., `-0400`) for automatic daylight savings
    management, if applicable in your location.

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

## Automation (Systemm & Cockpit)

To bot is automated via **Systemd Timers** for better reliability and
integrated logging via [Cockpit](https://cockpit-project.org).

### Setup Service & Timer

Create the following files in `/etc/systemd/system/`:

- `renovate.service`:

    ```ini
    [Unit]
        Description=Run Renovate Bot
        Wants=network-online.target
        After=network-online.target docker.service

    [Service]
        Type=oneshot
        User=<your-username>
        WorkingDirectory=/opt/renovate
        ExecStart=/bin/bash /opt/renovate/run-renovate.sh
        StandardOutput=journal
        StandardError=journal

    [Install]
        WantedBy=multi-user.target
    ```

- `renovate.timer`:

    ```ini
    [Timer]
        # See "Customizing the Schedule" below
        OnCalendar=*-*-* 00,12:00:00
        # Optional randomized delay up to 15 minutes
        RandomizedDelaySec=15m
        Persistent=true

    [Install]
        WantedBy=timers.target
    ```

### Customizing the Schedule

To change how often the bot runs, edit the `OnCalendar` line in `renovate.timer`:

- Twice daily (noon/midnight): `*-*-* 00,12:00:00`
- Daily at 3 AM: `*-*-* 03:00:00`
- Weekly on Mondays at 1 AM: `Mon *-*-* 01:00:00`
- Hourly: hourly

> Note: after changing the timer file, always run `sudo systemctl daemon-reload`
to apply changes

### Monitoring & Activation

Enable the timer to start automatically on boot:

```bash
sudo systemctl enable --now renovate.timer
```

- Live logs: Real-time, filtered logs (info level) are streamed to `journalctl`
    and can be visualized in the 'Services' tab in Cockpit.
- Debug logs: full JSON logs are stored at `/opt/renovate/logs/renovate.log`. To
    integrate these with system logs, while maintaining the application
    self-contained, use a symbolic link:

    ```bash
    sudo ln -sf /opt/renovate/logs /var/log/renovate
    ```

- Manual run: trigger an immedaite run with
    `sudo systemctl start renovate.service` or by starting the service directly
    from Cockpit.

### Log Rotation

Renovate appends to the log file indefinitely. To prevent `renovate.log` from
consuming excessive disk space, use the standard Linux `logrotate` utility.
Create a configuration file at `/etc/logrotate.d/renovate`:

```text
/opt/renovate/renovate.log {
    daily
    maxsize 50M
    rotate 14
    compress
    delaycompress
    missingok
    notifyempty
    copytruncate
    # Replace with your actual UID and GID (e.g. 1000 1000)
    create 0644 RENOVATE_UID RENOVATE_GID}
}
```

Ensure the RENOVATE_UID AND RENOVATE_GID match the settings on your `.env` file
so that the bot retains write permissions to the new file. You can test the
`logrotate` setup with

```bash
sudo logrotate -d /etc/logrotate.d/renovate
```

## Contributing

To maintain project quality and consistency, we use [pre-commit] for automation
and [uv] for reproducible Python environments.

### Pre-commit Hooks

We use the pre-commit framework to enforce code hygiene. Before your first
commit, please set this up:

1. **Install pre-commit:**

    ```bash
    pip install pre-commit # or use your preferred package manager
    ```

2. **Install the git hooks:**

    ```bash
    pre-commit install
    ```

**What the hooks do**: Every time you run `git commit`, these hooks
automatically run to:

- Fix trailing whitespace and end-of-file issues
- Validate YAML and JSON syntax
- Lint markdown files (**markdownlint-cli2**), shell scripts (**ShellCheck**),
and Python code (**Ruff**).
- Scan for commited secrets (**Gitleaks**)
- Format Python code (**Ruff**)
- Prevent accidental commits of debugging code (like `breakpoint()`)

> Note: Some markdown issues may require manual intervention as they cannot be
> auto-fixed.

### Tooling and local testing

This project offers a Python script `tools/renovate_log_formatter.py` to format
Renovate JSON logs in a human-readable format suitable for both TTY and non-TTY
environments. We use `uv` to manage a consistent Python environment for the
`tools/format-renovate-logs.py` script and its associated tests.

#### Setting up the environment

After cloning the repository, sync the environment to install all necessary
dependencies:

```bash
uv sync
```

#### Running the formatter and tests

Use `uv run` to execute tools within the managed virtual environment:

- **Run tests locally**

   ```bash
   uv run pytest
   ```

- **Run the log formatter** against local JSON log files:

    ```bash
    uv run python tools/format-renovate-logs.py < your-sample-logs.jsonl
    ```

## Known Issues and Limitations

### Security Vulnerability Disclosure in Public Repositories

By default, this bot is configured to provide detailed security insights. When a
vulnerability is detected, Renovate generates a Pull Request containing a
detailed table of CVE IDs, severity scores, and links to advisories.

#### The Risk

In public repositories, these PRs effectively broadcast known unpatched
vulnerabilities in your project to the public before the fix is even merged.

#### Recommended Mitigation Strategies

If you are running this bot on a public repository, you should choose one of the
following two patterns to protect your project.

##### Option A: Silent "Ghost" Patching (Recommended)

This approach scrubs the vulnerability table and merges the fix automatically.
This is the best balance between security and discretion. Add this to your
`renovate.json`:

```JSON
{
  "packageRules": [
    {
      "matchUpdateTypes": ["security"],
      "automerge": true,
      "automergeType": "pr",
      "requiredStatusChecks": []
    }
  ]
}
```

> Note: You may add required status checks to the empty array above, but be
> mindful that if these status checks fail, the PR will be blocked and the
> security vulnerabilities will be visible until the status checks pass.

#### Option B: Disable Security Scanning

If you prefer to handle security updates manually or through another tool
(like GitHub Native Dependabot or OSV-Scanner) to avoid any automated
disclosure, you can disable the feature entirely:

```JSON
{
  "vulnerabilityAlerts": {
    "enabled": false
  },
  "osvVulnerabilityAlerts": false
}
```

## License

This project is licensed under the **MIT License**.

[pre-commit]: https://pre-commit.com
[uv]: https://docs.astral.sh/uv/
