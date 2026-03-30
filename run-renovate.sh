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
# perl -nle | autoflush(1) ensures the pipe itself doesn't buffer
stdbuf -oL /usr/bin/docker compose run --rm renovate | perl -ne '
    BEGIN { $| = 1 }
    my ($time_raw) = /"time":"(.*?)"/;
    my ($lvl_num) = /"level":(\d+)/;
    my ($repo) = /"repository":"(.*?)"/;
    my ($msg) = /"msg":"(.*?)"/;

    next unless $msg;

    # Map numeric level to text
    my $lvl = ($lvl_num == 50) ? "ERROR" : ($lvl_num == 40) ? "WARN" : "INFO";

    # Only show HH:MM:SS if running in a real terminal (not Systemd)
    my $time = "";
    if (-t STDOUT) {
        $time_raw =~ s/[TZ]/ /g;
        $time = substr($time_raw, 11, 8) . " ";
    }

    # Construct clean output line
    my $current_line = "$time$lvl " . ($repo ? "[$repo] " : "") . $msg;

    # De-duplicate identical consecutive lines for cleaner UI
    if ($current_line ne $last_line) {
        print "$current_line\n";
        $last_line = $current_line;
    }
'
