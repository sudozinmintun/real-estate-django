from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    default_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name
