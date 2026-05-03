#!/usr/bin/env python3
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime

LAST_LINE = ""
IS_TTY = sys.stdout.isatty()

LEVELS = {
    60: {
        "text": "FATAL",
        "color": "red",
        "priority": 2,
        "logging_level": logging.CRITICAL,
    },
    50: {
        "text": "ERROR",
        "color": "red",
        "priority": 3,
        "logging_level": logging.ERROR,
    },
    40: {
        "text": "WARN",
        "color": "yellow",
        "priority": 4,
        "logging_level": logging.WARNING,
    },
    30: {
        "text": "INFO",
        "color": "green",
        "priority": 6,
        "logging_level": logging.INFO,
    },
    20: {
        "text": "DEBUG",
        "color": "cyan",
        "priority": 7,
        "logging_level": logging.DEBUG,
    },
    10: {
        "text": "TRACE",
        "color": "magenta",
        "priority": 8,
        "logging_level": logging.DEBUG - 5,
    },
}

ANSI = {
    "red": "\033[31m",
    "yellow": "\033[33m",
    "green": "\033[32m",
    "cyan": "\033[36m",
    "magenta": "\033[35m",
    "bright_black": "\033[90m",
    "reset": "\033[0m",
}


def level_info(level: int) -> dict[str, object]:
    info = LEVELS.get(level)
    if info is None:
        raise ValueError(f"Unknown log level: {level}")
    return info


def format_time(time_str: str | None) -> str:
    if not time_str:
        return ""

    try:
        dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
    except ValueError:
        return time_str

    if dt.tzinfo is None:
        return time_str

    return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S")


def colorize(text: str, color: str) -> str:
    return f"{ANSI[color]}{text}{ANSI['reset']}"


class TTYFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return record.getMessage()


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("logfilter")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    if IS_TTY:
        handler.setFormatter(TTYFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(handler)
    return logger


def emit(logger: logging.Logger, level: int, message: str) -> None:
    log_level = LEVELS[level]["logging_level"]
    logger.log(log_level, message)


def main() -> int:
    global LAST_LINE

    logger = setup_logging()

    for line in sys.stdin:
        line = line.rstrip("\n")

        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        msg = data.get("msg")
        if not msg:
            continue

        level = data.get("level", 30)
        repo = data.get("repository", "")
        json_time = data.get("time")

        try:
            info = level_info(level)
        except ValueError:
            continue

        level_text = info["text"]
        priority = info["priority"]

        time_str = f"{format_time(json_time)} " if IS_TTY and json_time else ""
        repo_str = f"[{repo}] " if repo else ""
        priority_str = "" if IS_TTY else f"<{priority}>"
        raw_line = f"{priority_str}{time_str}{level_text} {repo_str}{msg}"

        if raw_line == LAST_LINE:
            continue

        if IS_TTY:
            output = f"{colorize(time_str, 'bright_black') if time_str else ''}{colorize(level_text, info['color'])} {repo_str}{msg}"
        else:
            output = raw_line

        emit(logger, level, output)
        LAST_LINE = raw_line

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
