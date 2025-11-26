from django.core.cache import cache
from .models import SiteSettings
from account.models import Profile

def site_info(request):
    # 1. Получаем статические данные (адрес, часы работы)
    settings = SiteSettings.objects.first()
    
    # Если настроек нет в БД, используем дефолтные
    address = settings.address if settings else 'г. Алматы, ул. Байзакова, 280, Smart Point'
    
    # 2. Получаем динамические данные (кол-во участников)
    # Считаем профили, у которых текущий план дает статус резидента
    # Кэшируем результат на 24 часа, так как это тяжелый запрос для каждого хита
    count = cache.get('residents_count')
    if count is None:
        count = Profile.objects.filter(current_plan__grants_resident_status=True).count()
        cache.set('residents_count', count, 60 * 60 * 24)

    # Возвращаем словарь. Эти переменные будут доступны во ВСЕХ HTML шаблонах.
    return {
        'address': address,
        'residents_count': count,
        'site_settings': settings, # На случай если нужны другие поля
    }