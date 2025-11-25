from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):

    telegram_id = models.CharField(max_length=50, unique=True, blank=True, null=True)


    def if_verified(self):
        return bool(self.telegram_id)

class AuthSettings(models.Model):
    telegram_bot_name = models.CharField(max_length=100, help_text="Username бота без @ (например, MyHackerSpaceBot)")

    def __str__(self):
        return "Настройки аутентификации"

    class Meta:
        verbose_name = "Настройки аутентификации"
        verbose_name_plural = "Настройки аутентификации"
