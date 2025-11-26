from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

# 1. Конфигурация тарифов (чтобы менять цены/дни из админки)
class SubscriptionPlan(models.Model):
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", max_length=100, blank=True)
    slug = models.SlugField(unique=True) # free, resident_temp, resident_perm
    duration_days = models.PositiveIntegerField("Длительность (дней)", default=30)
    
    # Две цены
    price = models.DecimalField("Цена (KZT)", max_digits=10, decimal_places=0, default=0)
    student_price = models.DecimalField("Цена для студентов (KZT)", max_digits=10, decimal_places=0, null=True, blank=True)

    # Флаг: Является ли этот тариф "Резидентским"? 
    # (Например, "Ивент" - это не резиденство)
    grants_resident_status = models.BooleanField(default=True)
    
    is_public = models.BooleanField(default=True) # Виден ли в магазине

    def __str__(self):
        return self.title

# 2. Состояние пользователя
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    
    # Old fields kept
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    github_username = models.CharField(max_length=39, blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    telegram_username = models.CharField(max_length=32, blank=True, null=True)

    # New Subscription Logic
    current_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    subscription_end_date = models.DateField(blank=True, null=True)

    # === ЛОГИКА ЗАВИСИМОСТЕЙ ===

    @property
    def is_resident_active(self):
        """
        Базовая проверка: является ли он резидентом ПРЯМО СЕЙЧАС (без учета долгов).
        Нужно для отображения статуса 'Active' зеленым цветом.
        """
        if not self.current_plan or not self.subscription_end_date:
            return False
        return timezone.now().date() <= self.subscription_end_date

    @property
    def is_in_grace_period(self):
        """
        Проверка: находится ли он в 'Льготном периоде' (просрочил, но еще не выгнали).
        7 дней после окончания подписки.
        """
        if not self.current_plan or not self.subscription_end_date:
            return False
        
        today = timezone.now().date()
        grace_limit = self.subscription_end_date + timedelta(days=7)
        
        # Если дата окончания прошла, НО 7 дней еще не истекли
        return self.subscription_end_date < today <= grace_limit

    @property
    def has_access_to_space(self):
        """
        ГЛАВНЫЙ РУБИЛЬНИК ДОСТУПА В ПОМЕЩЕНИЕ.
        Пускаем, если подписка активна ИЛИ идет льготный период.
        """
        # Если план не дает резидентства (например, просто регистрация) -> False
        if self.current_plan and not self.current_plan.grants_resident_status:
            return False
            
        return self.is_resident_active or self.is_in_grace_period

    def __str__(self):
        return f"Profile of {self.user.username}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('completed', 'Оплачено'),
        ('failed', 'Ошибка'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment {self.id} - {self.user.username} - {self.amount}"