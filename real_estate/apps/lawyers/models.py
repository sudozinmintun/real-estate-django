from django.db import models
from apps.companies.models import Company
from django.contrib.auth.models import User


class Lawyer(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="lawyers",
        null=True,
        blank=True,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lawyer_created",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
