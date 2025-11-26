from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('address', 'working_hours', 'phone', 'email')
    
    # Ограничиваем создание более одной записи настроек
    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return True

    # Запрещаем удаление записи, НО редактирование (изменение полей) остается доступным!
    # Это защищает от случайного удаления единственной записи с настройками.
    def has_delete_permission(self, request, obj=None):
        return False

    # Улучшение: Если настройки уже созданы, при клике на "Site Settings" в админке
    # мы сразу попадаем на страницу редактирования, минуя список.
    def changelist_view(self, request, extra_context=None):
        if SiteSettings.objects.exists():
            obj = SiteSettings.objects.first()
            # admin:app_label_modelname_change
            return redirect(reverse('admin:website_sitesettings_change', args=[obj.pk]))
        return super().changelist_view(request, extra_context)

