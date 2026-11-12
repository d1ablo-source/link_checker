from config.command_line import parse_arguments
import pytest

def test_invalid_concurrency(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["link_checker", "https://google.com", "--concurrency", "0"]
    )

    with pytest.raises(SystemExit) as exc:
        parse_arguments()

    assert exc.value.code == 2

def test_invalid_timeout_func(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["link_checker", "https://google.com", "--timeout_func", "0"]
    )

    with pytest.raises(SystemExit):
        parse_arguments()


def test_invalid_timeout_response(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["link_checker", "https://google.com", "--timeout_response", "-1"]
    )

    with pytest.raises(SystemExit):
        parse_arguments()


def test_missing_url(monkeypatch):
    monkeypatch.setattr("sys.argv", ["link_checker"])

    with pytest.raises(SystemExit) as exc:
        parse_arguments()

    assert exc.value.code == 2
