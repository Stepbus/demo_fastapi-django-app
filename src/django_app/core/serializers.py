from rest_framework import serializers

from django_app.core.models import Currency, Provider, Block


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["id", "name"]


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ["id", "name"]


class BlockSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(slug_field="name", queryset=Currency.objects.all())
    provider = serializers.SlugRelatedField(slug_field="name", queryset=Provider.objects.all())

    class Meta:
        model = Block
        fields = ["id", "currency", "provider", "block_number", "created_at", "stored_at"]
