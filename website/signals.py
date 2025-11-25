from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Person

# Срабатывает при сохранении или удалении пользователя
@receiver([post_save, post_delete], sender=Person)
def clear_cache(sender, instance, **kwargs):
    # Удаляем устаревшее значение из Redis
    cache.delete('total_participants')