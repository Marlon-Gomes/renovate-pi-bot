import io
import json
import pytest


def test_level_info_known(mod):
    info = mod.level_info(30)
    assert info["text"] == "INFO"
    assert info["priority"] == 6


def test_level_info_unknown(mod):
    with pytest.raises(ValueError, match="Unknown log level: 99"):
        mod.level_info(99)


def test_format_time_valid_utc(monkeypatch, mod):
    class FixedDT:
        def astimezone(self):
            return self

        def strftime(self, fmt):
            return "2024-02-21 13:37:08"

        @property
        def tzinfo(self):
            return object()

    class FakeDatetime:
        @staticmethod
        def fromisoformat(s):
            return FixedDT()

    monkeypatch.setattr(mod, "datetime", FakeDatetime)
    assert mod.format_time("2024-02-21T18:37:08.087Z") == "2024-02-21 13:37:08"


def test_format_time_invalid_returns_original(mod):
    assert mod.format_time("not-a-time") == "not-a-time"


def test_colorize_uses_expected_escape(mod):
    assert mod.colorize("x", "red") == "\033[31mx\033[0m"


def test_main_non_tty_dedup_and_priority(monkeypatch, mod):
    monkeypatch.setattr(mod.sys.stdout, "isatty", lambda: False)
    monkeypatch.setattr(mod, "IS_TTY", False)

    stdin = io.StringIO(
        json.dumps(
            {
                "msg": "hello",
                "level": 30,
                "repository": "renovate",
                "time": "2024-02-21T18:37:08Z",
            }
        )
        + "\n"
        + json.dumps(
            {
                "msg": "hello",
                "level": 30,
                "repository": "renovate",
                "time": "2024-02-21T18:37:08Z",
            }
        )
        + "\n"
    )
    monkeypatch.setattr(mod.sys, "stdin", stdin)

    messages = []

    class DummyLogger:
        def log(self, level, message):
            messages.append(message)

    monkeypatch.setattr(mod, "setup_logging", lambda: DummyLogger())

    rc = mod.main()
    assert rc == 0
    assert len(messages) == 1
    assert messages[0] == "<6>INFO [renovate] hello"


def test_main_tty_colors(monkeypatch, mod):
    monkeypatch.setattr(mod, "IS_TTY", True)
    monkeypatch.setattr(mod.sys.stdout, "isatty", lambda: True)
    monkeypatch.setattr(mod, "format_time", lambda s: "2024-02-21 13:37:08")

    stdin = io.StringIO(
        json.dumps(
            {
                "msg": "hello",
                "level": 40,
                "repository": "renovate",
                "time": "2024-02-21T18:37:08Z",
            }
        )
        + "\n"
    )
    monkeypatch.setattr(mod.sys, "stdin", stdin)

    messages = []

    class DummyLogger:
        def log(self, level, message):
            messages.append(message)

    monkeypatch.setattr(mod, "setup_logging", lambda: DummyLogger())

    mod.main()
    assert len(messages) == 1
    out = messages[0]
    assert "\033[90m2024-02-21 13:37:08 \033[0m" in out
    assert "\033[33mWARN\033[0m" in out
    assert "[renovate] hello" in out
