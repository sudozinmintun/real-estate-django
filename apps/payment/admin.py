from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['bank_name', "account_name", "account_number"]  
    search_fields = ['bank_name', "account_name", "account_number"] 