from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from account.models import Profile
from news.models import News
from events.models import Event
from inventory.models import Item

# 1. Инвалидация счетчика резидентов
@receiver([post_save, post_delete], sender=Profile)
def clear_residents_count(sender, instance, **kwargs):
    cache.delete('residents_count')

# 2. Инвалидация новостей на главной
@receiver([post_save, post_delete], sender=News)
def clear_news_cache(sender, instance, **kwargs):
    cache.delete('homepage_news')

# 3. Инвалидация ивентов на главной
@receiver([post_save, post_delete], sender=Event)
def clear_events_cache(sender, instance, **kwargs):
    cache.delete('homepage_events')

# 4. Инвалидация оборудования на главной
@receiver([post_save, post_delete], sender=Item)
def clear_equipment_cache(sender, instance, **kwargs):
    cache.delete('homepage_equipment')