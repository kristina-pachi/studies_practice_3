import pytest
from unittest.mock import patch, MagicMock
from api import get_weather, fetch_weather, parse_weather

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
def test_fetch_weather_success(mock_get, mock_response, items):
    mock_response.status_code = 200
    mock_response.json.return_value = {"ok": True}

    mock_get.return_value = mock_response

    lat, lon, key = items
    result = fetch_weather(lat, lon, key)

    assert result == {"ok": True}

# ошибка сервера
@patch("api.requests.get")
def test_fetch_weather_api_error(mock_get, mock_response, items):
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    lat, lon, key = items
    result = fetch_weather(lat, lon, key)

    assert result is None

# корректный json
def test_parse_weather_success():
    data = {
        "name": "Москва",
        "main": {"temp": 5.0, "humidity": 80},
        "weather": [{"description": "пасмурно"}],
        "wind": {"speed": 3.2}
    }

    result = parse_weather(data)

    assert result == {
        "Город": "Москва",
        "Температура": 5.0,
        "Описание погоды": "пасмурно",
        "Скорость ветра": 3.2,
        "Влажность": 80
    }


# тест с неверным json ответом
def test_parse_weather_bad_json():
    data = {}  # нет нужных полей
    result = parse_weather(data)

    assert result is None

# успешний сценарий
@patch("api.fetch_weather")
@patch("api.parse_weather")
def test_get_weather_success(mock_parse, mock_fetch, items):
    mock_fetch.return_value = {"raw": True}
    mock_parse.return_value = {"ok": True}

    result = get_weather(*items)

    assert result == {"ok": True}
