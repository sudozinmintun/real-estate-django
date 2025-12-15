from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from apps.package.models import Package
from apps.payment.models import Payment


class Order(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending Approval"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    order_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        db_index=True,
        null=True,
        blank=True,
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    package = models.ForeignKey(Package, on_delete=models.PROTECT)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True
    )
    screenshot = models.ImageField(
        upload_to="order/screenshots/", null=True, blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING
    )

    # Frozen package snapshot
    package_name = models.CharField(max_length=100, editable=False)
    package_max_properties = models.PositiveIntegerField(editable=False)
    package_duration_months = models.PositiveIntegerField(editable=False)

    start_date = models.DateTimeField(null=True, blank=True, editable=False)
    end_date = models.DateTimeField(null=True, blank=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    _original_status = None

    class Meta:
        ordering = ["-created_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.status

    # ORDER ID
    def _generate_order_id(self):
        year = timezone.now().year
        last = (
            Order.objects.filter(order_id__startswith=f"ORD-{year}-")
            .order_by("id")
            .last()
        )
        number = int(last.order_id.split("-")[-1]) + 1 if last else 1
        return f"ORD-{year}-{number:06d}"

    # SAVE
    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            self.order_id = self._generate_order_id()
            self.package_name = self.package.name
            self.package_max_properties = self.package.max_properties
            self.package_duration_months = self.package.duration_months
            self.amount = self.package.price

        old_status = self._original_status
        new_status = self.status

        super().save(*args, **kwargs)

        # -----------------------------
        # STATUS TRANSITIONS
        # -----------------------------

        # PENDING / REJECTED ➜ APPROVED
        if old_status != self.STATUS_APPROVED and new_status == self.STATUS_APPROVED:
            self._activate()

        # APPROVED ➜ PENDING / REJECTED
        elif old_status == self.STATUS_APPROVED and new_status != self.STATUS_APPROVED:
            self.start_date = None
            self.end_date = None
            super().save(update_fields=["start_date", "end_date"])

        self._original_status = self.status

    # ACTIVATE
    def _activate(self):
        self.start_date = timezone.now()
        self.end_date = (
            self.start_date
            + relativedelta(months=self.package_duration_months)
            - relativedelta(days=1)
        )
        super().save(update_fields=["start_date", "end_date"])

    @classmethod
    def approved_orders(cls, user):
        now = timezone.now()
        return cls.objects.filter(
            user=user,
            status=cls.STATUS_APPROVED,
            start_date__lte=now,
            end_date__gte=now,
        )

    @classmethod
    def total_max_properties(cls, user):
        return (
            cls.approved_orders(user)
            .aggregate(total=models.Sum("package_max_properties"))
            .get("total")
            or 0
        )

    def __str__(self):
        return self.order_id
