from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "duration_months",
        "max_properties",
        "is_default",
        "is_active",
    )
