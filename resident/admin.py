from django.contrib import admin
from django.utils.html import format_html
from .models import Pathogen, Researcher


@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', 'email']


@admin.register(Pathogen)
class PathogenAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'creator',
        'origin',
        'is_available',
        'created_at'
    ]

    list_filter = [
        'is_available',
        'origin',
        'author',
        'creator'
    ]

    search_fields = [
        'title',
        'author__name',
        'creator__name',
        'family',
        'origin'
    ]

    date_hierarchy = 'created_at'

    fieldsets = (
        ("🧬 Основное", {
            'fields': ('title', 'description', 'image')
        }),
        ("👨‍🔬 Люди", {
            'fields': ('author', 'creator')
        }),
        ("🔬 Классификация", {
            'fields': ('family', 'origin', 'discovered')
        }),
        ("⚠️ Свойства", {
            'fields': ('application', 'transmission', 'is_available')
        }),
    )

    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.image.url)
        return "No Image"