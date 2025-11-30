from django.db import models
from django.contrib.auth.models import User
from apps.package.models import Package
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class Order(models.Model):

    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending Approval"),
        (STATUS_APPROVED, "Approved (Subscription Active)"),
        (STATUS_REJECTED, "Rejected / Failed Payment"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    package = models.ForeignKey(
        Package, on_delete=models.PROTECT, related_name="orders"
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING
    )

    # Freeze package state
    package_name = models.CharField(max_length=100, editable=False)
    package_max_properties = models.PositiveIntegerField(default=0, editable=False)
    package_duration_type = models.CharField(max_length=10, editable=False)

    start_date = models.DateTimeField(editable=False, null=True, blank=True)
    end_date = models.DateTimeField(editable=False, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    _original_status = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.status

    def save(self, *args, **kwargs):
        if not self.pk:
            self.package_name = self.package.name
            self.package_max_properties = self.package.max_properties
            self.package_duration_type = self.package.duration_type

        status_changed = self.status != self._original_status
        super().save(*args, **kwargs)

        if status_changed and self.status == self.STATUS_APPROVED:
            self._set_dates_for_stacked_subscription()

        self._original_status = self.status

    def _set_dates_for_stacked_subscription(self):

        latest_order = (
            Order.objects.filter(user=self.user, status=self.STATUS_APPROVED)
            .exclude(pk=self.pk)
            .order_by("-end_date")
            .first()
        )

        if latest_order and latest_order.end_date:
            self.start_date = latest_order.end_date + relativedelta(days=1)
        else:
            self.start_date = timezone.now()

        if self.package_duration_type == "MONTH":
            self.end_date = (
                self.start_date + relativedelta(months=1) - relativedelta(days=1)
            )
        elif self.package_duration_type == "YEAR":
            self.end_date = (
                self.start_date + relativedelta(years=1) - relativedelta(days=1)
            )

        super().save(update_fields=["start_date", "end_date"])

    @classmethod
    def approved_orders(cls, user):
        return cls.objects.filter(user=user, status=cls.STATUS_APPROVED)

    @classmethod
    def total_max_properties(cls, user):
        return sum(o.package_max_properties for o in cls.approved_orders(user))

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - {self.package_name} ({self.status})"
