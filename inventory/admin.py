from django.contrib import admin
from .models import Item, Loan

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'inventory_number', 'get_owner_display', 'is_available_for_loan', 'rent_price_per_day')
    search_fields = ('name', 'inventory_number', 'description')
    list_filter = ('is_available_for_loan', ('owner', admin.EmptyFieldListFilter))
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'inventory_number', 'description')
        }),
        ('Владелец', {
            'fields': ('owner',),
            'description': 'Оставьте пустым, если вещь принадлежит Хакерспейсу'
        }),
        ('Условия аренды', {
            'fields': ('is_available_for_loan', 'rent_price_per_day')
        }),
    )

    def get_owner_display(self, obj):
        return obj.owner if obj.owner else "HackerSpace"
    get_owner_display.short_description = "Владелец"

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('item', 'borrower', 'status', 'deadline', 'taken_at')
    list_filter = ('status', 'deadline')
    search_fields = ('item__name', 'borrower__username', 'purpose')
    autocomplete_fields = ['item', 'borrower']

