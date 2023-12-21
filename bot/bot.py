import logging

import telebot

from django.conf import settings

from telebot.types import Message, ReplyKeyboardMarkup
from api.yandex_api import get_forecast_weather_by_city


logger = logging.getLogger(__name__)

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add('Погода')


@bot.message_handler(commands=['start'])
def start_handler(message: Message) -> None:
    text = 'Здравствуйте! Этот бот поможет вам узнать прогноз погоды ' \
           'на текущий день в любом городе России'
    bot.reply_to(message, text=text, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text.lower() == 'погода')
def get_weather(message: Message) -> None:
    bot.reply_to(message, 'Введите город')
    bot.register_next_step_handler(message, return_weather)


def return_weather(message: Message) -> None:
    try:
        text = get_forecast_weather_by_city(message.text)
    except ValueError as err:
        logger.error(err)
        text = str(err)
    except Exception as err:
        logger.error(err)
        text = 'При запросе погоды произошла ошибка'

    bot.reply_to(message, text=text)


def start_bot() -> None:
    bot.polling(none_stop=True)
