from aiogram.dispatcher.filters.state import State, StatesGroup


class WeatherState(StatesGroup):
    wait_city_name = State()
