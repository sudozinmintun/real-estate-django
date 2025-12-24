from django.db import models
from django.core.exceptions import ValidationError


class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    duration_months = models.PositiveIntegerField(default=1)
    max_properties = models.PositiveIntegerField(default=0)

    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.duration_months} months)"
