from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News, NewsCard

@receiver(post_save, sender=News)
def create_news_card(sender, instance, created, **kwargs):
    if created and hasattr(instance, '_card_description'):
        NewsCard.objects.create(news=instance, description=instance._card_description)
