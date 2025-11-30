from django.db import models
from django.core.exceptions import ValidationError


class Package(models.Model):
    DURATION_CHOICES = [
        ("MONTH", "Monthly"),
        ("YEAR", "Yearly"),
    ]

    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=0,
        help_text="Price in Kyat (0 for free plan)",
    )
    max_properties = models.PositiveIntegerField(
        help_text="Maximum number of active properties allowed for this plan. Use 0 for unlimited."
    )
    duration_type = models.CharField(
        max_length=5,
        choices=DURATION_CHOICES,
        default="MONTH",
        help_text="Type of subscription duration",
    )
    is_default = models.BooleanField(
        default=False,
        help_text="If checked, this is the free plan automatically assigned to new users.",
    )

    class Meta:
        verbose_name_plural = "Packages (Subscription Plans)"

    def clean(self):
        if self.is_default:
            qs = Package.objects.filter(is_default=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    "There is already a package marked as default. Only one default package is allowed."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        status = " (Default/Free)" if self.is_default else ""
        limit = self.max_properties if self.max_properties > 0 else "Unlimited"
        duration = "Monthly" if self.duration_type == "MONTH" else "Yearly"
        return (
            f"{self.name} ({duration} - {limit} properties) - {self.price} Kyat{status}"
        )
