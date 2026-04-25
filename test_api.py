import pytest
from unittest.mock import patch, MagicMock
from api import get_weather


# тест на успешней ответ
def test_get_weather_success():

    # фейковый объект ответа requests.get()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "Москва",
        "main": {"temp": 5.0, "humidity": 80},
        "weather": [{"description": "пасмурно"}],
        "wind": {"speed": 3.2}
    }

    # подмена requests.get внутри api.py
    with patch("api.requests.get", return_value=mock_response):
        result = get_weather(55.75, 37.61, "FAKE_KEY")

    # проверка
    assert result == {
        "Город": "Москва",
        "Температура": 5.0,
        "Описание погоды": "пасмурно",
        "Скорость ветра": 3.2,
        "Влажность": 80
    }

# тест с неверным json ответом
def test_get_weather_bad_json():

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}  # пустой JSON

    with patch("api.requests.get", return_value=mock_response):
        result = get_weather(55.75, 37.61, "FAKE_KEY")

    assert result is None

# ошибка сервера
def test_get_weather_api_error():

    mock_response = MagicMock()
    mock_response.status_code = 404  # ошибка API

    with patch("api.requests.get", return_value=mock_response):
        result = get_weather(55.75, 37.61, "FAKE_KEY")

    assert result is None

# ошибка сети
def test_get_weather_exception():

    with patch("api.requests.get", side_effect=Exception("ошибка сети")):
        result = get_weather(55.75, 37.61, "FAKE_KEY")

    assert result is None
