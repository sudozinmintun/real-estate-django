from django.db import models
from django.contrib.auth.models import User
from apps.city.models import Township, City
from apps.country.models import Country


class Property(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=0)

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    township = models.ForeignKey(Township, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
