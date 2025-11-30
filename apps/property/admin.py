from django.contrib import admin
from .models import Property
from .forms import PropertyAdminForm


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    form = PropertyAdminForm
    list_display = ("title", "user", "price", "country", "city")
    search_fields = ("title", "user__username")
    list_filter = ("country", "city")
