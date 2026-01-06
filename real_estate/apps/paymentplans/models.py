from django.db import models
from django.core.exceptions import ValidationError
from apps.companies.models import Company
from django.contrib.auth.models import User


class PaymentPlan(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

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

    def __str__(self):
        return self.name


class PaymentPlanStep(models.Model):
    STEP_TYPES = [
        ("down_payment", "Down Payment"),
        ("installment", "Installment"),
        ("milestone", "Milestone"),
        ("bank_loan", "Bank Loan"),
        ("balloon", "Balloon Payment"),
        ("full_payment", "Full Payment"),
    ]

    plan = models.ForeignKey(
        PaymentPlan,
        related_name="steps",
        on_delete=models.CASCADE,
    )

    step_type = models.CharField(max_length=20, choices=STEP_TYPES)

    # Human-friendly display text (optional)
    label = models.CharField(max_length=120, blank=True)

    # Percentage of total price
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    # For installment / timing logic
    months = models.PositiveIntegerField(null=True, blank=True)
    due_after_month = models.PositiveIntegerField(null=True, blank=True)

    # Sort order for display
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        label = self.label or self.get_step_type_display()
        return f"{self.plan.name} — {label} ({self.percentage}%)"

    def clean(self):
        """
        Ensure plan total never exceeds 100%
        """
        existing_total = sum(s.percentage for s in self.plan.steps.exclude(id=self.id))
        if existing_total + self.percentage > 100:
            raise ValidationError("Total percentage for a plan cannot exceed 100%.")
