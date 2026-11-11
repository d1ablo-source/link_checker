import pytest
from main import format_cell, get_urls_from_file

@pytest.mark.parametrize("value, width, is_error, expected",
                         [
                            (None, 10, True, "ОК"),
                            (None, 10, False, "-"),
                            (10, 10, False, "10"),
                            (1.5, 10, False, "1.5s"),
                            ("10", 10, False, "10"),
                            (20000000000, 10, False, "2000000..."),
                            ("nag", 10, False, "nag"),

                         ]
                         )
def test_format_cell(value, width, is_error, expected):
    assert format_cell(value=value, width=width, is_error=is_error) == expected


def test_get_urls_from_file(path):
    