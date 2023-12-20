import requests

from django.conf import settings

from api.models import City


class Fact:
    def __init__(
            self, *, temp: float, wind_speed: float, pressure_mm: int, **kwargs):
        self.temp = temp
        self.wind_speed = wind_speed
        self.pressure_mm = pressure_mm


def get_win_dir(win_dir: str) -> str:
    win_dirs = {
        'nw': 'северо - западное',
        'n': 'северное',
        'ne': 'северо - восточное',
        'e': 'восточное',
        'se': 'юго - восточное',
        's': 'южное',
        'sw': 'юго - западное',
        'w': 'западное',
        'c': 'штиль',
    }
    return win_dirs.get(win_dir, 'неизвестно')


class ForecastPartDey:
    prec_types = ['без осадков', 'дождь', 'дождь со снегом', 'снег']
    part_names = {
        'night': 'ночь', 'morning': 'утро', 'day': 'день', 'evening': 'вечер'
    }

    def __init__(
            self, *, part_name: str, temp_min: float, temp_max: float,
            wind_speed: float, wind_dir: str,pressure_mm: float,
            prec_type: str, humidity: float, **kwargs
    ):
        self.part_name = part_name
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.wind_speed = wind_speed
        self.wind_dir = wind_dir
        self.pressure_mm = pressure_mm
        self.prec_type = int(prec_type)
        self.humidity = humidity

    @property
    def info(self) -> str:
        text = (
            f'{self.part_names.get(self.part_name)}\n'
            f'температура от {self.temp_min}°C до  {self.temp_max}°C\n'
            f'ветер {self.wind_speed} м/с, направление {get_win_dir(self.wind_dir)}\n'
            f'давление {self.pressure_mm} мм рт. ст., влажность {self.humidity}%\n'
            f'осадки {self.prec_types[self.prec_type]}'
        )
        return text


class Forecast:
    part_names = {
        'night': 'прогноз на ночь',
        'morning': 'прогноз на утро',
        'day': 'прогноз на день',
        'evening': 'прогноз на вечер'
    }

    def __init__(
            self, *, parts: dict, **kwargs):
        self.parts = parts

    @property
    def forecast(self) -> str:
        forecast = ''
        for part_name, part_text in self.part_names.items():
            part: dict = self.parts.get(part_name)
            if part:
                forecast += ForecastPartDey(part_name=part_name, **part).info + '\n\n'
        return forecast


def get_weather_by_city(
        city_name: str, lang: str = 'ru_RU', limit: int = 1, **kwargs) -> dict:

    try:
        city = City.objects.get(name__iexact=city_name.strip())
    except City.DoesNotExist as err:
        raise ValueError('Город не найден в базе')

    params = {'lat': city.lat, 'lon': city.lon, 'lang': lang, 'limit': limit}
    params.update(kwargs)
    try:
        response = requests.get(
            url=settings.WEATHER_URL,
            headers={"X-Yandex-API-Key": settings.YANDEX_API_KEY},
            params=params,
            timeout=(5, 10)
        )
    except requests.exceptions.Timeout as err:
        raise ValueError('Сервер погоды не ответил в отведенный период')

    return response.json()


def get_fact_weather_by_city(
        city_name: str, lang: str = 'ru_RU', limit: int = 1, **kwargs) -> Fact:
    """
    Get fact weather.
    """
    weather = get_weather_by_city(
        city_name=city_name, lang=lang, limit=limit, **kwargs)
    return Fact(**weather.get('fact'))


def get_forecast_weather_by_city(
        city_name: str, lang: str = 'ru_RU', limit: int = 1, **kwargs) -> str:
    """
    Get forecasts weather.
    """
    weather = get_weather_by_city(
        city_name=city_name, lang=lang, limit=limit, **kwargs)
    data = weather.get('forecasts')[0]
    response = Forecast(**data).forecast
    return response if response else 'Город не найден.'
