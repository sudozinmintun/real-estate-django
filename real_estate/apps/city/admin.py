from django.contrib import admin
from .models import City, Township


@admin.register(City)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "country"]
    search_fields = ["name", "country__name"] 


@admin.register(Township)
class TownshipAdmin(admin.ModelAdmin):
    list_display = ["name", "city"]
    search_fields = ["name", "city__name"]
