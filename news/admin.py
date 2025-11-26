from django.contrib import admin
from .models import News, NewsCard

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_by', 'published_at')
    search_fields = ('title', 'content')
    list_filter = ('published_at',)
    date_hierarchy = 'published_at'

@admin.register(NewsCard)
class NewsCardAdmin(admin.ModelAdmin):
    list_display = ('news', 'description')

