import pytest
from unittest.mock import MagicMock, patch
from parser import check_site, load_html


# использование fixture
# создание поддельного объекта
@pytest.fixture
def mock_response():
    return MagicMock()

# помена через @patch
@patch("parser.requests.head")
def test_check_site_ok(mock_head, mock_response):
    mock_response.status_code = 200  # успешно
    mock_head.return_value = mock_response

    assert check_site("https://example.com") is True

@patch("parser.requests.head")
def test_check_site_server_error(mock_head, mock_response):
    mock_response.status_code = 503  # ошибка сервера
    mock_head.return_value = mock_response

    assert check_site("https://example.com") is False

# исключение
@patch("parser.requests.head")
def test_check_site_exception(mock_head):
    mock_head.side_effect = Exception("ошибка сети")

    assert check_site("https://example.com") is False

@patch("parser.requests.get")
def test_load_html_ok(mock_get, mock_response):
    mock_response.text = "<html>ok</html>"
    mock_get.return_value = mock_response

    assert load_html("https://example.com") == "<html>ok</html>"

# side_effect выбросит исключение
@patch("parser.requests.get")
def test_load_html_exception(mock_get):
    mock_get.side_effect = Exception("ошибка сети")

    assert load_html("https://example.com") is None
