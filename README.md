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
