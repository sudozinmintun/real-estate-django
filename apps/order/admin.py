from django.contrib import admin
from .models import Order
from django.utils.html import format_html


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "user",
        "package_name",
        "payment",
        "amount",
        "status",
        "screenshot_preview",
        "start_date",
        "end_date",
        "created_at",
    )

    search_fields = (
        "order_id",
        "user__username",
        "user__email",
        "package_name",
    )

    list_editable = ("status",)

    def screenshot_preview(self, obj):
        if obj.screenshot:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="height:60px;border-radius:4px;" />'
                "</a>",
                obj.screenshot.url,
                obj.screenshot.url,
            )
        return "—"

    screenshot_preview.short_description = "Screenshot"
