import logging
from django.conf import settings
import telebot

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(settings.TELEGRAM_TOKEN, parse_mode='HTML')

from .models import TgUser, Message  # импорт моделей после создания bot

@bot.message_handler(commands=['start'])
def handle_start(message):
    tg = message.from_user
    user, created = TgUser.objects.get_or_create(
        telegram_id=tg.id,
        defaults={'username': tg.username, 'first_name': tg.first_name, 'last_name': tg.last_name}
    )
    if not created:
        changed = False
        if user.username != tg.username:
            user.username = tg.username; changed = True
        if user.first_name != tg.first_name:
            user.first_name = tg.first_name; changed = True
        if user.last_name != tg.last_name:
            user.last_name = tg.last_name; changed = True
        if changed:
            user.save()
    try:
        bot.send_message(message.chat.id, f"Привет, {tg.first_name or tg.username or 'пользователь'}! Вы зарегистрированы.")
    except Exception:
        logger.exception("Ошибка при отправке /start")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    try:
        tg = message.from_user
        user, _ = TgUser.objects.get_or_create(
            telegram_id=tg.id,
            defaults={'username': tg.username, 'first_name': tg.first_name, 'last_name': tg.last_name}
        )
        Message.objects.create(user=user, text=message.text or '')
        bot.send_message(message.chat.id, f"Вы написали: {message.text}")
    except Exception:
        logger.exception("Ошибка при обработке сообщения")

@bot.message_handler(content_types=['text'])
def test(message):
    if message.text == "hello":
        bot.send_message(message, 'hello зайка попрыгайка!!!')
def start_bot():
    logger.info("Запуск Telegram polling...")
    try:
        bot.infinity_polling(skip_pending=True, timeout=20)
    except Exception:
        logger.exception("Polling завершился с ошибкой")
