from django.db import models
from apps.companies.models import Company
from django.contrib.auth.models import User
from apps.property.models import Property
from apps.lawyers.models import Lawyer
from apps.buyers.models import Buyer
from apps.owners.models import Owner


class Contract(models.Model):
    CONTRACT_TYPES = [
        ("sale", "Sale Agreement"),
        ("lease", "Lease Agreement"),
        ("transfer", "Ownership Transfer"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("under_review", "Under Lawyer Review"),
        ("approved", "Approved"),
        ("signed", "Signed"),
        ("cancelled", "Cancelled"),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="contracts",
    )

    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.CASCADE,
        related_name="contracts",
    )

    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name="contracts",
    )

    lawyer = models.ForeignKey(
        Lawyer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contracts",
    )

    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPES)
    contract_date = models.DateField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="draft",
    )

    notes = models.TextField(blank=True)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="contracts",
        null=True,
        blank=True,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contract_created",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.property} — {self.contract_type} ({self.status})"
