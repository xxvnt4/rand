from django.contrib import admin

from .models import Topics


@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'subtitle',
        'author',
        'is_watched',
        'id'
    ]
    list_per_page = 10
    readonly_fields = [
        'is_watched',
        'author'
    ]
