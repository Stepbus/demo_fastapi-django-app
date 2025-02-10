from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=10, unique=True, db_index=True)

    class Meta:
        db_table = 'currency'
        verbose_name_plural = 'Currency'

    def __str__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'providers'
        verbose_name_plural = 'providers'

    def __str__(self):
        return self.name


class Block(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="blocks")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="blocks")
    block_number = models.BigIntegerField(unique=True, db_index=True)
    created_at = models.DateTimeField(null=True, blank=True)
    stored_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['block_number']
        db_table = 'blocks'
        verbose_name_plural = 'blocks'

    def __str__(self):
        return f"{self.currency.name} - Block {self.block_number}"
