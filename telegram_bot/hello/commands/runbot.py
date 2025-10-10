from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from hello.models import TgUser, Message

class Command(BaseCommand):
    help = 'Run Telegram bot (polling)'

    def handle(self, *args, **options):
        token = settings.TELEGRAM_TOKEN
        if not token:
            self.stderr.write("TELEGRAM_TOKEN не задан в settings")
            return
        bot = telebot.TeleBot(token, parse_mode='HTML')

        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            tg = message.from_user
            user, created = TgUser.objects.get_or_create(
                telegram_id=tg.id,
                defaults={
                    'username': tg.username,
                    'first_name': tg.first_name,
                    'last_name': tg.last_name
                }
            )
            if not created:
                # обновим данные
                changed = False
                if user.username != tg.username:
                    user.username = tg.username; changed = True
                if user.first_name != tg.first_name:
                    user.first_name = tg.first_name; changed = True
                if user.last_name != tg.last_name:
                    user.last_name = tg.last_name; changed = True
                if changed:
                    user.save()
            bot.send_message(message.chat.id, f"Привет, {tg.first_name or tg.username or 'user'}! Вы зарегистрированы.")

        @bot.message_handler(commands=['help'])
        def help_cmd(message):
            bot.send_message(message.chat.id, "Доступные команды:\n/start - регистрация\n/help - помощь")

        @bot.message_handler(func=lambda m: True)
        def echo_all(message):
            tg = message.from_user
            user, _ = TgUser.objects.get_or_create(
                telegram_id=tg.id,
                defaults={'username': tg.username, 'first_name': tg.first_name, 'last_name': tg.last_name}
            )
            Message.objects.create(user=user, text=message.text)
            bot.send_message(message.chat.id, f"Вы написали: {message.text}")

        self.stdout.write("Запуск бота (polling)...")
        bot.infinity_polling()