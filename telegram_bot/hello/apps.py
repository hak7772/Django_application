from django.apps import AppConfig


class HelloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hello'

    def ready(self):
        import os, sys, threading
        # стартуем только при запуске runserver (dev) и только в основном дочернем процессе autoreload
        if 'runserver' not in sys.argv:
            return
        run_main = os.environ.get('RUN_MAIN')
        if run_main != 'true' and '--noreload' not in sys.argv:
            return
        try:
            from . import bot as bot_module
        except Exception:
            return
        t = threading.Thread(target=bot_module.start_bot, name='TelegramBotThread', daemon=True)
        t.start()