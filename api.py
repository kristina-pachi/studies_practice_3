# 2. Получение данных о погоде через API.


import requests


api_url = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(lat: float, lon: float, api_key: str) -> dict | None:

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }

    try:
        response = requests.get(api_url, params=params, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()

        return {
            "Город": data["name"],
            "Температура": data["main"]["temp"],
            "Описание погоды": data["weather"][0]["description"],
            "Скорость ветра": data["wind"]["speed"],
            "Влажность": data["main"]["humidity"]
        }

    except Exception:
        return None

print(get_weather(55.75396, 37.62039, "016409432b4afafeb6d7bf65196c12e2"))
