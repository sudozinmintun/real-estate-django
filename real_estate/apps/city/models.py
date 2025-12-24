from django.db import models
from apps.country.models import Country


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities"
    )

    class Meta:
        unique_together = ("name", "country")
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Township(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="townships")

    class Meta:
        verbose_name_plural = "Townships"
        unique_together = ("name", "city")

    def __str__(self):
        return f"{self.name}, {self.city.name}"
