from django.db import models
import uuid


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True, editable=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"

    def save(self, *args, **kwargs):
        if not self.code:
            new_code = str(uuid.uuid4())[:8].upper()

            while Company.objects.filter(code=new_code).exists():
                new_code = str(uuid.uuid4())[:8].upper()

            self.code = new_code

        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
