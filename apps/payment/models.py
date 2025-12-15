from django.db import models


class Payment(models.Model):
    bank_name = models.CharField(max_length=50, blank=True, null=True)
    account_name = models.CharField(max_length=50, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    icon = models.ImageField(upload_to="payment/icons/")

    def __str__(self):
        return self.bank_name
