from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):

    telegram_id = models.CharField(max_length=50, unique=True, blank=True, null=True)


    def if_verified(self):
        return bool(self.telegram_id)

class PersonalData(models.Model):
    STATUS_CHOICES = [
        ('not_submitted', 'Не подано'),
        ('pending', 'На проверке'),
        ('approved', 'Подтверждено'), # Только этот статус дает право брать вещи
        ('rejected', 'Отклонено'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_data')
    # Можно добавить поля: ИИН, Адрес, Сканы, если нужно, но пока оставим базовую структуру как в запросе
    # или перенесем те поля, что были в account/models.py
    full_name = models.CharField("ФИО", max_length=255, blank=True)
    iin = models.CharField("ИИН", max_length=12, blank=True)
    address = models.TextField("Адрес прописки", blank=True)
    
    document_scan_front = models.FileField("Скан документа (лицевая)", upload_to='docs/private/', blank=True, null=True)
    document_scan_back = models.FileField("Скан документа (обратная)", upload_to='docs/private/', blank=True, null=True)
    
    # Специфичное поле для студентов
    student_document = models.ImageField(
        "Скан студенческого", 
        upload_to='docs/students/', 
        null=True, 
        blank=True
    )

    verification_status = models.CharField(choices=STATUS_CHOICES, default='not_submitted')
    manager_comment = models.TextField("Коммент менеджера (если отказ)", blank=True)

    def __str__(self):
        return f"PersonalData: {self.user.username}"

class AuthSettings(models.Model):
    telegram_bot_name = models.CharField(max_length=100, help_text="Username бота без @ (например, MyHackerSpaceBot)")

    def __str__(self):
        return "Настройки аутентификации"

    class Meta:
        verbose_name = "Настройки аутентификации"
        verbose_name_plural = "Настройки аутентификации"