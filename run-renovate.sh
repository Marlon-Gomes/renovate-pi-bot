#!/bin/bash
# Move to the renovate directory
cd /opt/renovate || exit 1

# Detect current User and Group IDs
RENOVATE_UID=$(id -u)
export RENOVATE_UID

RENOVATE_GID=$(id -g)
export RENOVATE_GID

# Run Renovate and log the output
# stdbuf -oL ensures line-buffering for the docker command
stdbuf -oL /usr/bin/docker compose run --rm renovate |
    python3 "$(dirname "$0")/tools/renovate_log_formatter.py"
