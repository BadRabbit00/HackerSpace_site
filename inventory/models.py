from django.db import models
from users.models import User

class Item(models.Model):
    OWNER_TYPE_CHOICES = [
        ('space', 'Собственность Спейса'),
        ('user', 'Собственность Резидента'),
    ]

    # Кто владелец? Если user=None, значит владелец - Спейс.
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_items')
    
    inventory_number = models.CharField(max_length=50, unique=True) # Штрихкод
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, default='General')
    
    # Цены и условия (если владелец хочет сдавать)
    rent_price_per_day = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    # Флаг: можно ли это вообще брать другим?
    is_available_for_loan = models.BooleanField(default=True) 

    def __str__(self):
        return f"{self.name} (#{self.inventory_number})"
    
class Loan(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Запрошено (ждет одобрения)'),
        ('active', 'На руках'),
        ('returned', 'Сдано'),
        ('overdue', 'Просрочено'),
        ('denied', 'Отклонено'),
        ('late_returned', 'Cдано с опозданием'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE) # Какую вещь взял
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans') # КТО взял
    
    taken_at = models.DateTimeField(null=True, blank=True) # Когда выдали
    deadline = models.DateTimeField() # Когда вернуть
    returned_at = models.DateTimeField(null=True, blank=True) # Когда вернул по факту
    
    status = models.CharField(choices=STATUS_CHOICES, default='requested')
    purpose = models.TextField("Цель использования") # Твое свободное поле

    # Сгенерированный документ (PDF)
    contract_file = models.FileField(upload_to='contracts/', null=True, blank=True)

    def __str__(self):
        return f"{self.item.name} -> {self.borrower.username}"