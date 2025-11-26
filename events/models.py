from django.db import models
from django.conf import settings # Ссылка на твоего юзера
from account.models import SubscriptionPlan # Ссылка на твои тарифы

class Event(models.Model):
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")
    photo = models.ImageField(upload_to='event_photos/', null=True, blank=True)
    date = models.DateTimeField("Дата и время начала")
    location = models.CharField("Место проведения", max_length=200)
    price = models.DecimalField("Цена входа", max_digits=8, decimal_places=2, default=0)

    # === 1. СВЯЗЬ С ТАРИФОМ (Вместо строки) ===
    # Если поле пустое (null=True) - значит ивент доступен всем (бесплатно/без подписки)
    required_plan = models.ForeignKey(
        SubscriptionPlan, 
        on_delete=models.SET_NULL, # Если удалим тариф, ивент не удалится, поле станет пустым
        null=True, 
        blank=True,
        verbose_name="Минимальный тариф"
    )

    # === 2. ВЕДУЩИЙ (HOST) ===
    # Ссылка "Один ко Многим". Один юзер может вести много ивентов.
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # Удалим юзера -> удалятся его ивенты
        related_name='hosted_events', # Чтобы искать: user.hosted_events.all()
        verbose_name="Организатор"
    )

    # === 3. УЧАСТНИКИ (PARTICIPANTS) ===
    # Ссылка "Многие ко Многим". Юзер ходит на много ивентов, на ивенте много юзеров.
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='attended_events', # Чтобы искать: user.attended_events.all()
        blank=True, # Можно создать ивент без участников
        verbose_name="Участники"
    )

    def __str__(self):
        return f"{self.title} ({self.date.strftime('%d.%m %H:%M')})"