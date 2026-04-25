from unittest.mock import patch, MagicMock
from parser import check_site, load_html


def test_check_site_ok():
    # фейковый ответ
    mock_response = MagicMock()
    mock_response.status_code = 200

    # patch подменяет requests.head внутри parser.py
    with patch("parser.requests.head", return_value=mock_response):
        assert check_site("https://example.com") is True

def test_check_site_server_error():
    mock_response = MagicMock()
    mock_response.status_code = 503

    with patch("parser.requests.head", return_value=mock_response):
        assert check_site("https://example.com") is False

def test_check_site_exception():
    # side_effect выбросит исключение
    with patch("parser.requests.head", side_effect=Exception("ошибка сети")):
        assert check_site("https://example.com") is False

def test_load_html_ok():
    mock_response = MagicMock()
    mock_response.text = "<html>ok</html>"

    with patch("parser.requests.get", return_value=mock_response):
        assert load_html("https://example.com") == "<html>ok</html>"

def test_load_html_exception():
    # имитация ошибки сети
    with patch("parser.requests.get", side_effect=Exception("ошибка сети")):
        assert load_html("https://example.com") is None
