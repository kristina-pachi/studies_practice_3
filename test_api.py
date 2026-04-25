import pytest
from unittest.mock import patch, MagicMock
from api import get_weather

# использование fixture
# чтобы не дублировать
@pytest.fixture
def mock_response():
    return MagicMock()

@pytest.fixture
def items():
    return 55.75, 37.61, "FAKE_KEY"

# тест на успешней ответ
@patch("api.requests.get")
def test_get_weather_success(mock_get, mock_response):
    # фейковый ответ API
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "Москва",
        "main": {"temp": 5.0, "humidity": 80},
        "weather": [{"description": "пасмурно"}],
        "wind": {"speed": 3.2}
    }

    # mock_get возвращать mock_response
    mock_get.return_value = mock_response

    result = get_weather(55.75, 37.61, "FAKE_KEY")

    assert result == {
        "Город": "Москва",
        "Температура": 5.0,
        "Описание погоды": "пасмурно",
        "Скорость ветра": 3.2,
        "Влажность": 80
    }

# тест с неверным json ответом
@patch("api.requests.get")
def test_get_weather_bad_json(mock_get, mock_response):
    mock_response.status_code = 200
    mock_response.json.return_value = {}

    mock_get.return_value = mock_response

    result = get_weather(*items)

    assert result is None

# ошибка сервера
@patch("api.requests.get")
def test_get_weather_api_error(mock_get, mock_response):
    mock_response.status_code = 404  # ошибка API
    mock_get.return_value = mock_response

    result = get_weather(*items)

    assert result is None

# ошибка сети
@patch("api.requests.get")
def test_get_weather_exception(mock_get):
    mock_get.side_effect = Exception("ошибка сети")

    result = get_weather(*items)

    assert result is None
