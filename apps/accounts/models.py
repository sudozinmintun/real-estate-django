from django.db import models
from django.contrib.auth.models import User
from apps.order.models import Order


class Profile(models.Model):
    MEMBER_TYPE_CHOICES = [
        ("ADMIN", "Admin"),
        ("MEMBER", "Member"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(
        max_length=10, choices=MEMBER_TYPE_CHOICES, default="MEMBER"
    )
    address = models.TextField(blank=True, null=True)

    def total_max_properties(self):
        return Order.total_max_properties(self.user)

    def __str__(self):
        return f"Profile: {self.user.username}"
