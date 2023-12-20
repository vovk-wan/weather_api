import logging

from django.core.management.base import BaseCommand
from bot.bot import start_bot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Запуск телеграм бота'

    def handle(self, *args, **options):
        try:
            start_bot()
            logger.info('telegram bot started.')
        except Exception as e:
            logger.error(e)
