import telebot
import settings
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

if settings.DEBUG:
    telebot.apihelper.proxy = {'https': settings.PROXY}

bot = telebot.TeleBot(settings.BOT_TOKEN, threaded=False)