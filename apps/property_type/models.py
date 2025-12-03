from django.db import models


class PropertyType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Property Type"
        verbose_name_plural = "Property Types"
        
    def __str__(self):
        return self.name
