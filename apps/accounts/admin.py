from django.contrib import admin
from .models import Profile
from apps.property.models import Property
from apps.order.models import Order

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone",
        "user_type",
        "total_max_properties_display",
        "posted_properties_count",
        "remaining_properties",
    )
    search_fields = ("user__username", "user__email", "phone")
    list_filter = ("user_type",)
    readonly_fields = (
        "total_max_properties_display",
        "posted_properties_count",
        "remaining_properties",
    )

    # Total allowed properties from approved orders
    def total_max_properties_display(self, obj):
        return obj.total_max_properties()

    total_max_properties_display.short_description = "Total Max Properties"

    # Count of already posted properties
    def posted_properties_count(self, obj):
        return Property.objects.filter(user=obj.user).count()

    posted_properties_count.short_description = "Posted Properties"

    # Remaining posts
    def remaining_properties(self, obj):
        remaining = obj.total_max_properties() - self.posted_properties_count(obj)
        return max(remaining, 0)

    remaining_properties.short_description = "Remaining Properties"
