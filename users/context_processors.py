from django.conf import settings

def auth_settings(request):
    return {
        'telegram_bot_name': settings.TELEGRAM_BOT_NAME
    }
