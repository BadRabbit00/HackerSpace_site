from django.core.cache import cache
from .models import SiteSettings

# Заглушка для модели резидентов (пока не создана)
class Resident:
    class objects:
        @staticmethod
        def count():
            return 42  # Заглушка

def site_info(request):
    # 1. Получаем статические данные (адрес, часы работы)
    settings = SiteSettings.objects.first()
    
    # Если настроек нет в БД, используем дефолтные
    address = settings.address if settings else 'г. Алматы, ул. Байзакова, 280, Smart Point'
    
    # 2. Получаем динамические данные (кол-во участников)
    # Можно добавить кэширование, если запросы станут тяжелыми
    count = Resident.objects.count()

    # Возвращаем словарь. Эти переменные будут доступны во ВСЕХ HTML шаблонах.
    return {
        'address': address,
        'residents_count': count,
        'site_settings': settings, # На случай если нужны другие поля
    }