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


def test_get_and_sort_urls_from_file(tmp_path):
    file = tmp_path / "URLS.txt"

    file.write_text(
                    "https://www.python.org\n"
                    "http://github.com\n"
                    "https://httpbin.org/status/404\n"
                    "   \n"
                    "example.com\n"
                    "#https://expired.badssl.com\n"
                    "https://httpbin.org/delay/3\n"
                    '"https://www.wikipedia.org"\n'
                    "https://httpbin.org/delay/3\n", 
                    encoding="utf-8")

    result = get_urls_from_file(file)
    assert result == ['https://www.python.org', 'http://github.com', 'https://httpbin.org/status/404', 'https://httpbin.org/delay/3', 'https://www.wikipedia.org']


def test_no_file(tmp_path):
    file = tmp_path / "urasdasd"
    with pytest.raises(FileNotFoundError):
        result = get_urls_from_file(file)
