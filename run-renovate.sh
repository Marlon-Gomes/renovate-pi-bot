#!/bin/bash
# Move to the renovate directory
cd /opt/renovate || exit 1

# Detect current User and Group IDs
RENOVATE_UID=$(id -u)
export RENOVATE_UID

RENOVATE_GID=$(id -g)
export RENOVATE_GID

# Run Renovate and log the output
/usr/bin/docker compose run --rm renovate > /opt/renovate/renovate.log 2>&1
