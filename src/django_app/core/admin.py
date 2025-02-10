from django.contrib import admin

from django_app.core.models import Currency, Provider, Block


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "api_key")
    search_fields = ("name",)


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("id", "currency", "provider", "block_number", "created_at", "stored_at")
    search_fields = ("currency__name", "provider__name", "block_number")
    list_filter = ("currency", "provider")
