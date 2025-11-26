from django.contrib import admin
from .models import User, AuthSettings, PersonalData
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(PersonalData)

@admin.register(AuthSettings)
class AuthSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Запрещаем создавать больше одной записи
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Запрещаем удалять запись
        return False

