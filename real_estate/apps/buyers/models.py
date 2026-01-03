from django.db import models
from apps.companies.models import Company
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ("new", "New"),
    ("contacted", "Contacted"),
    ("interested", "Interested"),
    ("negotiating", "Negotiating"),
    ("closed", "Closed"),
    ("lost", "Lost"),
]

SOURCE_CHOICES = [
    ("website", "Website"),
    ("facebook", "Facebook"),
    ("referral", "Referral"),
    ("walk_in", "Walk-in"),
    ("other", "Other"),
]


class Buyer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="buyers", null=True, blank=True
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    source = models.CharField(
        max_length=50, choices=SOURCE_CHOICES, null=True, blank=True
    )

    # Probability 0–100
    deal_probability = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Chance (0–100%) that this buyer will purchase.",
    )

    # Budget + preferences
    budget_min = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    budget_max = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    preferred_location = models.CharField(max_length=255, null=True, blank=True)
    preferred_type = models.CharField(max_length=100, null=True, blank=True)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_buyers",
    )

    notes = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyer_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["phone"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return self.name
