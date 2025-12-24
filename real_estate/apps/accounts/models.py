from django.db import models
from apps.order.models import Order
from apps.country.models import Country
from apps.city.models import City
from django.contrib.auth.models import AbstractUser
from apps.companies.models import Company
from django.contrib.auth.models import User


class Profile(models.Model):
    MEMBER_TYPE_CHOICES = [
        ("ADMIN", "Admin"),
        ("MEMBER", "Member"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="user", null=True, blank=True
    )

    phone = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(
        max_length=10, choices=MEMBER_TYPE_CHOICES, default="MEMBER"
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name="profiles_country",
        null=True,
        blank=True,
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        related_name="profiles_city",
        null=True,
        blank=True,
    )
    address = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    facebook = models.TextField(blank=True, null=True)
    linkedin = models.TextField(blank=True, null=True)
    x = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)

    def total_max_properties(self):
        return Order.total_max_properties(self.user)

    def __str__(self):
        return f"Profile: {self.user.username}"
