from django.db import models
from apps.companies.models import Company
from django.contrib.auth.models import User
from apps.property.models import Property

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

    @property
    def progress_style(self):
        return f"width: {self.deal_probability}%;"

    def __str__(self):
        return self.name


class CommunicationLog(models.Model):
    TYPE_CHOICES = [
        ("call", "Call"),
        ("visit", "Visit / Meeting"),
        ("message", "SMS / Text Message"),
        ("email", "Email"),
        ("viber", "Viber"),
        ("whatsapp", "WhatsApp"),
        ("telegram", "Telegram"),
        ("note", "Note"),
    ]

    # Relationships
    buyer = models.ForeignKey(
        Buyer, on_delete=models.CASCADE, related_name="communications"
    )
    related_property = models.ForeignKey(
        Property, on_delete=models.SET_NULL, null=True, blank=True
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_communications",
        help_text="Staff responsible for this log",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="communications",
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_communications",
    )

    # Fields
    communication_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    content = models.TextField(
        null=True, blank=True, help_text="Optional details about this communication"
    )
    reminder_date = models.DateField(
        null=True, blank=True, help_text="Optional follow-up date"
    )
    reminder_time = models.TimeField(
        null=True, blank=True, help_text="Optional follow-up time"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
