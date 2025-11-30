from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "package_name",
        "package_max_properties",
        "package_duration_type",
        "amount",
        "status",
        "start_date",
        "end_date",
        "created_at",
    )
    list_filter = ("status", "package_duration_type")
    search_fields = ("user__username", "package_name")
    list_editable = ("status",)

    ordering = ("-created_at",)
