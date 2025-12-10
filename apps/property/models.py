from django.db import models
from django.contrib.auth.models import User
from apps.city.models import Township, City
from apps.country.models import Country, Currency
from apps.property_type.models import PropertyType
from apps.amenities.models import Amenity


class Property(models.Model):
    property_id = models.CharField(max_length=500, blank=True, unique=True)
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True, blank=True)
    township = models.ForeignKey(
        Township, on_delete=models.DO_NOTHING, null=True, blank=True
    )

    # Property Type
    property_type = models.ForeignKey(
        PropertyType, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Purpose (Rent / Sell)
    PURPOSE_CHOICES = (
        ("rent", "Rent"),
        ("sell", "Sell"),
    )
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES, default="rent")

    area = models.CharField(max_length=100, null=True, blank=True)
    # Area unit
    AREA_UNIT_CHOICES = (
        ("sqft", "Sqft"),
        ("acre", "Acre"),
        ("sqm", "m²"),
    )
    area_unit = models.CharField(
        max_length=10, choices=AREA_UNIT_CHOICES, null=True, blank=True
    )

    # Price + Currency
    price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Furnished / Hall / Other
    property_status = models.CharField(max_length=50, null=True, blank=True)

    # Video Link
    video_link = models.URLField(max_length=500, null=True, blank=True)

    # Amenities (Many to Many)
    amenities = models.ManyToManyField(Amenity, null=True, blank=True)

    # User who posted
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    floor = models.CharField(max_length=100, null=True, blank=True)
    bedroom = models.CharField(max_length=100, null=True, blank=True)
    bathroom = models.CharField(max_length=100, null=True, blank=True)
    advertiser = models.CharField(max_length=500, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.property_id:
            last_property = Property.objects.order_by("-property_id").first()
            if last_property and last_property.property_id.isdigit():
                new_id = int(last_property.property_id) + 1
            else:
                new_id = 1
            self.property_id = str(new_id).zfill(6)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PropertyPhoto(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(upload_to="property/photos/")
    created_at = models.DateTimeField(auto_now_add=True)
