from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price_display",
        "max_properties_display",
        "duration_type",
        "is_default",
        "verbose_clean_status",
    )

    list_filter = (
        "is_default",
        "duration_type",
        "price",
    )

    search_fields = (
        "name",
        "price",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "price",
                    "max_properties",
                    "duration_type",
                    "is_default",
                )
            },
        ),
        (
            "Guidance",
            {
                "description": (
                    "Setting 'is_default' will automatically assign this plan to new users. "
                    "Only one plan can be set as default. "
                    "Use 0 for 'Max Properties' to indicate Unlimited. "
                    "Duration type determines if this plan is Monthly or Yearly."
                ),
                "fields": (),
            },
        ),
    )

    # Display Max Properties as "Unlimited" if 0
    def max_properties_display(self, obj):
        if obj.max_properties == 0:
            return "Unlimited"
        return obj.max_properties

    max_properties_display.short_description = "Max Properties"
    max_properties_display.admin_order_field = "max_properties"

    # Display price nicely
    def price_display(self, obj):
        return f"{obj.price} Kyat"

    price_display.short_description = "Price"
    price_display.admin_order_field = "price"

    # Run clean() to check if default package is valid
    def verbose_clean_status(self, obj):
        try:
            obj.clean()
            return "✅ Valid"
        except ValidationError as e:
            return f"❌ Error: {e.message}"
        except Exception:
            return "⚠️ Unknown Error"

    verbose_clean_status.short_description = "Default Status Check"
