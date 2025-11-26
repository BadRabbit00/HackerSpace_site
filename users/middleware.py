from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class TelegramRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 0. Если проверка отключена в настройках — пропускаем
        if not getattr(settings, 'TELEGRAM_AUTH_REQUIRED', True):
            return self.get_response(request)

        # 1. Если пользователь НЕ залогинен — пропускаем.
        # Пусть с ним разбираются @login_required или LoginView.
        if not request.user.is_authenticated:
            return self.get_response(request)

        # 2. Если у пользователя УЖЕ есть Telegram ID — пропускаем.
        # Он полноценный участник.
        if request.user.telegram_id:
            return self.get_response(request)

        # 3. БЕЛЫЙ СПИСОК (Whitelist)
        # Сюда пишем URL-ы, на которые МОЖНО заходить без Телеграма.
        # Иначе будет "вечный цикл" (Infinite Redirect Loop).
        exempt_urls = [
            reverse('connect_telegram'),        # Сама страница привязки
            reverse('link_telegram_callback'),  # Вьюха, которая ловит ответ от Телеги
            reverse('logout'),                  # Кнопка выхода (если он передумал)
        ]

        # Если пользователь идет на разрешенную страницу — пропускаем
        if request.path in exempt_urls:
            return self.get_response(request)
        
        # Дополнительно: можно разрешить админку, если админы входят без телеги
        if request.path.startswith('/admin/'):
             return self.get_response(request)

        # 4. ВСЕ ОСТАЛЬНОЕ — БЛОКИРУЕМ
        # Если он пытается зайти в /account/, /forum/ или просто на главную,
        # редиректим его на привязку.
        return redirect('connect_telegram')