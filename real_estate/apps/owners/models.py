from django.db import models
from apps.companies.models import Company
from django.contrib.auth.models import User


class Owner(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="owner", null=True, blank=True
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
