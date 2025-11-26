from django.shortcuts import render
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta
from news.models import News
from inventory.models import Item
from events.models import Event

def index(request):
    # Данные об адресе и количестве резидентов теперь берутся из context_processors.py
    
    # 1. Новости (Кэш 15 минут)
    news_list = cache.get('homepage_news')
    if news_list is None:
        seven_days_ago = timezone.now() - timedelta(days=7)
        news_list = list(News.objects.filter(published_at__gte=seven_days_ago).order_by('-published_at'))
        cache.set('homepage_news', news_list, 60 * 15)

    # 2. Оборудование (Кэш 30 минут)
    equipment_list = cache.get('homepage_equipment')
    if equipment_list is None:
        equipment_list = list(Item.objects.filter(is_available_for_loan=True)[:6])
        cache.set('homepage_equipment', equipment_list, 60 * 30)

    # 3. Ивенты (Кэш 15 минут)
    events_list = cache.get('homepage_events')
    if events_list is None:
        events_list = list(Event.objects.filter(date__gte=timezone.now()).order_by('date')[:6])
        cache.set('homepage_events', events_list, 60 * 15)

    context = {
        'news_list': news_list,
        'equipment_list': equipment_list,
        'events_list': events_list,
    }
    return render(request, 'website/index.html', context)