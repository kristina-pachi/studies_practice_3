import pytest
from unittest.mock import patch, MagicMock
from api import get_weather


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
